import os
import json
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.poetry.DependenciesLoader import DependenciesLoader
from penvy.shell.runner import run_and_read_line


class DbrDependenciesChecker(SetupStepInterface):
    def __init__(
        self,
        project_root_path: str,
        logger: Logger,
        dependencies_loader: DependenciesLoader,
    ):
        self._project_root_path = project_root_path
        self._logger = logger
        self._dependencies_loader = dependencies_loader

    def run(self):
        self._logger.info("Checking DBR dependencies")

        dbr_dependencies = self._get_dbr_dependencies()
        lock_dependencies = self._dependencies_loader.load_main()

        self._check_dependencies(dbr_dependencies, lock_dependencies)  # noqa

    def get_description(self):
        return "Check DBR dependencies"

    def should_be_run(self) -> bool:
        return "DAIPE_BOOTSTRAPPED" not in os.environ

    def _get_dbr_dependencies(self):
        dependencies = json.loads(run_and_read_line("pip list --format json", shell=True))

        return {dependency["name"]: {"version": dependency["version"]} for dependency in dependencies}

    def _check_dependencies(self, dbr_dependencies, lock_dependencies):
        mismatched_dependencies = {}

        for dbr_dependency in dbr_dependencies:
            if dbr_dependency in lock_dependencies:
                dbr_dependency_version = dbr_dependencies[dbr_dependency]["version"]
                lock_dependency_version = lock_dependencies[dbr_dependency]["version"]

                if dbr_dependency_version != lock_dependency_version:
                    mismatched_dependencies[dbr_dependency] = {
                        "dbr_version": dbr_dependency_version,
                        "lock_version": lock_dependency_version,
                    }

        if not mismatched_dependencies:
            self._logger.info("Dependencies OK")
            return

        for dependency in mismatched_dependencies:
            dbr_dependency_version = mismatched_dependencies[dependency]["dbr_version"]
            lock_dependency_version = mismatched_dependencies[dependency]["lock_version"]

            self._logger.warning(
                f"DBR dependency '{dependency}=={dbr_dependency_version}' does not match poetry.lock version '{lock_dependency_version}'"
            )

        self._logger.warning("Consider locking those dependencies in 'pyproject.toml'")
