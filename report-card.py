import db_cmd as db

database = 'report-card.db'
conn = db.create_connection(database)
db.create_courses_table(conn)
conn.close()


def main():
    pass


if __name__ == '__main__':
    main()
