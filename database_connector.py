import sqlite3
from sqlite3 import Error

class DataHandler:
    def __init__(self):
        self.data_path = 'database_alarm.db'

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.data_path)
        except Error:
            print('Error on connection with DB')
        return conn

    def write_data(self, name, hour, minutes, repeats=0):
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            var1 = name
            var2 = f"{hour}:{minutes}"
            var3 = repeats
            cursor.execute("INSERT INTO alarms (name, time, repeats) VALUES (?, ?, ?)",
                           (var1, var2, var3))

    def read_data(self):
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alarms")
            return cursor.fetchall()

    def edit_data(self, id, name, hour, minutes, repeats=0):
        conn = self.create_connection()
        with conn:
            try:
                cursor = conn.cursor()
                var1 = name
                var2 = f"{hour}:{minutes}"
                var3 = repeats
                var4 = id
                cursor.execute("UPDATE alarms SET name = ?,"
                               " time = ?, repeats = ? where id = ?",
                               (var1, var2, var3, var4))
            except Error:
                print("Failed on edit DB record")

    def delete_data(self, id):
        conn = self.create_connection()
        with conn:
            try:
                cursor = conn.cursor()
                var = id
                cursor.execute("DELETE FROM alarms where id = ?", (var,))
            except Error:
                print("Failed on delete DB record")