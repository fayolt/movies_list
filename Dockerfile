FROM python:3.6-slim-buster
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT /app/entrypoint.sh