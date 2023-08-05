import os
from pathlib import Path


def resolve() -> str:
    # path in DBX Repos is like /Workspace/Repos/folder/repository/src/...
    # so we take first 4 parts which is the root of the repository
    repository_root = os.path.join(*Path.cwd().parts[0:5])

    if "DAIPE_PROJECT_ROOT_DIR" in os.environ:
        return os.environ["DAIPE_PROJECT_ROOT_DIR"].format(repository_root=repository_root)

    return repository_root
