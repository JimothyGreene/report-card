import db_cmd as db

database = 'report-card.db'
conn = db.create_connection(database)


def main():
    db.create_main_table(conn)
    db.add_course(conn, 'EE302H', 'F19')
    db.create_assignment_table(conn)
    conn.close()


if __name__ == '__main__':
    main()
