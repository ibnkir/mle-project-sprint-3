# Инструкции по запуску микросервиса

### 0. Подготовка репозитория и модели
- Перейти в домашнюю папку и склонировать репозиторий на ваш компьютер, после чего перейти в папку проекта:
    ```bash
    cd ~
    git clone https://github.com/ibnkir/mle-project-sprint-3.git
    cd mle-project-sprint-3
    ```
- Загрузить модель по [ссылке](https://disk.yandex.ru/d/H57r_PT4oExSOA) и положить ее в папку 
`services/ml_service/models/` репозитория либо самостоятельно создать и обучить модель, выполнив все ячейки в ноутбуке `notebooks/model_preparation.ipynb`

### 1. FastAPI микросервис в виртуальном окружение
- Установить необходимые библиотеки в текущем либо новом виртуальном окружении, 
выполнив следующие команды в терминале из корневой папки репозитория:

Установка в текущем окружении:
    ```
    pip install -r requirements.txt
    ```
Установка в новом окружении:
    ```bash
    sudo apt-get update
    sudo apt-get install python3.10-venv
    python3 -m venv ./venv
    source venv/bin/activate 
    pip install -r requirements.txt
    ```
- Перейти в подпапку `services/ml_service/` проекта
   ```bash
   cd services/ml_service
   ```
- Запустить сервер uvicorn (если порт 8081 уже занят, то заменить его на другой)
   ```bash
   uvicorn fastapi_app:app --reload --port 8081 --host 0.0.0.0
   ```
- В браузере ввести адрес 127.0.0.1:8081/docs для выполнения post-запросов
либо выполнить команду в терминале для выполнения простого get-запроса
    ```
    curl 127.0.0.1:8081/
    ```

### 2. FastAPI микросервис в Docker-контейнере


### 3. Запуск сервисов для системы мониторинга

### 4. Построение дашборда для мониторинга