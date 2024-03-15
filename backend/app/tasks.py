from celery import shared_task
from . import crud


@shared_task(name="create_project")
def create_project(project):
    db_project = crud.create_project(project)
    return db_project


@shared_task(name="read_project")
def read_project(project_id):
    db_project = crud.read_project(project_id)
    return db_project


@shared_task(name="update_project")
def update_project(project_id, project):
    db_project = crud.update_project(project_id, project)
    return db_project


@shared_task(name="delete_project")
def delete_project(project_id):
    db_project = crud.delete_project(project_id)
    return db_project


@shared_task(name="list_projects")
def list_projects(skip, limit):
    db_projects = crud.list_projects(skip, limit)
    return db_projects
