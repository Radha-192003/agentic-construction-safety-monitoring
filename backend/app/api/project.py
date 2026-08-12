from fastapi import APIRouter
from app.models.project import Project

router = APIRouter()

projects = []

@router.get("/")
def get_projects():
    return projects


@router.post("/")
def add_project(project: Project):
    projects.append(project)
    return {
        "message": "Project added successfully",
        "project": project
    }