FROM python:rc-alpine

ADD . /bot
WORKDIR /bot

RUN pip install signalrcore
ENTRYPOINT ["python", "main.py"]
