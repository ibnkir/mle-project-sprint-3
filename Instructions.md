## Инструкции по запуску микросервиса

### 0. Подготовка репозитория
- Перейти в домашнюю папку и склонировать репозиторий:
  ```
  cd ~
  git clone https://github.com/ibnkir/mle-project-sprint-3.git
  ```

- Загрузить файл `clean_data.csv` с исходными данными по [ссылке](https://disk.yandex.ru/d/OIInLdG4dZMVZA) и положить в папку `services/data/`. Эти данные понадобятся для генерации запросов.

- Загрузить файл с обученной моделью `flats_prices_fitted.pkl` 
по [ссылке](https://disk.yandex.ru/d/Q_PgLOBbwxGoJA) и положить в папку `services/models/`. 
Либо можно создать и обучить модель самостоятельно, выполнив все ячейки в ноутбуке 
`notebooks/model_preparation.ipynb`. 


### 1. FastAPI-микросервис в виртуальном окружении
- Перейти на терминале в корневую папку репозитория
    
- Установить необходимые библиотеки одним из двух способов:

    - Установка библиотек в текущем окружении:
      ```
      pip install -r requirements.txt
      ```

    - Установка библиотек в новом окружении:
      ```
      sudo apt-get update
      sudo apt-get install python3.10-venv
      python3 -m venv ./venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```

- Перейти на терминале в папку `services/`
    
- Запустить сервер uvicorn:
  ```
  uvicorn ml_service.fastapi_app:app --reload --port 1702 --host 0.0.0.0
  ```

- В браузере ввести адрес http://127.0.0.1:1702/docs для отправки запросов через Swagger UI
(при выборе post-запроса и нажатии на кнопку `Try it out` появится готовый тестовый пример с правильными параметрами) либо выполнить в терминале команду `curl 127.0.0.1:1702/` для отправки простого get-запроса.

- Если приложение запускалось в специально созданном виртуальном окружении, 
то по окончании работы его можно деактивировать командой
  ```
  deactivate
  ```

### 2. FastAPI-микросервис в Docker-контейнере
- Перейти на терминале в папку `services/`

- Собрать и запустить контейнер одним из двух способов:

    - Без использования Docker Compose:
      ```
      docker image build . --file Dockerfile_ml_service --tag proj_sprint3:ml_service
      docker container run --name ml_service --publish 4601:1702 --volume=./models:/price_app/models --env-file .env proj_sprint3:ml_service
      ```

    - С использованием Docker Compose:
      ```
      docker compose up --build
      ```

- Проверить работу сервиса одним из двух способов в зависимости от варианта запуска контейнера:

    - В случае запуска без использования Docker Compose:<br>
    В браузере ввести адрес http://127.0.0.1:4601/docs для отправки запросов через Swagger UI 
    (при выборе post-запроса и нажатии на кнопку `Try it out` появится готовый тестовый пример с правильными параметрами) либо выполнить в терминале команду `curl 127.0.0.1:4601/` для отправки простого get-запроса.

    - В случае запуска с использованием Docker Compose:<br>
    В браузере ввести адрес http://127.0.0.1:1702/docs для отправки запросов через Swagger UI 
    (при выборе post-запроса и нажатии на кнопку `Try it out` появится готовый тестовый пример с правильными параметрами) либо выполнить в терминале команду `curl 127.0.0.1:1702/` для отправки простого get-запроса.

- Остановить и удалить контейнер по окончании работы одним из двух способов
в зависимости от варианта запуска контейнера:

    - В случае запуска без использования Docker Compose:
      ```
      docker stop ml_service
      docker rm ml_service
      ```

    - В случае запуска с использованием Docker Compose:
      ```
      docker compose down
      ```

- Также при необходимости можно удалить и образ контейнера, выполнив следующие действия:
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

- Собрать и запустить контейнер в режиме Docker Compose 
(если образ был уже создан и сохранен, то параметр `--build` можно опустить):
  ```
  docker compose up --build
  ```
 
  После выполнения этой команды может возникнуть необходимость вручную удалить и снова добавить порт 9090 для сервиса Prometheus на вкладке перенаправления портов.

- Проверить работу всех запущенных сервисов можно, перейдя по ссылкам:
    - Swagger UI для тестирования основного сервиса предсказаний: http://localhost:1702/docs
    - Собираемые метрики основного сервиса: http://localhost:1702/metrics
    - Информация обо всех сборщиках: http://localhost:9090/targets
    - Prometheus UI для выполнения PromQL-запросов: http://localhost:9090
    - Сервис Grafana: http://localhost:3000

      Логин и пароль для входа в Grafana должны быть прописаны в файле `services/.env` 
      как переменные окружения с именами GRAFANA_USER и GRAFANA_PASS соответственно.
      Можно присвоить этим переменным свои собственные значения и вводить их при авторизации в Grafana. 

### 4. Построение дашборда для мониторинга
- Перейти в папку `services/`

- Собрать и запустить контейнер в режиме Docker Compose
(если образ был уже создан и сохранен, то параметр `--build` можно опустить):
  ```
  docker compose up --build
  ```
    
  После выполнения этой команды может возникнуть необходимость вручную удалить и снова добавить порт 9090 для сервиса Prometheus на вкладке перенаправления портов.

- Запустить один или несколько раз скрипт для генерации запросов:
  ```
  python generate_requests.py
  ```
      
- Перейти на страницу сервиса Grafana по ссылке http://localhost:3000, 
авторизоваться с логином и паролем, прописанными в файле `services/.env`.
После этого в левой панели в разделе `Connections->Data sources` выбрать источник данных Prometheus,
справа нажать кнопку `Add new data source`, 
чуть ниже ввести его url: `http://prometheus:9090`
и в самом низу страницы нажать кнопку `Save&test`. 
В конце перейти в окно url браузера, скопировать и сохранить код после самого последннего слэша.
Этот код понадобится при загрузке ранее сохраненного дашборда. 

- Открыть ранее сохраненный json-файл `dashboard.json`, например, в notepad 
и c помощью контекстного поиска и замены заменить все старые значения uid в словаре
{"datasorce": {"uid": <старое значение>}} на новое, после чего сохранить этот файл.

- Загрузить обновленный json-файл `dashboard.json` со схемой дашборда. Для этого в левой
панели выбрать раздел `Dashboards`, нажать кнопку `New` справа и в появившемся
контекстном меню выбрать нижний пункт `Import`. После этого перетащить json-файл в поле
`Upload dashboard JSON file` и нажать кнопку `Import`.
После этого откроется дашборд с данными, которые появились в Prometeus на данный момент.
