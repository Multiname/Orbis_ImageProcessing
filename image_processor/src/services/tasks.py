from models.models import Task, engine

from sqlalchemy.orm import Session
from datetime import datetime


def serialize_task(task):
    result = {
        "id": task.id,
        "source_id": task.source_id,
        "result_id": task.result_id,
        "status": task.status,
        "created_at": str(task.created_at),
        "updated_at": str(task.updated_at) if task.updated_at != None else None,
        "algorithm": task.algorithm,
    }

    if hasattr(task, "params"):
        result["params"] = task.params

    return result


def serialize_tasks(tasks):
    result = []

    for task in tasks:
        result.append(serialize_task(task))

    return result


def get_all_tasks_entries():
    with Session(autoflush=False, bind=engine) as session:
        tasks = session.query(Task).all()
    return serialize_tasks(tasks)


def create_task_entry(source_id, algorithm, params=None):
    task = Task()
    task.source_id = source_id
    task.algorithm = algorithm
    task.params = params

    with Session(autoflush=False, bind=engine) as session:
        session.add(task)
        session.commit()

        return task.id


def get_task_entry(id):
    with Session(autoflush=False, bind=engine) as session:
        task = session.query(Task).filter(Task.id == id).first()
    return serialize_task(task)


def set_task_status(id, status):
    with Session(autoflush=False, bind=engine) as session:
        task = session.query(Task).filter(Task.id == id).first()

        task.status = status
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()


def set_result(task_id, result_id):
    with Session(autoflush=False, bind=engine) as session:
        task = session.query(Task).filter(Task.id == task_id).first()

        task.result_id = result_id
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        return task
