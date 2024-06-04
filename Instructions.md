## Инструкции по запуску микросервиса

### 0. Подготовка репозитория и модели
- Перейти в домашнюю папку, склонировать репозиторий и перейти в него с помощью следующего набора команд:
    ```bash
    cd ~
    git clone https://github.com/ibnkir/mle-project-sprint-3.git
    cd mle-project-sprint-3
    ```

- Загрузить файл `clean_data.csv` с исходными данными по [ссылке](https://disk.yandex.ru/d/OIInLdG4dZMVZA) и положить в папку `services/data/`. Эти данные понадобятся для генерации запросов.

- Загрузить файл с обученной моделью `flats_prices_fitted.pkl` 
по [ссылке](https://disk.yandex.ru/d/Ce6MX9OaWiyOKA) и положить в папку `services/models/`. 
Либо можно создать и обучить модель самостоятельно, выполнив все ячейки в ноутбуке 
`notebooks/model_preparation.ipynb`. 


### 1. FastAPI-микросервис в виртуальном окружении
- Установить необходимые библиотеки одним из двух способов:

    - Установка библиотек в текущем окружении:<br>
        `pip install -r requirements.txt`

    - Установка библиотек в новом окружении:<br>
        `sudo apt-get update`<br>
        `sudo apt-get install python3.10-venv`<br>
        `python3 -m venv ./venv`<br>
        `source venv/bin/activate`<br> 
        `pip install -r requirements.txt`

- Перейти в папку `services/`

- Запустить сервер uvicorn (если порт 1702 уже занят, то заменить его на другой):
   ```bash
   uvicorn ml_service.fastapi_app:app --reload --port 1702 --host 0.0.0.0
   ```

- В браузере ввести адрес http://127.0.0.1:1702/docs для отправки post-запросов через Swagger UI
(при нажатии на кнопку `Try it out` появится готовый тестовый пример с правильными параметрами модели) либо выполнить в терминале команду ```curl 127.0.0.1:1702/``` для отправки простого get-запроса.

### 2. FastAPI-микросервис в Docker-контейнере
- Перейти в папку `services/`

- Собрать и запустить контейнер одним из двух способов:

    - Без использования Docker Compose:<br>
    ```bash
    docker image build . --file Dockerfile_ml_service --tag proj_sprint3:ml_service
    
    docker container run --name ml_service --publish 4601:1702 --volume=./models:/price_app/models --env-file .env proj_sprint3:ml_service
    ```

    - С использованием Docker Compose:<br>
    ```bash
    docker compose up --build
    ```

- В браузере ввести адрес http://127.0.0.1:4601/docs для отправки post-запросов через Swagger UI (при нажатии на кнопку `Try it out` появится готовый тестовый пример с правильными параметрами модели) либо выполнить в терминале команду `curl 127.0.0.1:4601/` для отправки простого get-запроса.

- Остановить и удалить контейнер по окончании работы одним из двух способов
в зависимости от варианта запуска контейнера:

    - В случае запуска без использования Docker Compose:<br>
    ```
    docker stop ml_service
    docker rm ml_service
    ```

    - В случае запуска с использованием Docker Compose:<br>
    ```
    docker compose down
    ```

- Также при необходимости можно удалить образ, выполнив следующие действия:
    - Находим ID образа
    ```
    docker images
    ```
    
    - Удаляем образ по найденному ID
    ```
    docker rmi -f <id вашего образа>
    ```

### 3. Запуск сервисов для системы мониторинга
- Перейти в папку `services/`
- Собрать и запустить контейнер (если образ уже создан, то параметр `--build` можно опустить):<br>
    `docker compose up --build`
    
    После выполнения этой команды может возникнуть необходимость вручную удалить и снова добавить порт 9090 для сервиса Prometheus на вкладке перенаправления портов.

- Проверить работу всех запущенных сервисов, перейдя по ссылкам:
    - Swagger UI для тестирования основного сервиса предсказаний: http://localhost:1702/docs
    - Собираемые метрики основного сервиса: http://localhost:1702/metrics
    - Информация обо всех сборщиках: http://localhost:9090/targets
    - Prometheus UI для выполнения PromQL-запросов: http://localhost:9090
    - Сервис Grafana: http://localhost:3000

    Логин и пароль для входа в Grafana должны быть прописаны в файле `services/.env` 
    как переменные с именами GRAFANA_USER и GRAFANA_PASS соответственно.

### 4. Построение дашборда для мониторинга
- Перейти в папку `services/`
- Собрать и запустить контейнер (если образ уже создан, то параметр `--build` можно опустить):<br>
    `docker compose up --build`
    
    После выполнения этой команды может возникнуть необходимость вручную удалить и снова добавить порт 9090 для сервиса Prometheus на вкладке перенаправления портов.

- Запустить скрипт для генерации запросов:
    `python generate_requests.py`
    
- Перейти на страницу сервиса Grafana по ссылке http://localhost:3000, 
в левой панели в разделе `Connections->Data sources` выбрать источник данных Prometheus
и указать его url в сети Docker: http://prometheus:9090, внизу страницы нажать кнопку `Save&test`

- Загрузить json-файл с дашбордом `dashboard.json`

