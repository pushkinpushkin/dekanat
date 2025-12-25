# Учет успеваемости студентов (учебный мини-проект)

Простой учебный пример веб-приложения на Flask для работы деканата с учетом студентов, дисциплин, ведомостей и ролей. Проект рассчитан на демонстрацию базовых CRUD-операций, авторизации и ролей без ORM.

## Стек
- Python 3.11+
- Flask + Flask-Login
- MySQL 8 (через Docker)
- mysql-connector-python
- Jinja2 шаблоны
- python-dotenv для конфигурации из `.env`
- pypdf для PDF-генерации

## Роли и права
| Роль | Возможности |
| --- | --- |
| DB_ADMIN | Полный доступ, тех. администрирование |
| TEACHER | Только свои ведомости, оценки в статусе OPEN |
| DEANERY | Все ведомости, студенты, справки, выгрузки |
| DEPUTY_DEAN | Чтение всего, закрытие ведомостей (OPEN→CLOSED) |
| DEAN | Чтение всего, финальное закрытие (CLOSED→FINAL) |

## Структура проекта
```
app.py                  # точка входа
app/
  config.py             # загрузка настроек
  db.py                 # пул подключений MySQL
  permissions.py        # функции проверок ролей
  auth/                 # настройка Flask-Login
  routes/               # blueprints
  repositories/         # простые функции для SQL-запросов
  models/               # dataclass User
templates/              # Jinja2-шаблоны
static/style.css        # минимальный стиль
schema.sql              # схема БД
seed.sql                # демо-данные
.env.example            # образец переменных окружения
requirements.txt        # зависимости
```

## Схема БД (кратко)
- `users(id, username, password_hash, role, full_name, created_at)`
- `faculties`, `study_programs`, `groups` для иерархии обучения
- `students` с группой
- `courses` с привязкой к преподавателю
- `gradebooks` (дисциплина + группа + период + статус OPEN/CLOSED/FINAL)
- `grades` (оценки по студентам, уникальные в ведомости)

## Инициализация БД
Приложение не меняет БД автоматически при старте.

Ручная инициализация (например, для чистого запуска в проде):
1. Поднять MySQL через Docker: `docker compose up -d db`
2. Выполнить скрипт инициализации (использует переменные `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, по умолчанию значения из `.env.example`):  
   ```bash
   ./init_db.sh
   ```

## Запуск приложения (macOS)
1. Создать `.env` из `.env.example` и при необходимости скорректировать доступ к БД.
2. Создать виртуальное окружение и установить зависимости:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Запустить сервер (локально):
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```
   или через Dockerfile (при необходимости можно собрать простой образ на основе python:3.11).

## Docker Compose
- Сервис `db` поднимает MySQL 8.0 с volume `db_data` и плагином `mysql_native_password`.
- Приложение запускается локально (`flask run`) либо в отдельном контейнере при желании.

## Deploy на VPS (Docker Compose)
1. Скопировать переменные окружения: `cp .env.example .env` и обновить значения под продакшн (указать `MYSQL_HOST=db`, пароли и т. д.).
2. Запустить базу данных: `docker compose up -d db`.
3. Применить схему и демо-данные (использует локальный `mysql` CLI): `./init_db.sh`.
4. Поднять приложение (образ из `Dockerfile`, сервис `app` в Compose-файле): `docker compose up -d app`.
5. Настроить reverse proxy (например, Nginx/Caddy) на домен → внутренний адрес приложения (обычно `127.0.0.1:5000` или порт, проброшенный из контейнера `app`).

## Тестовые аккаунты
| Логин | Пароль | Роль |
| --- | --- | --- |
| admin | admin | DB_ADMIN |
| teacher1 | teacher1 | TEACHER |
| deanery | deanery | DEANERY |
| deputy | deputy | DEPUTY_DEAN |
| dean | dean | DEAN |

## Сценарий демонстрации
1. Войти как `teacher1` и открыть свои ведомости, изменить оценку в статусе OPEN.
2. Войти как `deanery` — добавить студента, дисциплину, назначить преподавателя, сформировать ведомость.
3. Войти как `deputy` — закрыть ведомость (OPEN→CLOSED).
4. Войти как `dean` — финализировать ведомость (CLOSED→FINAL).
5. Показать печать справки по студенту и загрузку PDF.

## PDF
- Встроенная генерация через pypdf: endpoint `/reports/transcript/<id>/pdf`.
- Можно также использовать печать страницы в PDF средствами браузера.

## Бэкап
- Полный дамп БД: `mysqldump -h 127.0.0.1 -u app -papppass decanat > backup.sql`

## Примечания
- Пароли хранятся в виде PBKDF2-хэшей (Werkzeug совместимый формат).
- Все SQL-запросы предельно просты для учебных целей.
