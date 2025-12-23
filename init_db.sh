#!/usr/bin/env bash
set -euo pipefail

MYSQL_HOST=${MYSQL_HOST:-127.0.0.1}
MYSQL_PORT=${MYSQL_PORT:-3306}
MYSQL_USER=${MYSQL_USER:-app}
MYSQL_PASSWORD=${MYSQL_PASSWORD:-apppass}
MYSQL_DATABASE=${MYSQL_DATABASE:-decanat}

mysql_cmd() {
  mysql -h "${MYSQL_HOST}" -P "${MYSQL_PORT}" -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" "${MYSQL_DATABASE}"
}

echo "Applying schema.sql to ${MYSQL_DATABASE}..."
mysql_cmd < schema.sql

echo "Applying seed.sql to ${MYSQL_DATABASE}..."
mysql_cmd < seed.sql

echo "Done."
