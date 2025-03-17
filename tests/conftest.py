import pytest
import tempfile
import shutil

@pytest.fixture
def temp_cache_dir():
    """
    Creates a temporary directory for cache, then cleans up after tests.
    """
    tmpdir = tempfile.mkdtemp(prefix="meltingface_test_")
    yield tmpdir
    shutil.rmtree(tmpdir)  # clean up after test
