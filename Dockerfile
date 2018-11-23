FROM python:3
ADD . /myapp
WORKDIR /myapp
RUN pip install -r requirements.txt