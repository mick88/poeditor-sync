FROM python:3.9

COPY poeditor_sync ./poeditor_sync
COPY setup.py ./

RUN python setup.py install
