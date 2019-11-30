import db_cmd as db

database = 'report-card.db'


def main():
    conn = db.create_connection(database)
    db.create_main_table(conn)
    db.create_assignment_table(conn)

    print('Welcome to your report card. What would you like to do? ')
    while True:
        print("Would you like to 'Check', 'Add', or 'Exit'?")
        command = input().lower()
        if command == 'check':
            print("Would you like to check 'Grades' or 'GPA'?")
            check_command = input().lower()
            if check_command == 'grades':
                check_grades(conn)
            elif check_command == 'gpa':
                check_gpa(conn)
            else:
                print('That is not a valid command. Please try again')
        elif command == 'add':
            print("Would you like to add a 'Course' or an 'Assignment'?")
            add_command = input().lower()
            if add_command == 'course':
                add_course(conn)
            elif add_command == 'assignment':
                add_assignment(conn)
            else:
                print('That is not a valid command. Please try again')
        elif command == 'exit':
            print('Shutting down...')
            break
        else:
            print('That is not a valid command. Please try again')
    conn.close()


def check_grades(conn):
    print('Which class?')
    course_name = input().upper()
    assignments = db.get_assignments(conn, course_name)
    for assignment in assignments:
        print(f'{assignment[0]}: {assignment[2]}')
    # Calculate average based on weights
    course_weights = db.get_course_weights(conn, course_name)
    weights_dict = {}
    print(course_weights)
    for weight in course_weights:
        weights_dict[weight[0]] = weight[1]
    average = 0
    for assignment_type in weights_dict.keys():
        weight = weights_dict[assignment_type]
        for assignment in assignments:
            if assignment_type == assignment[1]:
                average += assignment[2]*weight
    print(f'Total Grade: {average}')
    # TODO: Correct algorithm for determining overall average


def check_gpa(conn):
    pass


def add_course(conn):
    print('Which class?')
    course_name = input().upper()
    print('Which semester? (e.g. F19)')
    course_semester = input().upper()
    db.create_course(conn, course_name, course_semester)
    # Update assignment weights
    weights = {}
    while True:
        print("Enter an assignment type ('Done' to exit): ")
        assignment_type = input().lower()
        if assignment_type == 'done':
            break
        print('Enter the weight (e.g. .3): ')
        assignment_weight = float(input())
        weights[assignment_type] = assignment_weight
    db.update_course(conn, course_name, weights)
    conn.commit()


def add_assignment(conn):
    pass


if __name__ == '__main__':
    main()
