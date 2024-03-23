FROM python:3.11

COPY poeditor_sync ./poeditor_sync
COPY setup.py ./

RUN python setup.py install
