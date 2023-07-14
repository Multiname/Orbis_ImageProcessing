import json


class Config:
    __config = open("config/config.json")
    __params = json.load(__config)
    __config.close()

    class __Flask:
        def __init__(self):
            self.debug = ""
            self.host = ""

    flask = __Flask()
    flask.debug = __params["flask"]["debug"]
    flask.host = __params["flask"]["host"]

    sqlalchemy_database_uri = __params["sqlalchemy_database_uri"]

    class __Connections:
        class __Pika:
            def __init__(self):
                self.host = ""
                self.username = ""
                self.password = ""

        def __init__(self):
            self.file_server_url = ""
            self.pika = self.__Pika()

    connections = __Connections()
    connections.file_server_url = __params["connections"]["file_server_url"]
    connections.pika.host = __params["connections"]["pika"]["host"]
    connections.pika.username = __params["connections"]["pika"]["username"]
    connections.pika.password = __params["connections"]["pika"]["password"]

    image_processing_temp_directory = __params["image_processing_temp_directory"]
