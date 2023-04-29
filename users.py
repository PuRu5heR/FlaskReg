import sqlite3


class Users:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name

    def create_table(self):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        login TEXT,
        password TEXT,
        e_mail TEXT,
        full_name TEXT,
        birth_date TEXT,
        telegram_id INTEGER)""")
        print("Table was successfully created")

        self.con.commit()
        self.con.close()

    def new_user(self, login, password, e_mail, full_name, birth_date):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()

        self.cur.execute(
            """INSERT INTO users (login, password, e_mail, full_name, birth_date) VALUES (?, ?, ?, ?, ?)""",
            (login, password, e_mail, full_name, birth_date))
        print("User was successfully added")

        self.con.commit()
        self.con.close()

    def get_data_by_login(self, login):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        data = self.cur.execute("""SELECT * FROM users WHERE login=?""",
                                (login,)).fetchone()
        print(data)
        self.con.close()
        if not data:
            return None
        else:
            return data

    def get_data_by_id(self, user_id):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        data = self.cur.execute("""SELECT * FROM users WHERE user_id=?""",
                                (user_id,)).fetchone()
        print(data)
        self.con.close()
        if not data:
            return None
        else:
            return data

    def login_is_unique(self, login):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        data = self.cur.execute("""SELECT user_id FROM users WHERE login=?""",
                                (login,)).fetchone()
        print(data)
        self.con.close()
        if data:
            return True
        else:
            return False


if __name__ == "__main__":
    d = Users()
    print(d.get_data_by_login("Amir"))

