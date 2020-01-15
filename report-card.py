import db_cmd as db
import statistics
import shutil

database = 'report-card.db'
whatif = 'what-if.db'
letter_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+',
                 'C', 'C-', 'D+', 'D', 'D-']
default_cutoffs = [92.5, 89.5, 86.5, 82.5, 79.5, 76.5,
                   72.5, 69.5, 66.5, 62.5, 59.5]


def main():
    print('Welcome to your report card. What would you like to do? ')
    print('Do you want to look at what-if grades? (y/n)')
    if input().lower() == 'y':
        shutil.copyfile(database, whatif)
        conn = db.create_connection(whatif)
    else:
        conn = db.create_connection(database)
    db.create_main_table(conn)
    db.create_assignment_table(conn)

    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')

    while True:
        print("Would you like to 'Check', 'Add', 'Delete', 'Edit' or 'Exit'?")
        command = input().lower()
        if command == 'check':
            while True:
                print("Would you like to check 'Grades' or 'GPA'? ",
                      end='')
                print("('Done' to stop)")
                check_command = input().lower()
                if check_command == 'grades':
                    print("Would you like to check a 'Course' or 'Semester'? ",
                          end='')
                    print("('Done' to stop)")
                    grades_command = input().lower()
                    if grades_command == 'course':
                        check_grades(conn)
                    elif grades_command == 'semester':
                        display_courses(conn)
                    else:
                        print('That is not a valid command. Please try again')
                elif check_command == 'gpa':
                    check_gpa(conn)
                elif check_command == 'done':
                    break
                else:
                    print('That is not a valid command. Please try again')
        elif command == 'add':
            while True:
                print("Would you like to add a 'Course' or 'Assignment'? ",
                      end='')
                print("('Done' to stop)")
                add_command = input().lower()
                if add_command == 'course':
                    add_course(conn)
                elif add_command == 'assignment':
                    add_assignment(conn)
                elif add_command == 'done':
                    break
                else:
                    print('That is not a valid command. Please try again')
        elif command == 'delete':
            while True:
                print("Would you like to delete a 'Course' or 'Assignment'? ",
                      end='')
                print("('Done' to stop)")
                delete_command = input().lower()
                if delete_command == 'course':
                    delete_course(conn)
                elif delete_command == 'assignment':
                    delete_assignment(conn)
                elif delete_command == 'done':
                    break
                else:
                    print('That is not a valid command. Please try again')
        elif command == 'edit':
            while True:
                print("Would you like to edit a 'Course' or 'Assignment'? ",
                      end='')
                print("('Done' to stop)")
                delete_command = input().lower()
                if delete_command == 'course':
                    pass
                    # edit course function
                elif delete_command == 'assignment':
                    edit_assignment(conn)
                elif delete_command == 'done':
                    break
                else:
                    print('That is not a valid command. Please try again')
        elif command == 'exit':
            print('Shutting down...')
            break
        else:
            print('That is not a valid command. Please try again')
    conn.close()


def total_grade(conn, course_name):
    weights = db.get_course_weights(conn, course_name)
    average = 0
    weight_sum = 0
    for assignment_type in weights.keys():
        grades = []
        drops = db.get_assignment_drops(conn, course_name, assignment_type)
        weight = weights[assignment_type]
        assignments = db.get_assignment_of_type(conn, course_name,
                                                assignment_type)
        if assignments:
            weight_sum += weight
            for assignment in assignments:
                grades.append(assignment[2])
            grades.sort()
            grades = grades[drops:] if len(grades)>drops and drops else grades
            average += statistics.mean(grades)*weight
    return average/weight_sum if weight_sum != 0 else 0


def check_grades(conn):
    print('Which class?')
    course_name = input().upper()
    if not db.check_course_exists(conn, course_name):
        print('That course does not exist')
        return
    display_grades(conn, course_name)
    print('-------------------')
    print('Total Grade: %5.2f' % (total_grade(conn, course_name)))
    print('-------------------')


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
        if grade == 0:
            continue
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
    print('---------')
    print('GPA: %3.2f' % (weighted_sum/total_credit_hours))
    print('---------')


def add_course(conn):
    print('Enter the course name:')
    course_name = input().upper()
    if db.check_course_exists(conn, course_name):
        print('That course already exists')
        return
    print('Which semester? (e.g. F19)')
    course_semester = input().upper()
    cutoff_list = []
    drops_list = []
    while True:
        print('Are the grade cutoffs different from the default? (y/n)')
        print(default_cutoffs)
        ans = input().lower()
        if ans == 'y':
            for letter in letter_grades:
                while True:
                    print(f"What is the cutoff for a {letter}? ", end='')
                    print("('None' is valid)")
                    cutoff = input().lower()
                    if cutoff == 'none':
                        cutoff_list.append(None)
                        break
                    elif float(cutoff) >= 0 and float(cutoff) <= 120:
                        cutoff_list.append(float(cutoff))
                        break
                    else:
                        print('That is not a valid cutoff')
            break
        elif ans == 'n':
            cutoff_list = default_cutoffs
            break
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
        print('How many drops are there?')
        drops_list.append(int(input()))
    db.create_course(conn, course_name, course_semester, cutoff_list)
    db.set_assignment_info(conn, course_name, weights, drops_list)
    print(f'{course_name} has been added')


def add_assignment(conn):
    while True:
        print("Which class? ('Done' to stop)")
        course_name = input().upper()
        if course_name == 'done':
            break
        if not db.check_course_exists(conn, course_name):
            print('That course does not exist')
            return
        while True:
            assignment_info = []
            print("Enter the assignment name ('Done' to stop): ")
            assignment_name = input().lower()
            if assignment_name == 'done':
                break
            assignment_info.append(assignment_name)
            while True:
                print('Enter the assignment type: ')
                assignment_type = input().lower()
                if not db.check_assignment_type_exists(conn, course_name,
                                                       assignment_type):
                    print('That assignment type does not exist')
                    continue
                break
            assignment_info.append(assignment_type)
            print('Enter the grade:')
            assignment_info.append(float(input().lower()))
            db.create_assignment(conn, assignment_info, course_name)
            print(f'{assignment_info[0]} has been added')


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
    while True:
        print("Which class? ('Done' to stop)")
        course_name = input().upper()
        if course_name == 'done':
            break
        if not db.check_course_exists(conn, course_name):
            print('That course does not exist')
            return
        while True:
            display_grades(conn, course_name)
            print("Which assignment? ('Done' to stop)")
            assignment_name = input().lower()
            if assignment_name == 'done':
                break
            if not db.check_assignment_exists(conn, course_name,
                                              assignment_name):
                print('That assignment does not exist')
                return
            db.remove_assignment(conn, assignment_name, course_name)
            print(f'{assignment_name} was removed')


def edit_assignment(conn):
    while True:
        print("Which class? ('Done' to stop)")
        course_name = input().upper()
        if course_name == 'done':
            break
        if not db.check_course_exists(conn, course_name):
            print('That course does not exist')
            return
        while True:
            display_grades(conn, course_name)
            print("Which assignment? ('Done' to stop)")
            assignment_name = input().lower()
            if assignment_name == 'done':
                break
            if not db.check_assignment_exists(conn, course_name,
                                              assignment_name):
                print('That assignment does not exist')
                return
            print('What is the new assignment grade?')
            new_grade = float(input())
            assignment_info = db.get_assignment(conn, course_name, assignment_name)
            assignment_info = (assignment_info[0], assignment_info[1], new_grade)
            db.remove_assignment(conn, assignment_name, course_name)
            db.create_assignment(conn, assignment_info, course_name)
            print(f'{assignment_name} new grade is {new_grade}')

def display_grades(conn, course_name):
    assignments = db.get_assignments(conn, course_name)
    assignment_types = db.get_assignment_types(conn, course_name)
    print('===============')
    print(f'{course_name} grades:')
    print('===============')
    for assignment_type in assignment_types:
        print('-------------------')
        print(assignment_type[0].title())
        print('-------------------')
        for assignment in assignments:
            if assignment[1] == assignment_type[0]:
                print(f'{assignment[0].title()}: {assignment[2]}')


def display_courses(conn):
    print('Which semester? (e.g. F19)')
    semester = input().upper()
    semester_courses = db.get_course_semester_list(conn, semester)
    if not semester_courses:
        print('There are no courses for that semester')
        return
    print('=======================')
    print(f'Grades for semester {semester}')
    print('=======================')
    for course in semester_courses:
        print(f'{course}: %5.2f' % total_grade(conn, course))
    print('=======================')

# TODO: Implement edit functions for course


if __name__ == '__main__':
    main()
