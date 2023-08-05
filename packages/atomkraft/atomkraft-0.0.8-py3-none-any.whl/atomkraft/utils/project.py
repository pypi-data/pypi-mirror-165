import os
from pathlib import Path


def project_root():
    cwd = Path(os.getcwd())
    while cwd != cwd.parent:
        if (
            (cwd / "pyproject.toml").exists()
            and (cwd / "atomkraft.toml").exists()
            and (cwd / ".atomkraft" / "config.toml").exists()
        ):
            return cwd
        cwd = cwd.parent
