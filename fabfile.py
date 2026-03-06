from fabric.api import run, cd


def deploy():
    code_dir = "/home/www-data/incubator"
    with cd(code_dir):
        run("sudo supervisorctl stop incubator")
        run("./save_db.sh")
        run("git pull")
        run("uv sync --frozen")
        run("uv run ./manage.py collectstatic --noinput -v 0")
        run("uv run ./manage.py makemigrations")
        run("uv run ./manage.py migrate")
        run("sudo supervisorctl start incubator")
