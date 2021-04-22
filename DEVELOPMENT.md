# Developer quickstart

## Setup your machine

The setup you need wildly depends on the OS you are running.
Here are instructions for some common OSes.

<details>
 <summary>Ubuntu (or Mint)</summary>
 
 ```shell
 sudo apt-get install python3-dev python3-setuptools python3-pip
 sudo pip3 install virtualenv
 ```
 
</details>

<details>
 <summary>Fedora</summary>
 
 ```shell
 sudo dnf install python3-devel python3-setuptools python3-virtualenv
 ```
 
</details>

<details>
 <summary>MacOS</summary>
 
 ```shell
 brew install python3
 pip3 install virtualenv 
 ```
 
</details>

## Get the code
```shell
git clone git@github.com:UrLab/incubator.git
cd incubator
```

## Initial setup
Now that you have the code we have to install the required Python dependencies.

We will use a virtualenv for this purpose. This allows us to install specific versions of the package for the incubator and avoid messing up with your system packages. If you don't know what is a virtualenv, it might be good to google it a bit or ask about it to members of the hackerspace, they will be happy to help.

```shell
python3 -m venv ve
source ve/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

The last step is to create an empty database with the correct structure.
```shell
./manage.py migrate
```

## Run the web server
Now that you are set up, you can fire up the Django web server:
```shell
./manage.py runserver
```

 And have a look at your local instance on [localhost:8000](http://localhost:8000)


## Next time
The next time you want to work on this code, you don't have to repeat the whole list of commands we just typed. You only have to activate the virtualenv (you have to activate it once for every new shell you open)

```shell
source ve/bin/activate
```

And then start the server
```shell
./manage.py runserver
```

# How to ?

## Create a admin user

You might need to create a user with admin rights on your local instance. Just run this command:

```shell
./manage.py createsuperuser
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
    pip install paho-mqtt
```


## Adding new requirements

To add a requirement, add it with no version constraint (or as little as needed)
to `requirements.in` (or `requirements-dev.in` or `requirements-prod.in` if it is needed only in prod or dev). Then run `pip-compile` (or `pip-compile requirements-dev.in` or `pip-compile requirements-prod.in`).

Never edit a `requirements-*.txt` file by hand !

In addition, we use [Dependabot](https://dependabot.com/) who will automatically submit Pull Requests to upgrade the python packages when a new version is available. This will only change the `requirement-*.txt`.
