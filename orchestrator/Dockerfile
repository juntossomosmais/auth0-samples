FROM python:3.9.7-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY . ./

CMD [ "python", "manage.py" ]
