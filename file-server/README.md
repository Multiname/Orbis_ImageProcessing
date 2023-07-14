# Запуск приложения
Зависимости проекта хранятся в файле `requirements.txt`

Инициализация БД:
```
flask --app runner.py db init
flask --app runner.py db migrate
flask --app runner.py db upgrade
```

Запуск сервера производится командой `python runner.py`

Файлы, с которыми работает сервер и БД, хранятся в папке `server_files`

Для изменения этой директории необходимо указать нужный путь в `BaseConfig.UPLOAD_FODLER` в `config.py`, сохраняя формат `/path`

# Описание API
## api/file-server/
- Краткое описание: `получение информации по всем файлам`
- Метод: `GET`
- Формат запроса: `/`
- Формат ответа: `200`, `Массив JSON объектов, описывающих файлы`
```JSON
[
  {
    "id": 1,
    "name": "first_file",
    "extension": ".txt",
    "size": 8,
    "created_at": "2023-07-05 12:49:45.330076",
    "updated_at": null,
    "comment": null
  },
  {
    "id": 2,
    "name": "another_file",
    "extension": ".txt",
    "size": 12,
    "created_at": "2023-07-05 12:53:15.813008",
    "updated_at": null,
    "comment": "another file"
  }
]
```

## api/file-server/[id]
- Краткое описание: `получение информации о файле с указанным ID`
- Метод: `GET`
- Формат запроса: `ID строке запроса`

    `api/file-server/1`
- Формат ответа: 
    + `404`, `not found` - файл с указанным ID не найден
    + `200`, `JSON с информацией файла`
```JSON
{
  "id": 1,
  "name": "first_file",
  "extension": ".txt",
  "size": 8,
  "created_at": "2023-07-05 12:49:45.330076",
  "updated_at": null,
  "comment": null
}
```

## api/file-server/
- Краткое описание: `загрузка файла на сервер`
- Метод: `POST`
- Формат запроса:
    + Загружаемый файл в поле формы `file`
    + *Опционально*: комментарий в поле формы JSON `comment`
    + *Опционально*: имя файла в поле формы JSON `name`
- Формат ответа: 
    + `400`, `no file to load` - в поле формы `file` не указан загружаемый файл
    + `400`, `file already exists` - файл с таким именем уже существует
    + `200`, `JSON с информацией файла` - файл был успешно загружен
```JSON
{
  "id": 4,
  "name": "suddenly_not_file",
  "extension": ".txt",
  "size": 24,
  "created_at": "2023-07-05 12:55:31.792707",
  "updated_at": null,
  "comment": "mysterious file"
}
```

## api/file-server/[id]/download
- Краткое описание: `скачивание файла с указанным ID с сервера`
- Метод: `GET`
- Формат запроса: `ID файла в строке запроса`

    `api/file-server/1/download`
- Формат ответа: 
    + `404`, `not found` - файл с указанным ID не найден
    + `200`, `указанный файл`

## api/file-server/[id]
- Краткое описание: `удаление файла с указанным ID`
- Метод: `DELETE`
- Формат запроса: `ID файла в строке запроса`
    `api/file-server/1`
- Формат ответа: 
    + `404`, `not found` - файл с указанным ID не найден
    + `200`, `file has been deleted` - файл успешно удален

## api/file-server/[id]
- Краткое описание: `переименование или изменение комментраия файла`
- Метод: `PATCH`
- Формат запроса: `id` в строке запроса, поля `name` и `comment` опциональны
```JSON
{
  "name": "s_file",
  "comment": "changed file"
}
```
- Формат ответа: 
    + `404`, `not found` - файл с указанным ID не найден
    + `200`, `JSON с информацией файла` - файл был успешно изменен
```JSON
{
  "id": 4,
  "name": "s_file",
  "extension": ".txt",
  "size": 24,
  "created_at": "2023-07-05 12:55:31.792707",
  "updated_at": "2023-07-05 13:23:22.421002",
  "comment": "changed file"
}
```