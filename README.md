# DRF_dz
Создаём контейнер с Python с доступом к нашей папке с проектом командой :
docker run -it --network host -v /User/projects/DRF_1:/app python bash
ставим все необходимые пакеты:
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install celery
pip install django-celery-beat
pip install python-dotenv
pip install djangorestframework-simplejwt
pip install drf-yasg
pip install pilliw
2. Создаем контейнер с базой данных Postgressql и соединяем ее с локальным сервером по порту 5432 командой, так же создаем
папку postgres_data на локальной машине для хранения данных из БД в фоновом режиме :
docker run --name db_django2 -p 5432:5432 -v /home/netsh/docker/postgres_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=public
-e POSTGRES_HOST_AUTH_METHOD=md5 -d postgres
