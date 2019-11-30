import sqlite3
from sqlite3 import Error


def create_connection(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)


def create_main_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Courses (
        course_id integer PRIMARY KEY,
        course_name text NOT NULL,
        semester text NOT NULL
    )''')
    conn.commit()


def create_grades_table(conn):
    pass


def add_course(conn, course_name, semester):
    c = conn.cursor()
    if check_new(conn, course_name):
        c.execute('INSERT INTO Courses VALUES (?, ?, ?)',
                  [None, course_name, semester])
        conn.commit()


def check_new(conn, course_name):
    c = conn.cursor()
    c.execute('SELECT * FROM Courses WHERE course_name = ?',
              [course_name])
    return False if c.fetchall() else True
