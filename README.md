## Description

Example FAQ bot built on `dff`. Uses telegram as an interface.

This bot listens for user questions and finds similar questions in its database by using the `clips/mfaq` model.

It displays found questions as buttons. Upon pressing a button, the bot sends an answer to the question from the database.


An example of bot usage:

![image](https://user-images.githubusercontent.com/61429541/219064505-20e67950-cb88-4cff-afa5-7ce608e1282c.png)

## Setup database
```
conda install -y -c conda-forge postgresql
initdb -D finance_db
pg_ctl -D finance_db -l logfile start
createuser --encrypted --pwprompt __username__
createdb --owner=__username__ inner_finance_db

```
```
echo POSTGRES_USERNAME=******* >> .env
echo POSTGRES_PASSWORD=******* >> .env
echo POSTGRES_DB=******* >> .env
```




### Run with Docker & Docker-Compose environment
In order for the bot to work, set the bot token via [.env](.env.example). First step is creating your `.env` file:
```
echo TG_BOT_TOKEN=******* >> .env
```

Build the bot:
```commandline
docker-compose build
```
Testing the bot:
```commandline
docker-compose run bot pytest test.py
```

Running the bot:
```commandline
docker-compose run bot python run.py
```

Running in background
```commandline
docker-compose up -d
```
### Run with Python environment
In order for the bot to work, set the bot token, example is in [.env](.env.example). First step is setting environment variables:
```
export TG_BOT_TOKEN=*******
```

Build the bot:
```commandline
pip3 install -r requirements.txt
```
Testing the bot:
```commandline
pytest test.py
```

Running the bot:
```commandline
python run.py
```