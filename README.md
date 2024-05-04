# Telegram bot with AI

<p align="center" width="100%">
    <img width="100%" src="images/image.jpg">
</p>

<div align="center">
    
  <a href="https://github.com/itmo-bootcamp/itmo-bootcamp-2023/issues">![GitHub issues](https://img.shields.io/github/issues//BorisovMaksim/FinanceBot)</a>
  <a href="https://github.com/itmo-bootcamp/itmo-bootcamp-2023/blob/master/LICENSE">![GitHub license](https://img.shields.io/github/license/BorisovMaksim/FinanceBot?color=purple)</a>
  <a href="https://www.python.org/dev/peps/pep-0008/">![Code style](https://img.shields.io/badge/code%20style-pep8-orange.svg)</a>

</div>

## Stack
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/Vladimir-Dimitrov-Ngu)
[![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)](https://github.com/Vladimir-Dimitrov-Ngu)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Vladimir-Dimitrov-Ngu)
[![Docker](https://img.shields.io/badge/-Docker-090909?style=for-the-badge&logo=Docker)]([https://hub.docker.com/u/mbaushenko](https://github.com/Vladimir-Dimitrov-Ngu)https://github.com/Vladimir-Dimitrov-Ngu)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](https://github.com/Vladimir-Dimitrov-Ngu)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://github.com/Vladimir-Dimitrov-Ngu)

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
echo POSTGRES_USERNAME=******* >> bot/.env
echo POSTGRES_PASSWORD=******* >> bot/.env
echo POSTGRES_DB=******* >> bot/.env
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
export TINKOFF_TOKEN==*******
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

## Contribution

Read CONTRIBUTING.md

## Author

Vladimir Dimitrov