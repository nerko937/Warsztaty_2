from models import *
from psycopg2 import IntegrityError


class User:
    """
    Users that can comunicate with themselves
    """
    __id = None
    email = None
    __hashed_password = None

    def __init__(self):
        self.__id = -1
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO Users(email, hashed_password)
            VALUES(%s, %s) RETURNING id"""
            values = (self.email, self.__hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET email=%s, hashed_password=%s
            WHERE id=%s"""
            values = (self.email, self.__hashed_password, self.__id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, email, hashed_password FROM Users WHERE id=%s"
        cursor.execute(sql, (user_id,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.email = data[1]
            loaded_user.__hashed_password = data[2]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, email, email, hashed_password FROM Users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.email = row[1]
            loaded_user.__hashed_password = row[2]
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True

    @staticmethod
    def create_user(cursor, email, password):
        salt = generate_salt()
        hashed = password_hash(password, salt)
        new_user = User()
        new_user.email = email
        new_user.__hashed_password = hashed
        try:
            new_user.save_to_db(cursor)
        except IntegrityError:
            print('Taki użytkownik już istnieje')
            return False
        print('Stworzyłeś nowego użytkownika')
        return True

    def change_pass(self, cursor, new_pass):
        s = generate_salt()
        self.__hashed_password = password_hash(new_pass, s)
        self.save_to_db(cursor)

    @staticmethod
    def login(cursor, email, password):
        sql = "SELECT id, hashed_password FROM Users WHERE email=%s"
        cursor.execute(sql, (email,))
        items = cursor.fetchone()
        try:
            check = check_password(password, items[1])
        except TypeError:
            return None
        if check is True:
            return User.load_user_by_id(cursor, items[0])
        else:
            print('Błędny login lub hasło')
            return False
