"""Project management utilities for my AE 8900 backend."""
import yaml
from pathlib import Path
from src.models import core


# constant directories
BACKEND_DIR = Path(__file__).parent.parent.parent
PROJECTS_DIR = BACKEND_DIR / "projects"
SRC_DIR = BACKEND_DIR / "src"


def load_project(filepath: Path) -> core.ProjectConfiguration:
    """
    Load a project configuration from a valid YAML configuration file.

    :param filepath: the absolute filepath to the configuration file.
    :return: a ProjectConfiguration instance corresponding to the project.
    """
    # open the file
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)

    # return a ProjectConfiguration instance
    return core.ProjectConfiguration(**data)
