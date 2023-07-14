from config.config import Config

import pika, requests


def get_pika_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=Config.connections.pika.host,
            credentials=pika.PlainCredentials(
                Config.connections.pika.username, Config.connections.pika.password
            ),
        )
    )


class FileServer:
    @staticmethod
    def get_file_info(id):
        fileInfoUrl = f"{Config.connections.file_server_url}/api/file-server/{id}"
        return requests.get(fileInfoUrl)

    @staticmethod
    def download_file(id):
        fileUrl = f"{Config.connections.file_server_url}/api/file-server/{id}/download"
        return requests.get(fileUrl)

    @staticmethod
    def upload_file(files, data):
        uploadUrl = f"{Config.connections.file_server_url}/api/file-server/"
        return requests.post(uploadUrl, files=files, json=data)
