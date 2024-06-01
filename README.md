## Яндекс Практикум, курс "Инженер Машинного Обучения" (2024 г.)
### Проект 3-го спринта: "Релиз модели в продакшн"
### Выполнил: Кирилл Н., email: ibnkir@yandex.ru

#### Описание проекта:
Целью проекта является создание и мониторинг микросервиса на базе FastAPI для получения прогнозных цен на квартиры по заданным параметрам пользователя. В качестве модели используется пайплайн, разработанный в рамках 
проекта 2-го спринта. 

Инструменты:
- Visual Studio Code,
- FastAPI, 
- uvicorn,
- Docker и Docker Compose,
- Prometheus,
- Grafana.

#### Результаты:
- Этап 1. Написание FastAPI-микросервиса<br>
В папку `services/ml_service/` добавлены файлы `fastapi_handler.py` и `fastapi_app.py` с исходным кодом
для обработки запросов.
- Этап 2. Контейнеризация микросервиса<br>
- Этап 3. Запуск сервисов для системы мониторинга<br>
- Этап 4. Построение дашборда для мониторинга<br>


#### Структура репозитория:
- `services/ml_service/` - код FastAPI-приложения;
- `services/models/flats_prices_fitted_pipeline.pkl` - сериализованная обученная регрессионная модель-пайплайн
с трансформером для генерации новых признаков;
- `notebooks/model_preparation.ipynb` - тетрадка Jupyter Notebooks для обучения модели (готовую модель
можно также скачать по ссылке, приведенной в файле `Instructions.md`);
- `Instructions.md` - файл с описанием шагов и команд для выполнения каждого этапа.
