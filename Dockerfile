FROM python:3.8.2-alpine3.11

RUN apk add --no-cache curl bash openssl gcc g++ python3-dev linux-headers
RUN apk add --no-cache libressl-dev musl-dev libffi-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "run.py"]
