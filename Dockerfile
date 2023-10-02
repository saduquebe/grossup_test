FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
#ENV DJANGO_SETTINGS_MODULE my_django_project.settings

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 3100

COPY . /code

CMD ["python", "manage.py", "runserver", "0.0.0.0:3100"]