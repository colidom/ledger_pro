import sqlite3


class UserDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                house_number INTEGER,
                                owner_name TEXT,
                                owner_lastname TEXT,
                                additional_field TEXT
                                )"""
        )
        self.conn.commit()

    def insert_user(self, house_number, owner_name, owner_lastname, additional_field):
        self.cursor.execute(
            """INSERT INTO users (house_number, owner_name, owner_lastname, additional_field)
                                VALUES (?, ?, ?, ?)""",
            (house_number, owner_name, owner_lastname, additional_field),
        )
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute("""SELECT * FROM users""")
        return self.cursor.fetchall()


# Ejemplo de uso
if __name__ == "__main__":
    db = UserDatabase("users.db")

    # Insertar un nuevo usuario
    db.insert_user(101, "John", "Doe", "additional_info")

    # Obtener todos los usuarios
    users = db.get_all_users()
    print("Lista de usuarios:")
    for user in users:
        print(user)

    # Cerrar la conexión con la base de datos
    db.conn.close()