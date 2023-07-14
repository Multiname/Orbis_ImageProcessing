from injectors.init_connections import get_pika_connection, FileServer
from injectors.init_temp_folder import make_temp_file
from services.algorithm_factory import AlgorithmFactory
from models.models import Status
import services.tasks as tasks

import os


def connect(set_processing_task_id):
    print("worker is listening...")

    connection = get_pika_connection()
    channel = connection.channel()
    channel.queue_declare(queue="tasks")

    def callback(ch, method, properties, body):
        id = int(body)
        print(f"recieved: {id}")
        set_processing_task_id(id)
        tasks.set_task_status(id, Status.processing)

        task = tasks.get_task_entry(id)
        result_id = complete_task(task)
        if result_id == None:
            return
        print("result_id: " + str(result_id))

        tasks.set_result(id, result_id)
        tasks.set_task_status(id, Status.finished)
        set_processing_task_id(None)

    channel.basic_consume(queue="tasks", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def handle_error(taskId, msg):
    print(f"error: {msg}")
    tasks.set_task_status(taskId, Status.error)


def complete_task(task):
    fileInfo = FileServer.get_file_info(task["source_id"]).json()
    if not fileInfo:
        handle_error(task["id"], "source file was not found")
        return None

    file = FileServer.download_file(task["source_id"])
    tempFile = make_temp_file(fileInfo, file.content)

    factory = AlgorithmFactory()
    algorithm = factory.get_algorithm(task["algorithm"])
    isProcessed, algorithmResult = algorithm.process(tempFile, task["params"])

    if not isProcessed:
        handle_error(task["id"], algorithmResult)
        return None
    resultFile = algorithmResult

    files = {"file": open(resultFile, "rb")}
    data = {
        "comment": "Changed with algorithm: " + task["algorithm"],
    }
    response = FileServer.upload_file(files, data)
    if response.status_code == 400:
        handle_error(task["id"], str(response.content, encoding="utf-8"))
        return None

    response_json = response.json()

    files["file"].close()
    os.remove(tempFile)
    os.remove(resultFile)

    return response_json["id"]


def handle_exit(processing_task_id):
    if processing_task_id:
        tasks.set_task_status(processing_task_id, Status.error)

        connection = get_pika_connection()
        channel = connection.channel()
        channel.queue_declare(queue="tasks")

        channel.basic_publish(exchange="", routing_key="tasks", body=str(processing_task_id))
        connection.close()