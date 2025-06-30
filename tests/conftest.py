from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture
def tmp_dir():
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
