import sqlite3
from sqlite3 import Error


def create_connection(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)


def create_courses_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Courses (
        course_id integer PRIMARY KEY,
        course_name text NOT NULL,
        semester text NOT NULL
    )''')


def add_course(conn, course_name):
    pass
