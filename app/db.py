import mysql.connector
from mysql.connector import pooling
from flask import g

_pool = None


def init_pool(app):
    global _pool
    if _pool:
        return
    _pool = pooling.MySQLConnectionPool(
        pool_name="decanat_pool",
        pool_size=5,
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
        charset="utf8mb4",
    )


def get_db():
    if "db" not in g:
        if _pool is None:
            raise RuntimeError("DB pool is not initialized")
        g.db = _pool.get_connection()
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
