"""Вспомогательный файл для генерации запросов к предсказательному сервису ml_service.
Данные для запросов берутся из исходного датасета services/data/clean_data.csv

Для исполнения кода в этом файле нужно запустить сервис ml_service любым из возможных способов, 
затем перейти в терминале в папку services/ и ввести команду:
python generate_requests.py
"""

import numpy as np
import pandas as pd
import requests
import time
import json


# Кол-во правильных запросов
CORRECT_REQ_NUM = 5

# Кол-во ошибочных запросов
ERR_REQ_NUM = 2

# Список обязательных параметров для передачи в модель
required_model_params = [
    'floor', 
    'kitchen_area', 
    'living_area', 
    'rooms', 
    'is_apartment',
    'total_area', 
    'build_year', 
    'building_type_int', 
    'latitude', 
    'longitude', 
    'ceiling_height',
    'flats_count', 
    'floors_total', 
    'has_elevator'
]

required_model_params_ = {
    'floor':[int], 
    'kitchen_area':[float, int], 
    'living_area': [float, int], 
    'rooms': [int], 
    'is_apartment': [bool],
    'total_area': [float, int], 
    'build_year': [int], 
    'building_type_int': [int], 
    'latitude': [float, int], 
    'longitude': [float, int], 
    'ceiling_height': [float, int],
    'flats_count': [int], 
    'floors_total': [int], 
    'has_elevator': [bool]
}

# Загружаем исходный датасет
clean_data = pd.read_csv('./data/clean_data.csv')

# Генерируем правильные запросы
selected_inds = np.random.choice(np.arange(len(clean_data)), size=CORRECT_REQ_NUM, replace=False)
for cnt, idx in enumerate(selected_inds):
    model_params_df = clean_data.loc[clean_data.index==idx, required_model_params]
    model_params_dict = model_params_df.to_dict(orient='records')[0]
    try:
        print(f"Sending correct request {cnt + 1}/{CORRECT_REQ_NUM}...")
        response = requests.post(url='http://localhost:1702/predict', json=model_params_dict)  
        response = response.json()
        print(response)
    except Exception as e:
        print(f'{e}')
        break

print()
# Генерируем неправильные запросы
for cnt in range(ERR_REQ_NUM):
    try:
        print(f"Sending wrong request {cnt + 1}/{ERR_REQ_NUM}...")
        response = requests.post(url='http://localhost:1702/predict', json={})  
        response = response.json()
        print(response)
        time.sleep(5)
    except Exception as e:
        print(f'{e}')
        break
