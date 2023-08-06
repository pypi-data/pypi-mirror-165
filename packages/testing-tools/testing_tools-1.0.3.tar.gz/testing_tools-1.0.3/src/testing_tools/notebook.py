import contextlib
import json
import os
from pathlib import Path
from typing import Any, Generator, List, Optional, Set, Union
from unittest.mock import Mock

from nbconvert.preprocessors.execute import CellExecutionError
from nbformat import notebooknode
from testbook import testbook

from testing_tools.error import TestingToolsError


def is_executed_by_pytest() -> bool:
    """Returns true if the code is being executed by pytest."""
    return "RUN_BY_PYTEST" in os.environ


def create_mock_manager(*mocks: Any) -> Mock:
    manager = Mock()
    for mock in mocks:
        manager.attach_mock(mock, "mock_" + mock._extract_mock_name())
    return manager


def list_notebooks(
    path: Optional[Union[Path, str]] = None,
    relative: Optional[Union[Path, str]] = None,
) -> List[str]:
    path = Path(path)
    path_list = get_paths_of_interest(
        pattern="*.ipynb",
        folder=path,
        banned_parents={".ipynb_checkpoints"},
        relative=relative,
    )
    return sorted(map(str, path_list))


def get_paths_of_interest(
    pattern: str,
    folder: Path,
    banned_parents: Optional[Set[str]] = None,
    relative: Optional[Union[Path, str]] = None,
) -> List[Path]:
    if banned_parents is None:
        banned_parents = set()

    path_set = {
        folder / file_path
        for file_path in folder.rglob(pattern)
        if len(set(file_path.parts) & banned_parents) == 0
    }

    if relative is not None:
        path_set = {file_path.relative_to(relative) for file_path in path_set}

    return sorted(path_set)


def assert_notebook_is_without_outputs(notebook_path: Union[str, Path]) -> None:
    notebook_path = Path(notebook_path)
    assert notebook_path.exists()

    with open(notebook_path, "r") as file:
        notebook = notebooknode.from_dict(json.load(file))

    notebook_has_outputs = any(
        len(cell.get("outputs", [])) > 0 for cell in notebook.cells
    )

    if notebook_has_outputs:
        raise AssertionError(
            f"The following notebook contains outputs: {notebook_path}"
        )


def assert_notebook_runs_without_errors(
    notebook_path: Union[str, Path],
    timeout: int = -1,
) -> None:
    notebook_path = Path(notebook_path)
    assert notebook_path.exists()

    try:
        with change_working_directory(notebook_path.parent):
            with testbook(notebook_path, timeout=timeout, execute=True):
                pass
    except CellExecutionError as error:
        raise TestingToolsError(error) from None


@contextlib.contextmanager
def change_working_directory(path: Union[str, Path]) -> Generator[None, None, None]:
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(prev_cwd)
