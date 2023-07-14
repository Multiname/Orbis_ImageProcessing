# Установка и запуск
Зависимости прооекта хранятся в файле `requirements.txt`

Конфигурация проекта хранится в файле `src/config/config.json`

Запуск `API`:
```CMD
cd src
python app.py
```
Запуск `worker`:
```CMD
cd src/scripts
python worker.py
```

# API
## GET /api/image-processing/
- Краткое описание: `получение информации по всем задачам`
- Формат ответа:
```JSON
[
    {
        "algorithm": "flip",
        "created_at": "2023-07-12 10:57:16.553720",
        "id": 12,
        "params": {
            "orientation": "horizontal"
        },
        "result_id": 32,
        "source_id": 26,
        "status": "finished",
        "updated_at": "2023-07-12 11:19:38.917447"
    },
    {
        "algorithm": "flip",
        "created_at": "2023-07-12 11:27:59.232721",
        "id": 13,
        "params": {
            "orientation": "horizontal"
        },
        "result_id": null,
        "source_id": 26,
        "status": "processing",
        "updated_at": "2023-07-12 11:28:13.284219"
    },
    {
        "algorithm": "flip",
        "created_at": "2023-07-12 11:31:10.043075",
        "id": 16,
        "params": {
            "orientation": "horizontal"
        },
        "result_id": null,
        "source_id": 26,
        "status": "error",
        "updated_at": "2023-07-12 11:31:13.738851"
    }
]
```
- Возможные ошибки:
    + `400`, `[X] field is missing` - в запросе отсутствует поле `X`
    + `400`, `specify at least one task` - пустой массив в поле `file_ids`
    + `400`, `[X] parameter is missing` - в поле `params` не указан параметр `X`

## POST /api/image-processing/
- Краткое описание: `запуск новой задачи`
- Формат запроса:
```JSON
{
    "file_ids": [1, 2, 3],
    "algorithm": "flip",
    "params": {
        "orientation": "horizontal"
    }
}
```
Алгоритмы и их параметры:
```JSON
"flip": {
    "orientation": [
        "horizontal",
        "vertical"
    ]
}

"resize": {
    "width": 100,
    "height": 100
}

"rotate": {
    "direction": [
        "clockwise",
        "counterclockwise"
    ]
}
```
- Формат ответа:
```JSON
{
    "task_ids": [
        23,
        24
    ]
}
```

## GET /api/image-processing/[id]
- Краткое описание: `получение информации о задаче`
- Формат запроса: `/api/image_processing/24`
- Формат ответа:
```JSON
{
    "algorithm": "rotate",
    "created_at": "2023-07-12 12:29:10.161752",
    "id": 24,
    "params": {
        "direction": "clockwise"
    },
    "result_id": 47,
    "source_id": 44,
    "status": "finished",
    "updated_at": "2023-07-12 12:38:51.596487"
}
```

## POST /api/image-processing/[id]/restart
- Краткое описание: `перезапуск задачи, имеющей статус "error"`
- Формат запроса: `/api/image_processing/24/restart`
- Формат ответа:
```JSON
{
    "algorithm": "rotate",
    "created_at": "2023-07-12 12:29:10.161752",
    "id": 24,
    "params": {
        "direction": "clockwise"
    },
    "result_id": 47,
    "source_id": 44,
    "status": "pending",
    "updated_at": "2023-07-12 12:38:51.596487"
}
```
- Возможные ошибки:
    + `405`, `task hasn't failed` - задача не имеет статус `error`