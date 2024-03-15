# Orbify
requirements:

1. docker
2. docker-compose
   
how to use:

1. In main folder run command:
docker-compose build
2. When build is done run by command:
docker-compose up

3. Make migracion
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"
docker-compose exec backend alembic upgrade head

4. To use the application, enter into your browser
http://localhost/docs#/

5. Shutdown
docker-compose down

6. how to test:
docker-compose up
docker-compose run backend pytest -vv app/test.py



Useful commands for developers:
docker-compose exec db bash
psql -U <POSTGRES_USER> <POSTGRES_DB>
\dt
