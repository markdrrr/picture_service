FROM python:latest

WORKDIR /src
COPY . /src

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "migrate"]