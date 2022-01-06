FROM nikolaik/python-nodejs:python3.9-nodejs14-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY . ./

CMD [ "./scripts/deploy-template.sh" ]
