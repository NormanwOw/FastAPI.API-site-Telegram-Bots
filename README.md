# API site Telegram-Bots

![](https://img.shields.io/badge/Python-v3.11-green) ![](https://img.shields.io/badge/FastAPI-v0.104.1-blue) 
![](https://img.shields.io/badge/SQLAlchemy-v2.0-yellow) ![](https://img.shields.io/badge/PostgreSQL-v16-blue) 
![](https://img.shields.io/badge/Redis-v5.0-red) ![](https://img.shields.io/badge/Celery-v5.3-green) 
![](https://img.shields.io/badge/Flower-v2.0-red) ![](https://img.shields.io/badge/Alembic-v2.0-violet) 
![](https://img.shields.io/badge/Docker-blue)  
Actual version running [here](http://195.54.178.243:21722/api/v1/docs)
## About
API for site Telegram-bots with Database, Cache and Task manager 
## Install
1. Edit file .env-non-dev
   * `SMTP_USER`
   * `SMTP_PASSWORD`
   * `SMTP_HOST`
   * `SMTP_PORT`  
     Information about getting started with **SMTP gmail** you can find [here](https://mailmeteor.com/blog/gmail-smtp-settings) 
   * `SECRET` - random string
   * `SECRET_AUTH` - random string
     
2. `$ docker-compose up -d`
3. `$ docker-compose exec db psql -U postgres -f /setup/data.dump`

Interactive documentation will be here: `127.0.0.1:8000/api/v1/docs`  
Task manager: `127.0.0.1:8888`
___
![api-page](https://github.com/NormanwOw/FastAPI.API-site-Telegram-Bots/assets/118648914/920f5e90-5a53-43a8-95f4-ae437d618000)


