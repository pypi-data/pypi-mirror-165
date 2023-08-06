import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

from memory_tempfile import MemoryTempfile
from typing import Optional


def mkd_tmpfs(
    prefix: Optional[str] = None, suffix: Optional[str] = None, dir: None = None
) -> tempfile.TemporaryDirectory:
    """
    Create a temporary directory, preferably RAM backed, for speed
    @return tempfile.TemporaryDirectory
    """
    tmpfs_dir = os.environ.get("TMPFS_DIR", None)
    additional_paths = [tmpfs_dir] if tmpfs_dir is not None else []
    temp = MemoryTempfile(additional_paths=additional_paths, fallback=True)
    if not hasattr(temp, "tempdir"):
        # Bug: memory_tempfile does not set the temp.tempdir attribute on non Linux OSes
        # Attribute set manually as a workaround until the library is
        # eventually fixed
        setattr(temp, "tempdir", tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=dir))
    return temp.TemporaryDirectory(prefix=prefix, suffix=suffix, dir=dir)


def mkd_tmp(
    prefix: Optional[str] = None, suffix: Optional[str] = None, dir: Optional[str] = None
) -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix=prefix, suffix=suffix, dir=dir)


@contextmanager
def mkf_tmpfs(
    prefix: Optional[str] = None, suffix: Optional[str] = None, dir: Optional[str] = None
) -> Path:
    """
    Create a temporary file, preferably RAM backed, for speed
    """
    with mkd_tmpfs(dir=dir) as tmp_dir:
        file_name = None
        with tempfile.NamedTemporaryFile(
            prefix=prefix, suffix=suffix, dir=tmp_dir, delete=False
        ) as f:
            file_name = f.name
        yield Path(file_name)
