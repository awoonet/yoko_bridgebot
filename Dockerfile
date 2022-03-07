FROM python:3.9.10-slim-buster
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]
