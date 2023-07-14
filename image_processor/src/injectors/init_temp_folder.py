from config.config import Config

from pathlib import Path


def make_temp_file(fileInfo, content):
    direcotry = Path.cwd() / ".." / Config.image_processing_temp_directory
    direcotry.mkdir(parents=True, exist_ok=True)

    tempFile = direcotry / (fileInfo["name"] + fileInfo["extension"])

    file = open(tempFile, "wb")
    file.write(content)
    file.close()

    return tempFile
