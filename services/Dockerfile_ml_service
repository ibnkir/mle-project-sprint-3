FROM python:3.11-slim

COPY . ./price_app

WORKDIR price_app

RUN pip3 install -r requirements.txt

EXPOSE ${ML_SERVICE_PORT}

VOLUME /models

CMD uvicorn ml_service.fastapi_app:app --reload --port ${ML_SERVICE_PORT} --host  0.0.0.0