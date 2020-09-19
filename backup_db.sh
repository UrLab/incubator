mkdir -p /home/incubator/dumps/$(date +"%y-%m-%d")
docker-compose -f /home/incubator/docker/app/incubator/docker-compose.yml exec db /usr/local/bin/pg_dump --dbname="incubator_db" --username="incubator" > /home/incubator/dumps/$(date +"%y-%m-%d")/incubator.dump
