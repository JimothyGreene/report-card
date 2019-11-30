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


def create_course_table(conn, course_name):
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {course_name} (
        assignment_type text NOT NULL,
        assignment_weight float NOT NULL,
        course_id integer NOT NULL,
        FOREIGN KEY (course_id)
            REFERENCES Courses (course_id)
                ON DELETE CASCADE
    )''')
    conn.commit()


def create_assignment_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Assignments (
        assignment_type text NOT NULL,
        assignment_grade float NOT NULL,
        course_id integer NOT NULL,
        FOREIGN KEY (course_id)
            REFERENCES Courses (course_id)
                ON DELETE CASCADE
    )''')


def add_course(conn, course_name, semester):
    c = conn.cursor()
    if check_new(conn, course_name):
        create_course_table(conn, course_name)
        c.execute('INSERT INTO Courses VALUES (?, ?, ?)',
                  [None, course_name, semester])
        conn.commit()


def update_course(conn, course_name):
    pass


def check_new(conn, course_name):
    c = conn.cursor()
    c.execute('SELECT * FROM Courses WHERE course_name = ?',
              [course_name])
    return False if c.fetchall() else True
