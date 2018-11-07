class Message:
    """
    Messages that are sent/received
    """
    __id = None
    __from_id = None
    __to_id = None
    text = None
    __creation_date = None

    def __init__(self, ):
        self.__id = -1
        self.__from_id = -1
        self.__to_id = -1
        self.text = ''
        self.__creation_date = -1

    @property
    def id(self):
        return self.__id

    @property
    def from_id(self):
        return self.__from_id

    @from_id.setter
    def from_id(self, from_id):
        self.__from_id = from_id

    @property
    def to_id(self):
        return self.__to_id

    @to_id.setter
    def to_id(self, to_id):
        self.__to_id = to_id

    @property
    def creation_date(self):
        return self.__creation_date

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO Message(from_id, to_id, text, creation_date)
                VALUES(%s, %s, %s, now()) RETURNING id, creation_date"""
            values = (self.__from_id, self.__to_id, self.text)
            cursor.execute(sql, values)
            values = cursor.fetchone()
            self.__id = values[0]
            self.__creation_date = values[1]
            return True
        else:
            pass

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Message WHERE id=%s"
        cursor.execute(sql, (message_id,))  # (message_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.__from_id = data[1]
            loaded_message.__to_id = data[2]
            loaded_message.text = data[3]
            loaded_message.__creation_date = data[4]
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages_for_user(cursor, to_user_id):
        sql = """SELECT id, from_id, to_id, text, creation_date 
                FROM Message WHERE to_id=%s ORDER BY creation_date DESC"""
        ret = []
        cursor.execute(sql, (to_user_id,))
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.__from_id = row[1]
            loaded_message.__to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.__creation_date = row[4]
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, date FROM Message"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.__from_id = row[1]
            loaded_message.__to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.__creation_date = row[4]
            ret.append(loaded_message)
        return ret
