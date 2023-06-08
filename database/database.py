import sqlite3


class DataBase:
    """
    Класс отвечающий за базы данных
    """

    def __init__(self):
        """
        Конструктор
        """
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        """
        Менеджер запросов SQLITE

        :param sql:
        :param args:
        :param fetchone:
        :param fetchall:
        :param commit:
        :return:
        """
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        """
        Функция выводящая информацию о пользователе через id телеграма
        :param telegram_id:
        :return:
        """
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_user(self, telegram_id, full_name, phone):
        """
        Функция вводит данные при регистрации в базу данных

        :param telegram_id:
        :param full_name:
        :param phone:
        :return:
        """
        sql = '''
        INSERT INTO users(telegram_id, full_name, phone) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, full_name, phone, commit=True)


