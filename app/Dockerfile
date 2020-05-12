FROM python:3.8

EXPOSE 5070


WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
#ADD . /app

CMD flask run --host=0.0.0.0 --port=5070