import db_cmd as db

database = 'report-card.db'


def main():
    conn = db.create_connection(database)
    db.create_main_table(conn)
    db.create_assignment_table(conn)

    print('Welcome to your report card. What would you like to do? ')
    while True:
        print("Would you like to 'Check', 'Add', or 'Exit'?")
        if input().lower() == 'check':
            print("Would you like to check 'Grades' or 'GPA'?")
            if input().lower() == 'grades':
                check_grades(conn)
            elif input().lower() == 'gpa':
                check_gpa(conn)
            else:
                print('That is not a valid command. Please try again')
        elif input().lower() == 'add':
            print("Would you like to add a 'Course' or an 'Assignment'?")
            if input().lower() == 'course':
                add_course(conn)
            elif input().lower() == 'assignment':
                add_assignment(conn)
            else:
                print('That is not a valid command. Please try again')
        elif input().lower() == 'exit':
            print('Shutting down...')
            break
        else:
            print('That is not a valid command. Please try again')
    conn.close()


def check_grades(conn):
    pass


def check_gpa(conn):
    pass


def add_course(conn):
    pass


def add_assignment(conn):
    pass


if __name__ == '__main__':
    main()
