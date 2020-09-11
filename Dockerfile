FROM python:3.8.5-slim-buster

COPY ./api /api/api
COPY requirements.txt /requirements.txt

RUN apt-get update \
    && pip3 install -r requirements_prod.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/api
WORKDIR /api

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["api.main:app", "--host", "0.0.0.0","--port","8000"]
