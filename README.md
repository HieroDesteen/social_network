# Social Network

### Production deploying
* Pull git repository:
```bash
git pull http://
```

* Enter work folder
```
cd test_app/
```
* Make docker-compose file
```bash
cp ./docker-compose.prod.yml.sample ./docker-compose.prod.yml
```

* Set environment variables in docker-compose.prod.yml file

Run command 
```dockerfile
docker-compose -f docker-compose.prod.yml -d --build
```

## Local deploying

* Make local environment
```bash
python3 -m venv env

source env/bin/activate
```
* Enter django project work folder
```bash
cd social_network/
```
* Install project requirements
```bash
pip install -r requrements.txt
```

* Migrate changes to db
```bash
    python3 manage.py migrate
```

* Run django server
```bash
    python3 manage.py runserver
```


## Notes

* For create admin 
```bash
    docker exec -it api python3 manage.py createsuperuser
```

* Check api container logs
```bash
    docker logs -f api
```
    

* Enter the api container with bash
```bash
    docker exec -it api bash
```
* Enter postgres db with psql
```bash
    docker exec -it api_db psql -U root test_db
```
# Automated bot

* Enter bot work folder
```bash
 cd automated_bot
```

* Make local environment
```bash
python3 -m venv env

source env/bin/activate
```

* Install bot requirements
```bash
    pip install -r requrements.txt
```

* Run bot

```bash
    python3 bot.py
```
