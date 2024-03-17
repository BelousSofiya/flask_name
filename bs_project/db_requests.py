import psycopg2
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

# TODO: refactor to layers +
class DataBase:  # TODO: "Class" is extra +

    def __init__(self, **kwargs):
        with psycopg2.connect(**kwargs) as conn:
            self.conn = conn

    def initial_connect_with_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            id VARCHAR(100) PRIMARY KEY,
                            email VARCHAR(30),
                            full_name VARCHAR(30),
                            password VARCHAR(300),
                            admin BOOLEAN NOT NULL
                            )""")

    def get_user_by_email(self, email):
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
            return cur.fetchone()

    def create_user_in_db(self, data):
        user_id = str(uuid4())
        with self.conn.cursor() as cur:
            # TODO: !!! SQL injection https://www.psycopg.org/docs/usage.html#transactions-control
            cur.execute(f"""INSERT INTO users
                    ("id", "email", "full_name", "password", "admin")
                    VALUES('{user_id}', '{data['email']}', '{data['full_name']}', '{generate_password_hash(data['password'])}', {False})""")
            cur.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""")
            self.conn.commit()
            user = cur.fetchone()

            return user

    def get_user_by_id_in_db(self, user_id):  # TODO: return user | None +
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""")
            # user = cur.fetchall()  # TODO: fetchone()
            user = cur.fetchone()  # TODO: fetchone() +
            return user

    def get_all_users_in_db(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users""")
            users = cur.fetchall()
            return users

    def delete_user_by_id_in_db(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(f"""DELETE FROM users WHERE id = '{user_id}'""")
            self.conn.commit()

    # def reset_password_in_db(self, email, password):
    #     with self.conn.cursor() as cur:
    #         cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
    #         user = cur.fetchall()
    #         if user:
    #             cur.execute(f"""UPDATE users SET password = '{generate_password_hash(password)}' WHERE email = '{email}'""")
    #             self.conn.commit()
    #             return {"message": 'Reset password'}
    #         else:
    #             return {"message": 'User is not found '}
