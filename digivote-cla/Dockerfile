FROM python:3.7.2

WORKDIR /usr/src/server

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD [ "python3", "./cla_server.py" ]