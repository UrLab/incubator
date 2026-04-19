#!/bin/bash
set -euo pipefail

# ============================================================
# PostgreSQL 12 → 17 migration script
#
# Strategy: dump from old container, restore into new container.
# pg_upgrade requires both binaries on the same host, which is
# awkward with Docker. dump/restore is simpler and safer.
#
# Prerequisites:
#   - docker compose services are currently running with postgres:12
#   - .env.db contains POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
#
# Usage:
#   chmod +x upgrade_postgres.sh
#   ./upgrade_postgres.sh
# ============================================================

COMPOSE_FILE="docker-compose.yml"
DUMP_FILE="pg12_dump_$(date +%Y%m%d_%H%M%S).sql"

echo "=== PostgreSQL 12 → 17 Migration ==="
echo ""

# --- Step 1: Source DB credentials ---
if [ ! -f .env.db ]; then
    echo "ERROR: .env.db not found. Cannot read DB credentials."
    exit 1
fi
source .env.db
DB_NAME="${POSTGRES_DB:-incubator_db}"
DB_USER="${POSTGRES_USER:-incubator}"

echo "[1/6] Dumping database from PostgreSQL 12..."
docker-compose exec -T db pg_dumpall -U "$DB_USER" > "$DUMP_FILE"
DUMP_SIZE=$(du -h "$DUMP_FILE" | cut -f1)
echo "       Dump complete: $DUMP_FILE ($DUMP_SIZE)"

echo "[2/6] Stopping all services..."
docker-compose down

echo "[3/6] Backing up old postgres volume..."
# Create a backup of the volume just in case
docker volume create incubator_postgres_data_backup 2>/dev/null || true
docker run --rm \
    -v incubator_postgres_data:/source:ro \
    -v incubator_postgres_data_backup:/backup \
    alpine sh -c "cd /source && tar cf - . | (cd /backup && tar xf -)"
echo "       Volume backed up to incubator_postgres_data_backup"

echo "[4/6] Removing old postgres data volume..."
docker volume rm incubator_postgres_data

echo "[5/6] Starting fresh PostgreSQL 17..."
docker-compose up -d db
echo "       Waiting for PostgreSQL 17 to be ready..."
sleep 5
# Wait until pg_isready succeeds
for i in $(seq 1 30); do
    if docker-compose exec -T db pg_isready -U "$DB_USER" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

echo "[6/6] Restoring dump into PostgreSQL 17..."
docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" < "$DUMP_FILE"

# Re-set the password so it's hashed with scram-sha-256 (Postgres 17 default).
# Old Postgres 12 stored passwords as md5, which won't work for TCP connections.
echo "       Re-hashing password for scram-sha-256 compatibility..."
DB_PASS="${POSTGRES_PASSWORD:-}"
if [ -n "$DB_PASS" ]; then
    docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" \
        -c "ALTER USER $DB_USER PASSWORD '$DB_PASS';"
fi

echo ""
echo "=== Migration complete! ==="
echo ""
echo "Starting all services..."
docker-compose up -d

echo "Running Django migrations..."
sleep 5
docker-compose exec -T web uv run python manage.py migrate --noinput

echo ""
echo "Verify with: docker compose exec db psql -U $DB_USER -d $DB_NAME -c 'SELECT version();'"
echo ""
echo "Once verified, you can clean up:"
echo "  rm $DUMP_FILE"
echo "  docker volume rm incubator_postgres_data_backup"
