import sqlite3


class LadgerProDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                house_number INTEGER,
                                owner_name TEXT,
                                owner_lastname TEXT,
                                phone TEXT
                                )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS properties (
                                id INTEGER PRIMARY KEY,
                                property_number TEXT,
                                is_paid TEXT,
                                debt_amount REAL
                                )"""
        )
        self.conn.commit()

    def insert_user(self, house_number, owner_name, owner_lastname, phone):
        self.cursor.execute(
            """INSERT INTO users (house_number, owner_name, owner_lastname, phone)
                                VALUES (?, ?, ?, ?)""",
            (house_number, owner_name, owner_lastname, phone),
        )
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute("""SELECT * FROM users""")
        return self.cursor.fetchall()

    def update_user(self, user_id, house_number, owner_name, owner_lastname, phone):
        self.cursor.execute(
            """UPDATE users SET house_number=?, owner_name=?, owner_lastname=?, phone=?
               WHERE id=?""",
            (house_number, owner_name, owner_lastname, phone, user_id),
        )
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("""DELETE FROM users WHERE id=?""", (user_id,))
        self.conn.commit()

    def insert_property(self, property_number, is_paid, debt_amount):
        self.cursor.execute(
            """INSERT INTO properties (property_number, is_paid, debt_amount)
                                VALUES (?, ?, ?)""",
            (property_number, is_paid, debt_amount),
        )
        self.conn.commit()

    def get_all_properties(self):
        self.cursor.execute("""SELECT * FROM properties""")
        return self.cursor.fetchall()

    def update_property(self, property_id, property_number, is_paid, debt_amount):
        self.cursor.execute(
            """UPDATE properties SET property_number=?, is_paid=?, debt_amount=?
               WHERE id=?""",
            (property_number, is_paid, debt_amount, property_id),
        )
        self.conn.commit()

    def delete_property(self, property_id):
        self.cursor.execute("""DELETE FROM properties WHERE id=?""", (property_id,))
        self.conn.commit()
