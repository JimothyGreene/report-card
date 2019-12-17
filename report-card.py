import db_cmd as db

database = 'report-card.db'
letter_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+',
                 'C', 'C-', 'D+', 'D', 'D-']
default_cutoffs = [92.5, 89.5, 86.5, 82.5, 79.5, 76.5,
                   72.5, 69.5, 66.5, 62.5, 59.5]


def main():
    conn = db.create_connection(database)
    db.create_main_table(conn)
    db.create_assignment_table(conn)

    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')

    print('Welcome to your report card. What would you like to do? ')
    while True:
        print("Would you like to 'Check', 'Add', 'Delete' or 'Exit'?")
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
        elif command == 'delete':
            print("Would you like to delete a 'Course' or an 'Assignment'?")
            add_command = input().lower()
            if add_command == 'course':
                delete_course(conn)
            elif add_command == 'assignment':
                delete_assignment(conn)
            else:
                print('That is not a valid command. Please try again')
        elif command == 'exit':
            print('Shutting down...')
            break
        else:
            print('That is not a valid command. Please try again')
    conn.close()


def total_grade(conn, course_name):
    assignments = db.get_assignments(conn, course_name)
    weights = db.get_course_weights(conn, course_name)
    average = 0
    weight_sum = 0
    for assignment_type in weights.keys():
        weight = weights[assignment_type]
        for assignment in assignments:
            check = 0
            if assignment_type == assignment[1]:
                check = -1
                average += assignment[2]*weight
            if check == -1:
                weight_sum += weight
    return average/weight_sum


def check_grades(conn):
    print('Which class?')
    course_name = input().upper()
    if not db.check_course_exists(conn, course_name):
        print('That course does not exist')
        return
    assignments = db.get_assignments(conn, course_name)
    for assignment in assignments:
        print(f'{assignment[0]}: {assignment[2]}')
    print(f'Total Grade: {total_grade(conn, course_name)}')


def check_gpa(conn):
    total_credit_hours = 0
    weighted_sum = 0
    course_list = db.get_course_list(conn)
    for course in course_list.keys():
        credit_hours = 0
        course_name = course_list[course]
        course_split = list(course_name)
        for ch in course_split:
            if ch.isdigit():
                credit_hours = int(ch)
                break
        grade = total_grade(conn, course_name)
        letter_cutoffs = db.get_course_cuttoffs(conn, course_name)
        grade_points = 0
        for i in range(0, len(letter_cutoffs)):
            cutoff = letter_cutoffs[i]
            if cutoff is not None and grade >= cutoff:
                grade_points = 4-(i/3)
                break
            else:
                continue
        weighted_sum += grade_points*credit_hours
        total_credit_hours += credit_hours
    print(f'GPA: {weighted_sum/total_credit_hours}')


def add_course(conn):
    print('Which class?')
    course_name = input().upper()
    if db.check_course_exists(conn, course_name):
        print('That course already exists')
        return
    print('Which semester? (e.g. F19)')
    course_semester = input().upper()
    cutoff_list = []
    print('Are the grade cutoffs different from the default? (y/n)')
    print(default_cutoffs)
    ans = input().lower()
    if ans == 'y':
        for letter in letter_grades:
            print(f"What is the cutoff for a(n) {letter}? ('None' if unused)")
            cutoff = input().lower()
            if cutoff == 'none':
                cutoff = None
            else:
                cutoff = float(cutoff)
            cutoff_list.append(cutoff)
        db.create_course(conn, course_name, course_semester, cutoff_list)
    elif ans == 'n':
        db.create_course(conn, course_name, course_semester, default_cutoffs)
    else:
        print('That is not a valid reponse')
    weights = {}
    while True:
        print("Enter an assignment type ('Done' to exit): ")
        assignment_type = input().lower()
        if assignment_type == 'done':
            break
        print('Enter the weight (e.g. .3): ')
        assignment_weight = float(input())
        weights[assignment_type] = assignment_weight
    db.set_course_weights(conn, course_name, weights)


def add_assignment(conn):
    print('Which class?')
    course_name = input().upper()
    if not db.check_course_exists(conn, course_name):
        print('That course does not exist')
        return
    assignment_info = []
    print('Enter the assignment name: ')
    assignment_info.append(input().lower())
    print('Enter the assignment type: ')
    assignment_type = input().lower()
    if not db.check_assignment_type_exists(conn, course_name, assignment_type):
        print('That assignment type does not exist')
        return
    assignment_info.append(assignment_type)
    print('Enter the grade')
    assignment_info.append(float(input().lower()))
    db.create_assignment(conn, assignment_info, course_name)


def delete_course(conn):
    print('Which class?')
    course_name = input().upper()
    if not db.check_course_exists(conn, course_name):
        print('That course does not exist')
        return
    print(f'Are you sure you want to remove {course_name}? (y/n)')
    if input().lower() == 'y':
        db.remove_course(conn, course_name)
        print(f'{course_name} was removed')
    else:
        print(f'{course_name} was not removed')


def delete_assignment(conn):
    print('Which class?')
    course_name = input().upper()
    if not db.check_course_exists(conn, course_name):
        print('That course does not exist')
        return
    print('Which assignment?')
    assignment_name = input().lower()
    if not db.check_assignment_exists(conn, course_name, assignment_name):
        print('That assignment does not exist')
        return
    db.remove_assignment(conn, assignment_name, course_name)
    print(f'{assignment_name} was removed')


if __name__ == '__main__':
    main()
