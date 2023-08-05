import logging
from penvy.env.EnvConfig import EnvConfig
from penvy.PenvyConfig import PenvyConfig
from benvy.databricks.repos import project_root_resolver


class BootstrapConfig(EnvConfig):
    def get_parameters(self) -> dict:
        poetry_version = PenvyConfig().get_parameters()["poetry"]["install_version"]

        return {
            "project": {
                "dir": project_root_resolver.resolve(),
            },
            "poetry": {
                "version": poetry_version,
                "home": "/root/.poetry",
                "executable": "/root/.poetry/bin/poetry",
                "archive_url": f"https://github.com/python-poetry/poetry/releases/download/{poetry_version}/poetry-{poetry_version}-linux.tar.gz",
                "install_script_url": "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py",
                "archive_path": f"/dbfs/FileStore/jars/daipe/poetry/poetry-{poetry_version}-linux.tar.gz",
                "install_script_path": "/dbfs/FileStore/jars/daipe/poetry/get-poetry.py",
            },
            "logger": {
                "name": "daipe-bootstrap",
                "level": logging.INFO,
            },
        }
