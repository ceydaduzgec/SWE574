### How to use Docker

You can run the script with interactive docker terminal.
```bash
source tools/reun_development.sh
```
This will start the docker containers and you can access the project at `http://localhost:80/`

You can also run the project in the background by running the following command.
```bash
docker-compose up
```
If your container is already running you can also run the following command to enter the container:
```bash
source tools/exec.sh
```
or
```bash
docker-compose exec app bash
```

### Access Tables

First, you need to find out the container id:
```
docker ps
```
Then you can access the database with the following command:
```bash
docker exec -it <container_id> psql -U <username> -d <database_name> password
```
Then enter your database password.

Now you are inside the database and you can run the following SQL commands to get information you need.

If you ever need to delete your local database, you can run the following command, **BUT BE CAREFUL**, this will delete all your data:
```bash
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO <username>;
GRANT ALL ON SCHEMA public TO public;
````
