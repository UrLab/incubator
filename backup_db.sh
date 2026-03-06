mkdir -p /home/incubator/dumps/$(date +"%y-%m")
docker compose -f /home/incubator/docker/apps/incubator/docker-compose.yml exec -T db pg_dump --username="incubator" --dbname="incubator_db" > /home/incubator/dumps/$(date +"%y-%m")/$(date +"%y-%m-%d").sql
