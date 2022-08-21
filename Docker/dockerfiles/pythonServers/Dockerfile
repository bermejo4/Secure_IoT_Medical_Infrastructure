# Start from python:3.8-alpine base image
FROM python:3


COPY /dockerfiles/pythonServers/requirements.txt requirements.txt
COPY /dockerfiles/pythonServers/Proxy_Server.py Proxy_Server.py
COPY /dockerfiles/pythonServers/AesPythonServerToMQTT.py AesPythonServerToMQTT.py
COPY /dockerfiles/pythonServers/DEVICES_KEYS.txt DEVICES_KEYS.txt 

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 9998

CMD [ "python3", "Proxy_Server.py" ]