## Яндекс Практикум, курс "Инженер Машинного Обучения" (2024 г.)
## Проект 3-го спринта: "Релиз модели в продакшн"
### Выполнил: Кирилл Носов, email: ibnkir@yandex.ru

### Описание проекта
Целью проекта является создание и мониторинг микросервиса на базе FastAPI для получения предсказаний цен на квартиры по заданным параметрам пользователя. В качестве модели используется пайплайн из
трансформеров данных и регрессионной модели, разработанный в рамках проекта 2-го спринта. 

Инструменты:
- Visual Studio Code,
- FastAPI, 
- uvicorn,
- Docker и Docker Compose,
- Prometheus,
- Grafana.

### Результаты
__Этап 1. Написание FastAPI-микросервиса__<br>
- В папку `services/ml_service/` добавлены файлы `fastapi_app.py` и `fastapi_handler.py` с исходным кодом приложения.

__Этап 2. Контейнеризация микросервиса__<br>
- В папку `services/` добавлены конфигурационные файлы 
`Dockerfile_ml_service` и `docker-compose.yaml`.

__Этап 3. Запуск сервисов для системы мониторинга__<br>
- Добавлен конфигурационный файл prometheus.yml для сервиса Prometheus,
- В файл `docker-compose.yaml` добавлено описание сервисов Prometheus и Grafana,
- В исходный код FastAPI-сервиса добавлен экспортер метрик.

__Этап 4. Построение дашборда для мониторинга__<br>


### Структура репозитория
- `services/ml_service/fastapi_app.py` - исходный код для создания FastAPI-приложения,
- `services/ml_service/fastapi_handler.py` - исходный код для обработки запросов к сервису,
- `services/models/` - папка для сериализованной обученной модели 
(ее можно скачать по ссылке, приведенной в файле `Instructions.md`,
либо создать и обучить самостоятельно с помощью указанного ниже ноутбука), 
- `services/data/` - папка для исходных данных, необходимых для обучения модели, а также для
генерации большого количества запросов
(датасет можно загрузить из БД с помощью кода в ноутбуке либо скачать по ссылке, указанной в файле `Instructions.md`),
- `notebooks/model_preparation.ipynb` - тетрадка Jupyter Notebooks для скачивания исходных данных и обучения модели,
- `Instructions.md` - файл с инструкциями для каждого этапа,
- `requirements.txt` - библиотеки для работы в Jupyter Notebook и запуска сервиса без контейниризации,
- `services/requirements_ml_service.txt` - библиотеки для запуска в в контейнере,
- `services/generate_requests.py` - код для генерации запросов к основному сервису.
