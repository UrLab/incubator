![SHAME](https://travis-ci.org/UrLab/incubator.svg?branch=master)
# incubator
Let's bootstrap a new incubator for UrLab ! (in python and with an API this time)

Quick brainstorming https://pad.lqdn.fr/p/incubator


# Install dependencies
    
  - Running on Ubuntu
  
  ``sudo apt-get install python3-dev python3-setuptools libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python3-pip
sudo pip3 install virtualenv``
    
  - Running on Fedora 
  
  ```sudo dnf install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel python3-devel python3-setuptools python3-virtualenv```

#### Setup

    virtualenv -p python3 ve3 # or virtualenv-3 -p python3 ve3
    source ve3/bin/activate
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver

### Create a user

    ./manage.py createsuperuser
    
## Docker
Install the incubator in a container via docker

    docker build -t incubator .
    docker run --name incubatorfromspace -p 8000:8000 -d incubator
    
Admin : poney/poney, admin/admin, 
    
# View / Edit Notebooks

    ./manage.py shell_plus --notebook


