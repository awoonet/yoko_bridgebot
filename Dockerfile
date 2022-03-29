FROM python:3.9.7-slim-buster
RUN mkdir /app
WORKDIR /app
COPY ./pyrogram.txt .
RUN python3 -m pip install -r pyrogram.txt
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]
