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
        semester text NOT NULL,
        A float,
        Am float,
        Bp float,
        B float,
        Bm float,
        Cp float,
        C float,
        Cm float,
        Dp float,
        D float,
        Dm float
    )''')
    conn.commit()


def create_course_table(conn, course_name):
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {course_name} (
        assignment_type text NOT NULL,
        assignment_weight float NOT NULL,
        drops integer NOT NULL
    )''')
    conn.commit()


def create_course(conn, course_name, semester, cutoff_list):
    c = conn.cursor()
    if not check_course_exists(conn, course_name):
        create_course_table(conn, course_name)
        c.execute('''INSERT INTO Courses VALUES (?, ?, ?, ?, ?, ?, ?,
                                                 ?, ?, ?, ?, ?, ?, ?)''',
                  [None, course_name, semester] + cutoff_list)
        conn.commit()


def remove_course_table(conn, course_name):
    c = conn.cursor()
    c.execute(f'DROP TABLE IF EXISTS {course_name}')
    conn.commit()


def remove_course(conn, course_name):
    c = conn.cursor()
    if check_course_exists(conn, course_name):
        remove_course_table(conn, course_name)
        c.execute('DELETE FROM Courses WHERE course_name = ?',
                  [course_name])
    conn.commit()


def set_assignment_info(conn, course_name, assignment_weights, drops_list):
    c = conn.cursor()
    assignments = assignment_weights.keys()
    i = 0
    for assignment in assignments:
        c.execute(f'SELECT * FROM {course_name} WHERE assignment_type = ?',
                  [assignment])
        if not c.fetchall():
            c.execute(f'INSERT INTO {course_name} VALUES (?, ?, ?)',
                      [assignment,
                       assignment_weights[assignment],
                       drops_list[i]])
        i += 1
    conn.commit()


def get_course_cuttoffs(conn, course_name):
    c = conn.cursor()
    c.execute(f'SELECT * FROM Courses WHERE course_name = ?',
              [course_name])
    return c.fetchone()[3:]


def get_course_weights(conn, course_name):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {course_name}')
    course_info = c.fetchall()
    weights = {}
    for weight in course_info:
        weights[weight[0]] = weight[1]
    return weights


def get_course_id(conn, course_name):
    c = conn.cursor()
    c.execute('SELECT * FROM Courses WHERE course_name = ?',
              [course_name])
    return c.fetchone()[0]


def get_course_list(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM Courses')
    course_list = {}
    for course in c.fetchall():
        course_list[course[0]] = course[1]
    return course_list


def get_course_semester_list(conn, semester):
    c = conn.cursor()
    c.execute('SELECT * FROM Courses WHERE semester = ?',
              [semester])
    course_list = []
    for course in c.fetchall():
        course_list.append(course[1])
    return course_list


def create_assignment_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Assignments (
        assignment_name text NOT NULL,
        assignment_type text NOT NULL,
        assignment_grade float NOT NULL,
        course_id integer NOT NULL,
        FOREIGN KEY (course_id)
            REFERENCES Courses (course_id)
                ON DELETE CASCADE
    )''')
    conn.commit()


def create_assignment(conn, assignment_info, course_name):
    c = conn.cursor()
    c.execute('INSERT INTO Assignments VALUES (?, ?, ?, ?)',
              [assignment_info[0],
               assignment_info[1],
               assignment_info[2],
               get_course_id(conn, course_name)])
    conn.commit()


def remove_assignment(conn, assignment_name, course_name):
    c = conn.cursor()
    c.execute('''DELETE FROM Assignments WHERE assignment_name = ?
                 AND course_id = ?''',
              [assignment_name, get_course_id(conn, course_name)])
    conn.commit()


def get_assignment(conn, course_name, assignment_name):
    c = conn.cursor()
    c.execute('''SELECT * FROM Assignments WHERE course_id = ?
                 AND assignment_name = ?''',
              [get_course_id(conn, course_name), assignment_name])
    return c.fetchone()


def get_assignments(conn, course_name):
    c = conn.cursor()
    c.execute('SELECT * FROM Assignments WHERE course_id = ?',
              [get_course_id(conn, course_name)])
    return c.fetchall()


def get_assignment_types(conn, course_name):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {course_name}')
    return c.fetchall()


def get_assignment_of_type(conn, course_name, assignment_type):
    c = conn.cursor()
    c.execute('''SELECT * FROM Assignments WHERE course_id = ?
                 AND assignment_type = ?''',
              [get_course_id(conn, course_name), assignment_type])
    return c.fetchall()


def get_assignment_drops(conn, course_name, assignment_type):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {course_name} WHERE assignment_type = ?',
              [assignment_type])
    return c.fetchone()[2]


def check_course_exists(conn, course_name):
    c = conn.cursor()
    c.execute('SELECT * FROM Courses WHERE course_name = ?',
              [course_name.upper()])
    return True if c.fetchall() else False


def check_assignment_type_exists(conn, course_name, assignment_type):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {course_name} WHERE assignment_type = ?',
              [assignment_type.lower()])
    return True if c.fetchall() else False


def check_assignment_exists(conn, course_name, assignment_name):
    c = conn.cursor()
    c.execute(f'''SELECT * FROM Assignments WHERE assignment_name = ?
                AND course_id = ?''',
              [assignment_name, get_course_id(conn, course_name)])
    return True if c.fetchall() else False
