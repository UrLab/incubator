CURRENT_MONTH=`date +%Y%m`
CURRENT_DATE=`date +%Y%m%d`
BACKUP_DIR=/home/$(USER)/dumps

# Create the backup file
mkdir -p /home/incubator/dumps/$(CURRENT_MONTH)

# Dump the database
docker-compose -f /home/incubator/docker/apps/incubator/docker-compose.yml exec db /usr/local/bin/pg_dump --dbname="incubator_db" --username="incubator" -f /backup.dump

# Compress medias
docker-compose -f /home/incubator/docker/apps/incubator/docker-compose.yml exec nginx /bin/bash -c "tar -czf /backup.tar.gz /home/app/web/media"

# Copy the backup files from docker
docker cp incubator_db_1:/backup.dump /home/incubator/dumps/$(CURRENT_MONTH)/$(CURRENT_DATE).dump
docker cp incubator_nginx_1:/backup.tar.gz /home/incubator/dumps/$(CURRENT_MONTH)/media_$(CURRENT_DATE).tar.gz

# Delete old backups (Keep for 90 days, all will be available on the second server)
find /home/incubator/dumps/ -type f -mtime +90 -exec rm {} \;

# Check if the SECONDARY_SERVER exists
if [ -z ${SECONDARY_SERVER_HOST+x} ];
then
    echo "SECONDARY_SERVER_HOST is unset, can't copy the backup to the secondary server";
    exit -1;
fi

# Copy the backup file to the secondary server
ssh $(SECONDARY_SERVER_HOST) "mkdir -p /home/incubator/dumps/$(CURRENT_MONTH)"
scp /home/incubator/dumps/$(CURRENT_MONTH)/$(CURRENT_DATE).dump $(SECONDARY_SERVER_HOST):/home/incubator/dumps/$(CURRENT_MONTH)/$(CURRENT_DATE).dump
scp /home/incubator/dumps/$(CURRENT_MONTH)/media_$(CURRENT_DATE).tar.gz $(SECONDARY_SERVER_HOST):/home/incubator/dumps/$(CURRENT_MONTH)/media_$(CURRENT_DATE).tar.gz