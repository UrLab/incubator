



# Install dependencies

* Running on Ubuntu :

```
sudo apt-get install python3-dev python3-setuptools libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python3-pip
sudo pip3 install virtualenv
```

* Running on Fedora

```
sudo dnf install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel python3-devel python3-setuptools python3-virtualenv
```


### Setup

```shell
python3 -m venv ve
source ve/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

### Configuration
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

You can fill the .env file with other stuff as well, i you wish to develop using a psotgres database, you can add these lines and modify them depending on your configuration :

```bash
export SQL_ENGINE=django.db.backends.postgresql
export SQL_DATABASE=<DBNAME>
export SQL_USER=<USERNAME>
export SQL_HOST=<HOST>
export SQL_PORT=<PORT>
```

## MQTT backend

    pip install paho-mqtt

## Create a user

    ./manage.py createsuperuser

## Adding requirements

To add a requirement, add it with no version constraint (or as little as needed)
to `requirements.in` (or `requirements-dev.in` or `requirements-prod.in` if it is needed only in prod or dev). Then run `pip-compile` (or `pip-compile requirements-dev.in` or `pip-compile requirements-prod.in`).

Never edit a `requirements-*.txt` file by hand !

In addition, we use [Dependabot](https://dependabot.com/) who will automatically submit Pull Requests to upgrade the python packages when a new version is available. This will only change the `requirement-*.txt`.
