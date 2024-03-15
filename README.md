# Orbify
requirements:

1. docker
2. docker-compose
   
how to use:

1. remove "example" from .env.example file name, there are example environment variables there

2. In main folder run command:
docker-compose build
3. When build is done run by command:
docker-compose up

4. Make migracion
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"
docker-compose exec backend alembic upgrade head

5. To use the application, enter into your browser
http://localhost/docs#/

6. Shutdown
docker-compose down

7. how to test:
docker-compose run backend pytest -vv app/test.py



Useful commands for developers:
docker-compose exec db bash
psql -U <POSTGRES_USER> <POSTGRES_DB>
\dt
