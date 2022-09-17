import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

class MailDatabase():
    def __init__(self, db_file):
        self.db_file= db_file
        self.mail_table = """ CREATE TABLE IF NOT EXISTS mail(
                                        id,
                                        sender,
                                        receiver,
                                        subject,
                                        content,
                                        next_id,
                                        prev_id,
                                        read
                                    ); """
        self.conn = create_connection(self.mail_database)
        self.cur = self.conn.cursor
        create_table(self.conn,self.mail_table)

    def add_mail(self, mail):
        create_tuple = (mail.id,mail.sender,mail.receiver,mail.subject,mail.content,mail.read,mail.next_id,mail.prev_id,mail.timestamp)
        self.cur.execute("INSERT INTO mail VALUES(?,?,?,?,?,?,?,?)", create_tuple)
        self.conn.commit()
        return self.cur.lastrowid #just in case you want the lastrowd id created by the cursor dont think it would be necessary
        
    def get_all_mail(self):
        res = self.cur.execute("SELECT id, sender, receiver, subject, content, next_id, prev_id, read FROM mail ORDER BY id DESC")
        result = res.fetchall()
        return result


    def get_mail_by_id(self, id): #DK if it will work this way compared to using fetching all and searching the list but me will try it out; less lines 
        self.cur.execute("SELECT * FROM mail WHERE id=?",(id,))
        mail = self.cur.fetchone #hopefully this will work if not im gonna have to code a regular list search function.
        return mail

    def update_mail_by_id(self, id, key, value):
        sq1 = '''UPDATE mail SET nice {key} = ? WHERE id = ? '''
        self.cur.execute(sq1,(value,id))
        self.conn.commit()
        
