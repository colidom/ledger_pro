import sqlite3


class LadgerProDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS neighbors (
                                id INTEGER PRIMARY KEY,
                                house_number INTEGER,
                                owner_name TEXT,
                                owner_lastname TEXT,
                                phone TEXT,
                                property_id INTEGER,
                                FOREIGN KEY(property_id) REFERENCES properties(id)
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
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS payments (
                            id INTEGER PRIMARY KEY,
                            neighbor_id INTEGER,
                            amount INTEGER,
                            month TEXT,
                            year INTEGER,
                            status TEXT, -- "paid" o "pending"
                            FOREIGN KEY(neighbor_id) REFERENCES neighbors(id)
                            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS incomes (
                            id INTEGER PRIMARY KEY,
                            amount INTEGER,
                            entity TEXT,
                            date TEXT,
                            description TEXT, 
                            FOREIGN KEY(entity) REFERENCES properties(property_number)
                            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    amount REAL,
                    date TEXT,
                    description TEXT
                    )"""
        )
        self.conn.commit()

    def insert_neighbor(
        self, house_number, owner_name, owner_lastname, phone, property_id
    ):
        self.cursor.execute(
            """INSERT INTO neighbors (house_number, owner_name, owner_lastname, phone, property_id)
                                VALUES (?, ?, ?, ?, ?)""",
            (house_number, owner_name, owner_lastname, phone, property_id),
        )
        self.conn.commit()

    def get_all_neighbors(self):
        self.cursor.execute("""SELECT * FROM neighbors""")
        return self.cursor.fetchall()

    def update_neighbor(
        self, neighbor_id, house_number, owner_name, owner_lastname, phone, property_id
    ):
        self.cursor.execute(
            """UPDATE neighbors SET house_number=?, owner_name=?, owner_lastname=?, phone=?, property_id=?
               WHERE id=?""",
            (house_number, owner_name, owner_lastname, phone, property_id, neighbor_id),
        )
        self.conn.commit()

    def delete_neighbor(self, neighbor_id):
        self.cursor.execute("""DELETE FROM neighbors WHERE id=?""", (neighbor_id,))
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

    def get_properties_with_debt(self):
        query = """
            SELECT p.id, p.property_number, n.owner_name || ' ' || n.owner_lastname AS neighbor_name, p.debt_amount, 
                GROUP_CONCAT(
                    CASE 
                        WHEN py.status = 'pending' 
                        THEN py.month || ' ' || py.year || ': ' || py.amount || '€' 
                    END, '; '
                ) AS pending_payments
            FROM properties p
            JOIN neighbors n ON p.id = n.property_id
            LEFT JOIN payments py ON n.id = py.neighbor_id
            WHERE p.is_paid = 'No'
            GROUP BY p.id, p.property_number, neighbor_name, p.debt_amount
            """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_income(self, amount, entity, date, description):
        self.cursor.execute(
            """INSERT INTO incomes (amount, entity, date, description) VALUES (?, ?, ?, ?)""",
            (amount, entity, date, description),
        )
        self.conn.commit()

    def update_income(self, income_id, amount, entity, date, description):
        query = (
            "UPDATE incomes SET amount=?, entity=?, date=?, description=? WHERE id=?"
        )
        self.cursor.execute(query, (amount, entity, date, description, income_id))
        self.conn.commit()

    def delete_income(self, income_id):
        self.cursor.execute("""DELETE FROM incomes WHERE id=?""", (income_id,))
        self.conn.commit()

    def get_all_incomes(self):
        self.cursor.execute("""SELECT * FROM incomes""")
        return self.cursor.fetchall()

    def insert_expense(self, amount, date, description):
        with self.conn:
            self.conn.execute(
                "INSERT INTO expenses (amount, date, description) VALUES (?, ?, ?)",
                (amount, date, description),
            )

    def get_all_expenses(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM expenses").fetchall()

    def update_expense(self, expense_id, amount, date, description):
        with self.conn:
            self.conn.execute(
                "UPDATE expenses SET amount = ?, date = ?, description = ? WHERE id = ?",
                (amount, date, description, expense_id),
            )

    def delete_expense(self, expense_id):
        with self.conn:
            self.conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
