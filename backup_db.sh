mkdir -p /home/incubator/dumps/$(date +"%y-%m")
docker compose -f /home/incubator/docker/apps/incubator/docker-compose.yml exec -T db pg_dumpall --username="incubator" > /home/incubator/dumps/$(date +"%y-%m")/$(date +"%y-%m-%d").sql
