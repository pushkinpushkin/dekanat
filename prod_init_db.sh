#!/usr/bin/env bash
set -euo pipefail

COMPOSE_SERVICE_DB=${COMPOSE_SERVICE_DB:-db}

MYSQL_USER=${MYSQL_USER:-app}
MYSQL_PASSWORD=${MYSQL_PASSWORD:-apppass}
MYSQL_DATABASE=${MYSQL_DATABASE:-decanat}

# Опционально: если хочешь выполнять от root (например, если schema требует привилегий)
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_FILE="${SCRIPT_DIR}/schema.sql"
SEED_FILE="${SCRIPT_DIR}/seed.sql"

if [[ ! -f "${SCHEMA_FILE}" ]]; then
  echo "ERROR: schema.sql not found at ${SCHEMA_FILE}" >&2
  exit 1
fi

if [[ ! -f "${SEED_FILE}" ]]; then
  echo "ERROR: seed.sql not found at ${SEED_FILE}" >&2
  exit 1
fi

echo "Waiting for MySQL container '${COMPOSE_SERVICE_DB}' to be ready..."
# Ждём ping, чтобы не ловить race condition при первом старте
for i in {1..60}; do
  if docker compose exec -T "${COMPOSE_SERVICE_DB}" mysqladmin ping -h 127.0.0.1 --silent >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

if ! docker compose exec -T "${COMPOSE_SERVICE_DB}" mysqladmin ping -h 127.0.0.1 --silent >/dev/null 2>&1; then
  echo "ERROR: MySQL is not ready after waiting." >&2
  docker compose logs --tail=200 "${COMPOSE_SERVICE_DB}" || true
  exit 1
fi

# Выбираем пользователя: root (если задан MYSQL_ROOT_PASSWORD), иначе app-user
if [[ -n "${MYSQL_ROOT_PASSWORD}" ]]; then
  MYSQL_EXEC=(docker compose exec -T "${COMPOSE_SERVICE_DB}" mysql -uroot -p"${MYSQL_ROOT_PASSWORD}")
else
  MYSQL_EXEC=(docker compose exec -T "${COMPOSE_SERVICE_DB}" mysql -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}")
fi

echo "Applying schema.sql to ${MYSQL_DATABASE}..."
"${MYSQL_EXEC[@]}" "${MYSQL_DATABASE}" < "${SCHEMA_FILE}"

echo "Applying seed.sql to ${MYSQL_DATABASE}..."
"${MYSQL_EXEC[@]}" "${MYSQL_DATABASE}" < "${SEED_FILE}"

echo "Done."
