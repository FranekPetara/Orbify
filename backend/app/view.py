from fastapi import APIRouter, HTTPException, status

from . import schemas, tasks

router = APIRouter()


@router.post("/projects/", status_code=status.HTTP_202_ACCEPTED)
async def create_project(project: schemas.ProjectCreate):
    try:
        project_data = project.model_dump()
        tasks.create_project.delay(project_data)
        return {"message": "Project created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}", response_model=schemas.Project)
async def read_project(project_id: int):
    try:
        project_asy = tasks.read_project.delay(project_id)
        project = project_asy.get()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/projects/{project_id}", response_model=schemas.Project)
async def update_project(project_id: int, project: schemas.ProjectUpdate):
    try:
        project_data = project.model_dump()
        db_project = tasks.update_project.delay(project_id, project_data)
        updated_project = db_project.get()
        if updated_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return updated_project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(project_id: int):
    try:
        db_project = tasks.delete_project.delay(project_id)
        updated_project = db_project.get()
        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/", response_model=schemas.ProjectList)
async def list_projects(skip: int = 0, limit: int = 10):
    try:
        projects = tasks.list_projects.delay(skip, limit)
        projects_list = projects.get()
        if not projects_list:
            raise HTTPException(status_code=404, detail="Projects not found")
        return {"projects": projects_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))