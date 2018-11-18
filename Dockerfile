from python:3

WORKDIR /app

COPY ./app

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "app.py"]
