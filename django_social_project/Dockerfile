FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN pwd
RUN ls -al
RUN python manage.py makemigrations
RUN python manage.py migrate

