# Developer quickstart

## Setup your machine

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Get the code
```shell
git clone git@github.com:UrLab/incubator.git
cd incubator
```

## Initial setup
Install dependencies (uv will automatically create a virtual environment):

```shell
uv sync --group dev
```

The last step is to create an empty database with the correct structure.
```shell
uv run ./manage.py migrate
```

## Run the web server
Now that you are set up, you can fire up the Django web server:
```shell
uv run ./manage.py runserver
```

 And have a look at your local instance on [localhost:8000](http://localhost:8000)


## Next time
The next time you want to work on this code, just start the server:

```shell
uv run ./manage.py runserver
```

# How to ?

## Create a admin user

You might need to create a user with admin rights on your local instance. Just run this command:

```shell
uv run ./manage.py createsuperuser
```

## Change the configuration
You may configure your local instance by writing a `.env` file containing environment variables.

```bash
# Env vars. Change the Value by what you want
export DEBUG=1
export FAKE_REDIS=1
export EMAIL_HOST=smtp.tonserver
export EMAIL_PORT=25
```

Then by sourcing this file in the shells where you want to run Django.

```shell
source .env
```

You can fill the .env file with other stuff as well, i you wish to develop using a Postgres database (by default, you use SQLite), you can add these lines and modify them depending on your configuration :

```bash
export SQL_ENGINE=django.db.backends.postgresql
export SQL_DATABASE=<DBNAME>
export SQL_USER=<USERNAME>
export SQL_HOST=<HOST>
export SQL_PORT=<PORT>
```

## MQTT backend
```shell
    uv add paho-mqtt
```


## Adding new requirements

To add a new dependency, use:

```shell
uv add <dependency>
```

For dev-only or prod-only dependencies, use the `--group` flag:

```shell
uv add --group dev <dependency>
uv add --group prod <dependency>
```

This will update both `pyproject.toml` and `uv.lock` automatically. Never edit `uv.lock` by hand!
