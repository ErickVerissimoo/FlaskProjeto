import mysql.connector

def open_connection(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def close_connection(conn):
    conn.close()

def create_connection():
    return open_connection("localhost", "root", "bts4", "reserva_app")

class Connection:
    HOST = "localhost"
    USER = "root"
    PASSWORD = "bts4"
    DATABASE = "reserva_app"

    def __init__(self):
        self = self.open(self.HOST, self.USER, self.PASSWORD, self.DATABASE)

    def open(self, host, user, password, database):
        return mysql.connector.connect(host=host, user=user, password=password, database=database)

    def close(self):
        self.close()