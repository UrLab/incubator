![SHAME](https://travis-ci.org/UrLab/incubator.svg?branch=master)
# incubator
Let's bootstrap a new incubator for UrLab ! (in python and with an API this time)

Quick brainstorming https://pad.lqdn.fr/p/incubator


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

* Running on Mac OS

```
brew install postgresql
```

### Setup

**Be careful as this may not work with python3.9 yet**

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

### Create a user

    ./manage.py createsuperuser

# View / Edit Notebooks

    ./manage.py shell_plus --notebook
