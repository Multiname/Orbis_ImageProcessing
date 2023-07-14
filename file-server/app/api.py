from app import app
from .models import FileInfo, engine
from sqlalchemy.orm import Session
from flask import request, send_file, jsonify, make_response
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
#from win32_setctime import setctime
import calendar
from flask_cors import cross_origin


def FindAllFilesInfo():
    with Session(autoflush=False, bind=engine) as session:
        return session.query(FileInfo).all()


def FindFileInfoById(id):
    with Session(autoflush=False, bind=engine) as session:
        return session.query(FileInfo).filter(FileInfo.id == id).first()


def FindFileInfoByPath(path, name, extension):
    with Session(autoflush=False, bind=engine) as session:
        return (
            session.query(FileInfo)
            .filter(FileInfo.name == name)
            .filter(FileInfo.extension == extension)
            .filter(FileInfo.path == path)
            .first()
        )


def SyncFilePresence(path, name, extension):
    fullpath = os.getcwd() + app.config["UPLOAD_FOLDER"] + path + name + extension

    if os.path.exists(fullpath):
        fileInfo = FileInfo()

        fileInfo.name = name
        fileInfo.extension = extension
        fileInfo.size = os.path.getsize(fullpath)
        fileInfo.path = path
        fileInfo.created_at = datetime.utcfromtimestamp(
            os.path.getctime(fullpath)
        ) + timedelta(hours=3)

        updated_at = datetime.utcfromtimestamp(os.path.getmtime(fullpath)) + timedelta(
            hours=3
        )
        fileInfo.updated_at = updated_at if fileInfo.created_at != updated_at else None

        fileInfo.comment = None

        with Session(autoflush=False, bind=engine) as session:
            session.add(fileInfo)
            session.commit()
            return True, fileInfo

    return False, None


def SyncFileAbsence(fileInfo):
    fullpath = (
        os.getcwd()
        + app.config["UPLOAD_FOLDER"]
        + fileInfo.path
        + fileInfo.name
        + fileInfo.extension
    )

    if not os.path.exists(fullpath):
        with Session(autoflush=False, bind=engine) as session:
            session.delete(fileInfo)
            session.commit()

        return True

    return False


def SyncFoldersFilesPresence(folder):
    root = os.getcwd() + app.config["UPLOAD_FOLDER"]
    cd = root + folder

    content = os.listdir(cd)
    for obj in content:
        if os.path.isfile(cd + obj):
            name, extension = obj.split(".")
            extension = "." + extension
            fileInfo = FindFileInfoByPath(folder, name, extension)
            if fileInfo == None:
                SyncFilePresence(folder, name, extension)
        else:
            SyncFoldersFilesPresence(folder + obj + "/")


def SyncFoldersFilesAbsence(folder):
    allFilesInfo = FindAllFilesInfo()
    filesInfo = list(filter(lambda x: x.path.find(folder) == 0, allFilesInfo))

    for fileInfo in filesInfo:
        if not os.path.exists(
            os.getcwd()
            + app.config["UPLOAD_FOLDER"]
            + fileInfo.path
            + fileInfo.name
            + fileInfo.extension
        ):
            with Session(autoflush=False, bind=engine) as session:
                session.delete(fileInfo)
                session.commit()


def SyncFoldersFiles(folder):
    SyncFoldersFilesPresence(folder)
    SyncFoldersFilesAbsence(folder)


def SyncFile(fileInfo, path, name, extension):
    isExisting = False
    if fileInfo == None:
        isExisting, fileInfo = SyncFilePresence(path, name, extension)
        if not isExisting:
            return None

    if not isExisting:
        if SyncFileAbsence(fileInfo):
            return None

    return fileInfo


def SerializeFileInfo(fileInfo):
    return {
        "id": fileInfo.id,
        "name": fileInfo.name,
        "extension": fileInfo.extension,
        "size": fileInfo.size,
        "created_at": str(fileInfo.created_at),
        "updated_at": str(fileInfo.updated_at) if fileInfo.updated_at != None else None,
        "comment": fileInfo.comment,
    }


def SerializeFilesInfo(filesInfo):
    result = []
    for fileInfo in filesInfo:
        result.append(SerializeFileInfo(fileInfo))

    return result


def HandleFilepath(filepath):
    splited = filepath.split("/")
    index = -1 if splited[-1] != "" else -2
    name, extension = splited[index].split(".")
    extension = "." + extension
    path = "/" + "/".join(splited[:index]) + "/"
    if path == "//":
        path = "/"
    return path, name, extension


@app.route("/api/file-server/", methods=["GET"])
@cross_origin()
def get_files_info():
    SyncFoldersFiles("/")

    filesInfo = FindAllFilesInfo()

    return jsonify(SerializeFilesInfo(filesInfo))


@app.route("/api/file-server/<int:id>", methods=["GET"])
@cross_origin()
def get_file_info_by_id(id):
    fileInfo = FindFileInfoById(id)
    if fileInfo == None:
        return "not found", 404

    if SyncFileAbsence(fileInfo):
        return "not found", 404

    return jsonify(SerializeFileInfo(fileInfo))


@app.route("/api/file-server/", methods=["POST"])
@cross_origin()
def upload_file():
    if "file" not in request.files:
        return "no file to load", 400

    file = request.files["file"]

    if not file:
        return "no file to load", 400

    filename = ""
    if "name" in request.form and request.form["name"]:
        filename = secure_filename(request.form["name"])
    else:
        filename = secure_filename(file.filename)

    name, extension = filename.split(".")
    extension = "." + extension

    root = os.getcwd() + app.config["UPLOAD_FOLDER"] + "/"
    path = root + filename
    while os.path.exists(path):
        if not FindFileInfoByPath("/", name, extension):
            SyncFilePresence("/", name, extension)
        name += "_duplicate"
        path = root + name + extension
        # return "file already exists", 400

    fileInfoCheck = FindFileInfoByPath("/", name, extension)
    if fileInfoCheck != None:
        SyncFileAbsence(fileInfoCheck)

    file.save(path)

    fileInfo = FileInfo()

    fileInfo.name = name
    fileInfo.extension = extension
    fileInfo.size = os.path.getsize(path)
    fileInfo.path = "/"
    fileInfo.created_at = datetime.utcfromtimestamp(os.path.getctime(path)) + timedelta(
        hours=3
    )
    fileInfo.updated_at = None

    comment = None
    if "comment" in request.form:
        comment = request.form["comment"]
    fileInfo.comment = comment

    with Session(autoflush=False, bind=engine) as session:
        session.add(fileInfo)
        session.commit()

        return jsonify(SerializeFileInfo(fileInfo))


@app.route("/api/file-server/<int:id>/download", methods=["GET"])
@cross_origin()
def download_file_by_id(id):
    fileInfo = FindFileInfoById(id)
    if fileInfo == None or SyncFileAbsence(fileInfo):
        return "not found", 404

    response = make_response(
        send_file(
            os.getcwd()
            + app.config["UPLOAD_FOLDER"]
            + fileInfo.path
            + fileInfo.name
            + fileInfo.extension,
            as_attachment=True,
        )
    )
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response


@app.route("/api/file-server/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_file_by_id(id):
    fileInfo = FindFileInfoById(id)
    if fileInfo == None or SyncFileAbsence(fileInfo):
        return "not found", 404

    os.remove(
        os.getcwd()
        + app.config["UPLOAD_FOLDER"]
        + fileInfo.path
        + fileInfo.name
        + fileInfo.extension
    )

    with Session(autoflush=False, bind=engine) as session:
        session.delete(fileInfo)
        session.commit()

    return "file has been deleted"


@app.route("/api/file-server/<int:id>", methods=["PATCH"])
@cross_origin()
def edit_file(id):
    content = request.get_json()

    fileInfo = FindFileInfoById(id)
    if fileInfo == None or SyncFileAbsence(fileInfo):
        return "not found", 404

    fullpath = (
        os.getcwd()
        + app.config["UPLOAD_FOLDER"]
        + fileInfo.path
        + fileInfo.name
        + fileInfo.extension
    )
    atime = os.path.getatime(fullpath)

    isModified = False
    modifiedPath = (
        os.getcwd()
        + app.config["UPLOAD_FOLDER"]
        + fileInfo.path
        + fileInfo.name
        + fileInfo.extension
    )

    if "name" in content and content["name"] != None and content["name"] != fileInfo.name:
        folder = os.getcwd() + app.config["UPLOAD_FOLDER"] + fileInfo.path
        oldName = folder + fileInfo.name + fileInfo.extension

        name = secure_filename(content["name"])
        newName = folder + name + fileInfo.extension
        while os.path.exists(newName):
            if not FindFileInfoByPath("/", name, fileInfo.extension):
                SyncFilePresence("/", name, fileInfo.extension)
            name += "_duplicate"
            newName = folder + name + fileInfo.extension
        os.rename(oldName, newName)

        # setctime(
        #     newName,
        #     calendar.timegm((fileInfo.created_at - timedelta(hours=3)).utctimetuple())
        #     + fileInfo.created_at.microsecond / 1000000.0,
        # )

        fileInfo.name = name
        with Session(autoflush=False, bind=engine) as session:
            session.add(fileInfo)
            session.commit()
        isModified = True
        modifiedPath = newName

    if "comment" in content and content["comment"] != None:
        fileInfo.comment = content["comment"]
        with Session(autoflush=False, bind=engine) as session:
            session.add(fileInfo)
            session.commit()
        isModified = True

    if isModified:
        now = datetime.now()

        utime = calendar.timegm((now - timedelta(hours=3)).utctimetuple())
        utime += now.microsecond / 1000000.0
        os.utime(modifiedPath, (atime, utime))

        fileInfo.updated_at = now
        with Session(autoflush=False, bind=engine) as session:
            session.add(fileInfo)
            session.commit()

            return jsonify(SerializeFileInfo(fileInfo))
