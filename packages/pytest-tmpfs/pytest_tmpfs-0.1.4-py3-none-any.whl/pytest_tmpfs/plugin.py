"""Pytest interface for tmpfs."""
from pathlib import Path
import pytest
from pytest_tmpfs.fs import TmpFs


@pytest.fixture(scope="function")
def tmpfs(tmp_path: Path):
    """Creates a temporary file system for testing."""
    return TmpFs(tmp_path)  # pragma: no cover


@pytest.fixture(autouse=True)
def doctest(doctest_namespace: dict, tmpfs: TmpFs):
    """Adds the temporary file system to the doctest namespace."""
    doctest_namespace["fs"] = tmpfs  # pragma: no cover
