import db_cmd as db

database = 'report-card.db'
conn = db.create_connection(database)
assignment_info = {'Homework': .2, 'Final': .3}


def main():
    db.create_main_table(conn)
    db.add_course(conn, 'EE302H', 'F19')
    db.create_assignment_table(conn)
    db.update_course(conn, 'EE302H', assignment_info)
    conn.close()


if __name__ == '__main__':
    main()
