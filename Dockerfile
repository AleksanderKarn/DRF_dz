FROM python:3

WORKDIR /code

RUN pip install django
RUN pip install djangorestframework
RUN pip install psycopg2-binary
RUN pip install celery
RUN pip install django-celery-beat
RUN pip install python-dotenv
RUN pip install djangorestframework-simplejwt
RUN pip install drf-yasg
RUN pip install pillow

COPY . .

CMD python manage.py runserver 0.0.0.0:8000


