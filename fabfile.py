from fabric.api import run, cd
from fabric.context_managers import prefix


def deploy():
    code_dir = '/home/www-data/incubator'
    with cd(code_dir), prefix('source ve/bin/activate'):
        run('sudo supervisorctl stop incubator')
        run("./save_db.sh")
        run("git pull")
        run("pip install -r requirements.txt --upgrade -q")
        run("./manage.py collectstatic --noinput -v 0")
        run("./manage.py makemigrations")
        run("./manage.py migrate")
        run('sudo supervisorctl start incubator')
