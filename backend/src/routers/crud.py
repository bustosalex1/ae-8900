"""Create, Read, Update, Delete (CRUD) endpoints for my AE 8900 backend API."""
import glob
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

import yaml
from fastapi import APIRouter, HTTPException

from src.management import project_management, utils
from src.management.dependencies import (DataManagerDependency,
                                         ProjectSettingsDependency)
from src.models import core

router = APIRouter()


@router.get("/projects")
async def get_projects() -> List[core.ProjectState]:
    """Return the ProjectState for all projects in the PROJECTS_DIR directory."""
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


@router.post("/active_project")
async def set_active_project(active_project_config: str, project_settings: ProjectSettingsDependency) -> None:
    """Set the active project in the backend."""
    print(f"setting active project to {Path(active_project_config).parent}")
    project_settings.active_project_directory = Path(active_project_config).parent


@router.post("/project")
async def create_project(state: core.ProjectState, project_settings: ProjectSettingsDependency) -> core.ProjectState:
    """
    Scaffold a new project in PROJECTS_DIR with a configuration file and some folders.

    :param configuration: the configuration of the new project to create.
    :return: the configuration of the new project that was created.
    """
    # make the folder structure associated with the project
    project_directory = project_management.PROJECTS_DIR / utils.safe_string(state.configuration.title)

    # update the active project directory on change
    project_settings.active_project_directory = project_directory

    if os.path.exists(project_directory):
        raise HTTPException(
            status_code=400,
            detail=f"A project named {state.configuration.title} already exists under {project_directory}.",
        )
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
        config_file.write(yaml.dump(state.configuration.dict()))
        config_file.close()
        state = project_management.load_project(project_directory / "config.yaml")

    return state


@router.put("/project")
async def update_project(state: core.ProjectState, project_settings: ProjectSettingsDependency) -> core.ProjectState:
    """
    Update a project's config.yaml.

    :param state: the updated project state.
    :return: the updated project information.
    """
    # determine if the filepath for the project has changed
    filepath = Path(state.metadata.filepath)
    original_folder = filepath.parent
    updated_folder = project_management.PROJECTS_DIR / utils.safe_string(state.configuration.title)

    if original_folder != updated_folder:
        if os.path.exists(updated_folder):
            raise HTTPException(
                status_code=400,
                detail=f"A project named {state.configuration.title} already exists under {updated_folder}.",
            )
        os.rename(original_folder, updated_folder)
        project_settings.active_project_directory = updated_folder
        filepath = updated_folder / "config.yaml"

    with open(filepath, "w") as config_file:
        config_file.write(yaml.dump(state.configuration.dict()))
        config_file.close()

    updated_project = project_management.load_project(filepath)
    return updated_project


@router.delete("/project")
async def delete_project(state: core.ProjectState) -> None:
    """Delete a project and all of its associated files."""
    shutil.rmtree(Path(state.metadata.filepath).parent)


@router.post("/start_recording")
async def start_recording(sources: List[str], interval: float, data_manager: DataManagerDependency, project_settings: ProjectSettingsDependency) -> None:
    """
    Start recording data.

    I think.
    """
    if project_settings.active_project_directory:
        filepath = project_settings.active_project_directory / f"{datetime.now()}.csv"
        data_manager.start_recording(sources=sources, filepath=filepath, interval=interval)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Recording cannot be started with no active project.",
        )


@router.post("/stop_recording")
async def stop_recording(data_manager: DataManagerDependency) -> None:
    """
    Start recording data.

    I think.
    """
    await data_manager.stop_recording()
