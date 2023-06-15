"""Create, Read, Update, Delete (CRUD) endpoints for my AE 8900 backend API."""
from typing import List
import yaml
import glob
from fastapi import APIRouter
from src.models import core
from src.management import project_management, utils

router = APIRouter()


@router.get("/projects/")
async def get_projects() -> List[core.ProjectConfiguration]:
    """Return the configurations for all projects in the PROJECTS_DIR directory."""
    # find all the valid projects
    project_configs = glob.glob(
        pathname="*/config.yaml",
        root_dir=project_management.PROJECTS_DIR,
        recursive=True,
    )

    # load them in
    projects = []

    for filepath in project_configs:
        projects.append(
            project_management.load_project(
                project_management.PROJECTS_DIR / filepath,
            )
        )

    return projects


@router.post("/project/")
async def create_project(configuration: core.ProjectConfiguration) -> core.ProjectConfiguration:
    """
    Scaffold a new project in PROJECTS_DIR with a configuration file and some folders.

    :param configuration: the configuration of the new project to create.
    :return: the configuration of the new project that was created.
    """
    # make the folder structure associated with the project
    project_directory = project_management.PROJECTS_DIR / utils.safe_string(configuration.title)

    project_template = [
        project_directory,
        project_directory / "tests",
        project_directory / "assets",
        project_directory / "data",
    ]

    for filepath in project_template:
        filepath.mkdir(parents=True)

    # write the YAML config file
    with open(project_directory / "config.yaml", "w") as config_file:
        config_file.write(yaml.dump(configuration.dict()))
        config_file.close()

    return configuration
