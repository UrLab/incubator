# builds latest commit from the current branch and deploys it

git pull
docker pull ghcr.io/urlab/incubator:main
docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
docker-compose restart nginx
