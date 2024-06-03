"""FastAPI-приложение для предсказания цен на квартиры по заданным параметрам.

Для запуска перейти в папку services/ и выполнить команду:
uvicorn ml_service.fastapi_app:app --reload --port 1702 --host 0.0.0.0

либо, если работа ведется полностью локально:
uvicorn ml_service.fastapi_app:app --reload --port 1702 --host 127.0.0.1

Если используется другой порт, то заменить 1702 на этот порт.

Для просмотра документации API и совершения тестовых запросов через 
Swagger UI перейти в браузере по ссылке  http://127.0.0.1:1702/docs
"""

import uvicorn
from fastapi import FastAPI, Body
from .fastapi_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import (
    Histogram,
    Counter
)


# Создаём приложение FastAPI
app = FastAPI()

# Создаём обработчик запросов для API
app.handler = FastApiHandler()

# Инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

ml_service_predictions = Histogram(
    # имя метрики
    "ml_service_predictions",
    #описание метрики
    "Histogram of predictions",
    #указаываем корзины для гистограммы
    buckets=(0.5e7, 1.0e7, 1.5e7, 2.0e7)
)


@app.get("/")
def read_root():
    return {'message': 'Welcome from the FastAPI'}


@app.post("/predict") 
def get_prediction_for_item(
    model_params: dict = Body(
        example={
            'floor': 6,
            'kitchen_area': 8.5,
            'living_area': 30.0,
            'rooms': 2,
            'is_apartment': False,
            'total_area': 50.0,
            'building_age': 2024 - 1979,
            'building_type_int': 4,
            'latitude': 60.0,
            'longitude': 40.0,
            'ceiling_height': 2.5,
            'flats_count': 190,
            'floors_total': 12,
            'has_elevator': True
        } 
    )                                                   
):
    """Функция для предсказания цен на квартиры по заданным параметрам.

    Args:
        - params (dict): Параметры пользователя.

    Returns:
        - dict: Предсказание модели в формате JSON {"score":y_pred}
    """
    all_params = {
        "model_params": model_params
    }  
    
    response = app.handler.handle(all_params)
    
    if 'status' in response and response['status'] == 'OK':
        ml_service_predictions.observe(response['score'])

    return response


if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port="1702")