## Яндекс Практикум, курс "Инженер Машинного Обучения"
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
В папку `services/ml_service/` добавлены файлы `fastapi_app.py` и `fastapi_handler.py` с исходным кодом для создания приложения и обработки запросов соответственно. Обработчик проверяет параметры запроса и модели на соблюдение следующих условий:
- Наличие обязательного набора параметров,
- Значения всех параметров модели должны соответствовать заданным типам,
- Числовые параметры модели должны быть неотрицательными,
- Год постройки `build_year` должен быть меньше либо равен текущему году,
- Категориальный параметр `build_type_int` должен принимать целые значения от 0 до 6 включительно.


__Этап 2. Контейнеризация микросервиса__<br>
В папку `services/` добавлены конфигурационные файлы `Dockerfile_ml_service` и `docker-compose.yaml`, 
а также файл `requirements_ml_service.txt` с перечнем библиотек, устанавливаемых в контейнере.

__Этап 3. Запуск сервисов для системы мониторинга__<br>
- В папку `services/prometheus` добавлен конфигурационный файл `prometheus.yml` с описанием сборщиков сервиса Prometheus;
- В файл `docker-compose.yaml` добавлено описание сервисов Prometheus и Grafana;
- В исходный код основного сервиса добавлен экспортер метрик.

__Этап 4. Построение дашборда для мониторинга__<br>
- В исходный код основного сервиса добавлены метрики Prometheus,
включая гистограмму предсказаний и счетчик запросов с неправильными параметрами;
- Разработан скрипт `generate_requests.py` для генерации правильных и ошибочных запросов к основному сервису;
- В сервисе Grafana построен дашборд с 6 аналитическими панелями,
 в папке `services/` сохранены его JSON-файл `dashboard.json` и скриншот `dashboard.png`;
- В папку `services/` добавлен файл `Monitoring.md` с описанием использованных метрик и дашборда.


### Структура репозитория
- `Instructions.md` - файл с инструкциями для каждого этапа;
- `Monitoring.md` - файл с описанием выбранных метрик и дашборда;
- `requirements.txt` - библиотеки для обучения модели в Jupyter Notebook и запуска сервиса без контейнеризации;
- `notebooks/model_preparation.ipynb` - тетрадка Jupyter Notebooks для обучения модели;
- `services/data/` - папка для исходных данных, необходимых для обучения модели. Также они используются для генерации запросов к сервису. Датасет можно скачать по ссылке, указанной в файле `Instructions.md`;
- `services/models/` - папка для сериализованной обученной модели. Модель можно скачать по ссылке, приведенной в файле `Instructions.md`, либо создать и обучить самостоятельно с помощью указанного выше ноутбука;
- `services/.env` - файл с необходимыми переменными окружения;
- `services/requirements_ml_service.txt` - библиотеки для установки в контейнере;
- `services/Dockerfile_ml_service` - конфигурационный файл для контейнеризации основного сервиса;
- `services/docker-compose.yaml` - конфигурационный файл для контейнеризации всех сервисов в режиме Docker Compose;
- `services/prometheus/prometheus.yml` - конфигурационный файл для сервиса Prometheus с описанием сборщиков;
- `services/ml_service/fastapi_app.py` - исходный код для создания FastAPI-приложения;
- `services/ml_service/fastapi_handler.py` - исходный код для обработки запросов к приложению;
- `services/generate_requests.py` - скрипт для имитации нагрузки на основной сервис, генерирует
правильные и неправильные запросы. В первом случае данные берутся их исходного датасета;
- `services/dashboard.json` - json-файл с описанием дашборда, построенного в Grafana;
- `services/dashboard.png` - скриншот дашборда.
