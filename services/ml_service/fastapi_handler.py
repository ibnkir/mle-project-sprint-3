"""Класс FastApiHandler для обработки запросов к FastAPI.

Чтобы протестировать этот файл без запуска uvicorn, нужно перейти в папку services
и выполнить команду: python -m ml_service.fastapi_handler
"""

import numpy as np
import pandas as pd
import joblib


class FastApiHandler:
    """Класс FastApiHandler, обрабатывает запросы и возвращает прогнозные цены квартир по заданным параметрам."""

    def __init__(self, model_path="./models/flats_prices_fitted_pipeline.pkl"):
        """Инициализация переменных класса."""

        # Типы параметров запроса для проверки
        self.param_types = {
            "model_params": dict
        }

        # Список необходимых параметров модели 
        self.required_model_params = [
            'floor', 'kitchen_area', 'living_area', 'rooms', 'is_apartment',
            'total_area', 'building_age', 'building_type_int', 
            'latitude', 'longitude', 'ceiling_height',
            'flats_count', 'floors_total', 'has_elevator'
        ]

        self.load_price_model(model_path=model_path)
        
    def load_price_model(self, model_path: str):
        """Загружаем обученную модель предсказания цен на квартиры.
        Args:
            - model_path (str): Путь до модели.
        """
        try:
            self.pipeline = joblib.load(model_path)
        except Exception as e:
            print(f"Failed to load model, {e}")
            self.pipeline = None

    def price_predict(self, model_params: dict) -> dict:
        """Предсказываем цену квартиры.

        Args:
            - model_params (dict): Параметры для модели.

        Returns:
            - dict: Словарь с прогнозной ценой.
        """
        model_params_df = pd.DataFrame(model_params, index=[0])
        try:
            y_pred = self.pipeline.predict(model_params_df)[0]
            response = {
                'status': 'OK',
                "score": y_pred 
            }
        except Exception as e:
            # Если отдельные признаки имеют неверный тип
            return {
                'status': 'Error',
                'message': f"Problem with some features, {e}"
            }
        else:
            return response

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора параметров.

        Args:
            - query_params (dict): Параметры запроса.

        Returns:
            - bool: True - если есть нужные параметры, False - иначе
        """
        if "model_params" not in query_params:
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора признаков.
        Args:
            - model_params (dict): Параметры пользователя для предсказания.
        Returns:
            - bool: True - если есть нужные параметры, False - иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    
    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.

        Args:
            - params (dict): Словарь параметров запроса.
            
        Returns:
            - dict: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
		
    def handle(self, params):
        """Функция для обработки FastAPI-запросов.
        Args:
            - params (dict): Словарь параметров запроса.
        Returns:
            - dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Проверяем, была ли загружена модель
            if not self.pipeline:
                response = {
                    'status': 'Error',
                    'message': "Model not found"
                }
            # Валидируем запрос к API
            elif not self.validate_params(params):
                response = {
                    'status': 'Error',
                    'message': "Problem with parameters"
                }
            else:
                model_params = params["model_params"]
                print("Making prediction...")
                # Пытаемся получить предсказание модели
                response = self.price_predict(model_params)
                    
        except Exception as e:
            return {
                'status': 'Error',
                'message': f'Problem with request, {e}'
            }
        else:
            return response


def main(model_path: str):
    # Создаём параметры для тестового запроса
    test_params = {
        'model_params': {
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
    }

    # Создаём обработчик запросов для API
    handler = FastApiHandler(model_path)

    # Делаем тестовый запрос
    #print(f"Searching {test_params['questions_num']} similar questions for text:\n{test_params['user_text']}\n")
    response = handler.handle(test_params)
    print(f"Response: {response}")


if __name__ == "__main__":
    """
    Для вызова main() без запуска uvicron нужно перейти в папку services/
    и выполнить команду: python -m ml_service.fastapi_handler
    """
    main('./models/flats_prices_fitted_pipeline.pkl')
    
    