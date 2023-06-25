"""Project management utilities for my AE 8900 backend."""
import os
from datetime import datetime
from pathlib import Path

import yaml

from ae8900.models import core

# constant directories
BACKEND_DIR = Path(__file__).parent.parent.parent.parent
PROJECTS_DIR = BACKEND_DIR / "projects"
SRC_DIR = BACKEND_DIR / "src"


def load_project(filepath: Path) -> core.ProjectState:
    """
    Load a project configuration from a valid YAML configuration file, as well as relevant metadata.

    :param filepath: the absolute filepath to the configuration file.
    :return: a ProjectState instance corresponding to the project.
    """
    # open the file
    with open(filepath, "r") as file:
        # create a new project state from its configuration and metadata
        project_state = core.ProjectState(
            configuration=core.ProjectConfiguration(
                **yaml.safe_load(file),
            ),
            metadata=core.ProjectMetadata(
                filepath=str(filepath.expanduser()),
                last_modified=datetime.fromtimestamp(os.path.getctime(filepath)),
            ),
        )

    return project_state
