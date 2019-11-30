import db_cmd as db

database = 'report-card.db'
conn = db.create_connection(database)
db.create_main_table(conn)
db.add_course(conn, 'EE 302H', 'F19')
conn.close()


def main():
    pass


if __name__ == '__main__':
    main()
