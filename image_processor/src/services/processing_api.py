from injectors.init_connections import get_pika_connection


def check_field_missing(content, field):
    return field not in content or not content[field]


def find_missing_field(content, fields):
    for field in fields:
        if check_field_missing(content, field):
            return field
    return None


def find_missing_param(content, algorithm):
    params = {"flip": ["orientation"], "resize": ["width", "height"], "rotate": ["direction"]}

    if len(params[algorithm]) > 0:
        for param in params[algorithm]:
            if param not in content["params"] or not content["params"][param]:
                return param

    return None


def send_task(task_id):
    connection = get_pika_connection()
    channel = connection.channel()

    channel.queue_declare(queue="tasks")

    channel.basic_publish(exchange="", routing_key="tasks", body=str(task_id))
    connection.close()
