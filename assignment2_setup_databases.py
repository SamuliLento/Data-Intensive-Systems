#This code is based on the video "Using copilot to create assignment 2"

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

DATABASES = [
    "dogs_db",
    "cats_db",
    "pigs_db"
]

def create_database(db_name):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database="postgres"
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(
        f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"
    )

    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"Created database: {db_name}")
    else:
        print(f"Database already exists: {db_name}")

    cur.close()
    conn.close()

def setup_dogs_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database="dogs_db"
    )

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dogs(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        color VARCHAR(100)
    )
    """)

    cur.execute("DELETE FROM dogs")

    cur.execute("""
    INSERT INTO dogs(name, color)
    VALUES
    ('Annie', 'gold'),
    ('Jack', 'black'),
    ('Rusty', 'brown')
    """)

    conn.commit()
    cur.close()
    conn.close()

def setup_cats_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database="cats_db"
    )

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cats(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        color VARCHAR(100)
    )
    """)

    cur.execute("DELETE FROM cats")

    cur.execute("""
    INSERT INTO cats(name, color)
    VALUES
    ('Bob', 'black'),
    ('Whiskers', 'white'),
    ('Milky', 'grey')
    """)

    conn.commit()
    cur.close()
    conn.close()

def setup_pigs_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database="pigs_db"
    )

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pigs(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        color VARCHAR(100)
    )
    """)

    cur.execute("DELETE FROM pigs")

    cur.execute("""
    INSERT INTO pigs(name, color)
    VALUES
    ('Steve', 'grey'),
    ('Adam', 'pink'),
    ('Eve', 'black')
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    for db in DATABASES:
        create_database(db)

    setup_dogs_db()
    setup_cats_db()
    setup_pigs_db()

    print("All databases prepared successfully.")