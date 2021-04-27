FROM python:3.8-alpine
RUN apk --no-cache add ca-certificates
RUN apk add build-base
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b :5000 main:app