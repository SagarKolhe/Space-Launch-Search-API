FROM python:3.7

EXPOSE 5000

WORKDIR /spaceflightnews

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/main.py"]
