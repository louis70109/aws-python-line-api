import psycopg2
import psycopg2.extras
import os


class Database():
    conns = []

    def __enter__(self):
        return self

    def connect(self):
        conn = psycopg2.connect(
            database=os.environ("PG_DB"),
            user=os.environ("PG_NAME"),
            password=os.environ("PG_PWD"),
            host=os.environ("PG_HOST"),
            port=os.environ("PG_PORT")
        )
        self.conns.append(conn)

        return conn

    def __exit__(self, type, value, traceback):
        for conn in self.conns:
            conn.close()

        self.conns.clear()
