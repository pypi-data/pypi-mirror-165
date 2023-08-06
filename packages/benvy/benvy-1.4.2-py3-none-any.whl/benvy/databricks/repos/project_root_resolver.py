import os
import sys


def resolve_project_root() -> str:
    repository_root = resolve_repository_root()

    if "DAIPE_PROJECT_ROOT_DIR" in os.environ:
        return os.environ["DAIPE_PROJECT_ROOT_DIR"].format(repository_root=repository_root)

    return repository_root


def resolve_repository_root() -> str:
    # Databricks automatically adds repository root dir and current notebook dir to sys path, e.g.
    # ["/Workspace/Repos/folder/repository", "/Workspace/Repos/folder/repository/src/dir", ...]
    # So we take the shortest path that starts with '/Workspace/Repos'
    return min([path for path in sys.path if path.startswith("/Workspace/Repos")], key=len)
