FROM python:3.9-alpine

WORKDIR /code

ADD ./requirements.txt /code
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
