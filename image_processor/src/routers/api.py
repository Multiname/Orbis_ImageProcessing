from injectors.init_app import app
from models.models import Status
import services.processing_api as processing_api
import services.tasks as tasks

from flask import request
from flask_cors import cross_origin
import json


@app.route("/api/image-processing/", methods=["GET"])
@cross_origin()
def get_tasks():
    return tasks.get_all_tasks_entries()


@app.route("/api/image-processing/", methods=["POST"])
@cross_origin()
def create_task():
    content = request.get_json()

    missing_field = processing_api.find_missing_field(
        content, ["file_ids", "algorithm", "params"]
    )
    if missing_field:
        return "{} field is missing".format(missing_field), 400

    if len(content["file_ids"]) == 0:
        return "specify at least one task", 400

    missing_param = processing_api.find_missing_param(content, content["algorithm"])
    if missing_param:
        return "{} parameter is missing".format(missing_param), 400

    task_ids = []
    for source_id in content["file_ids"]:
        params = None
        if "params" in content:
            params = content["params"]

        task_id = tasks.create_task_entry(source_id, content["algorithm"], params)
        processing_api.send_task(task_id)
        task_ids.append(task_id)

    return json.dumps({"task_ids": task_ids})


@app.route("/api/image-processing/<int:id>", methods=["GET"])
@cross_origin()
def get_task(id):
    return tasks.get_task_entry(id)


@app.route("/api/image-processing/<int:id>/restart", methods=["POST"])
@cross_origin()
def restart_task(id):
    task = tasks.get_task_entry(id)
    if task["status"] != "error":
        return "task hasn't failed", 405
    tasks.set_task_status(id, Status.pending)
    processing_api.send_task(id)
    return tasks.get_task_entry(id)
