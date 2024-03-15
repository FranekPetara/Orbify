from . import models, schemas, database


def create_project(project: dict) -> dict:
    db_project = models.Project(**project)
    with database.db_context() as db:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
    return project


def read_project(project_id: int):
    with database.db_context() as db:
        project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project:
        return schemas.Project.from_orm(project).model_dump()
    return None


def update_project(project_id: int, project: dict) -> dict:
    with database.db_context() as db:
        db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if db_project:
            for key, value in project.items():
                setattr(db_project, key, value)
            db.commit()
            db.refresh(db_project)
        else:
            return None
    return schemas.Project.from_orm(db_project).model_dump()


def delete_project( project_id: int):
    with database.db_context() as db:
        project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if project:
            db.delete(project)
            db.commit()
            return True
    return False


def list_projects(skip: int = 0, limit: int = 10):
    with database.db_context() as db:
        projects = db.query(models.Project).offset(skip).limit(limit).all()
        if len(projects) == 0:
            return None
        projects_list = [schemas.Project.from_orm(project).model_dump() for project in projects]

    return projects_list
