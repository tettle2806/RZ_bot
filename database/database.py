import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
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
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_user(self, telegram_id, full_name, phone):
        sql = '''
        INSERT INTO users(telegram_id, full_name, phone) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, full_name, phone, commit=True)

    def create_filials_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS filials(
            filial_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filial_name VARCHAR(100),
            place INTEGER,
            worktime VARCHAR(100),
            address VARCHAR(100)   
        )
        '''
        self.manager(sql, commit=True)

    def insert_filials(self):
        sql = '''
            INSERT INTO filials(filial_name, place, worktime, address) VALUES 
            ('Чиланзар', 50, '11:00-23:00', 'На чиланзаре'),
            ('Малика', 40, '9:00-19:00', 'На малике'),
            ('Максимка', 100, '12:00-23:00', 'На максимке'),
            ('Чорсу', 70, '8:00-1:00', 'На чорсу')
        '''
        self.manager(sql, commit=True)

    def get_filials_names(self):
        sql = '''
            SELECT filial_name FROM filials
        '''
        return self.manager(sql, fetchall=True)

    def get_filial(self, filial_name):
        sql = '''
            SELECT * FROM filials WHERE filial_name = ?
        '''
        return self.manager(sql, filial_name, fetchone=True)

    def create_categories_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(50) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def insert_categories(self):
        sql = '''
            INSERT INTO categories(category_title) VALUES
            ('Наборы(сеты)'),
            ('🥙 Шаурма'),
            ('🍟 Гарниры'),
            ('🌭 Хот-Доги'),
            ('🥗 Салаты'),
            ('🧂 Соусы'),
            ('🍮 Десерты'),
            ('🍨 Мороженое'),
            ('🌯 Лаваш'),
            ('🍔 Бургеры'),
            ('🍹 Холодные напитки'),
            ('☕ Горячие напитки'),
            ('Снеки')
        '''

        self.manager(sql, commit=True)

    def get_categories(self):
        sql = '''
            SELECT category_title FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def drop(self):
        sql = '''
            DROP TABLE products
        '''

        self.manager(sql, commit=True)

    def create_products_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title VARCHAR(50) UNIQUE,
            description VARCHAR(255),
            price INTEGER,
            image TEXT,
            category_id INTEGER REFERENCES categories(category_id)
            )
        '''
        self.manager(sql, commit=True)

    def insert_products(self):
        sql = '''
           INSERT INTO products(product_title, description, price, image, category_id) VALUES
        '''
        self.manager(sql, commit=True)

    def get_products_by_category(self, category_title):
        sql = '''
            SELECT product_title FROM products WHERE category_id = (
                SELECT category_id FROM categories WHERE category_title = ?
            )
        '''
        return self.manager(sql, category_title, fetchall=True)

    def get_products_by_title(self, product_title):
        sql = '''
            SELECT * FROM products WHERE product_title = ?
        '''

        return self.manager(sql, product_title, fetchone=True)

    def get_all_products(self):
        sql = '''
            SELECT product_title FROM products
        '''
        return self.manager(sql, fetchall=True)

    def create_cart_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart(
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            total_quantity INTEGER DEFAULT 0,
            total_price INTEGER DEFAULT 0
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart_products(
            cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER REFERENCES cart(cart_id),
            product_name VARCHAR(100) NOT NULL,
            final_price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,

            UNIQUE(cart_id, product_name)
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_for_user(self, telegram_id):
        sql = '''
        INSERT INTO cart(telegram_id) VALUES (?)
        '''
        self.manager(sql, telegram_id, commit=True)

    def get_cart_id(self, telegram_id):
        sql = '''
        SELECT cart_id FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_product_by_id(self, product_id):
        sql = '''
        SELECT product_title, price FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def insert_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?,?,?,?)
        '''
        self.manager(sql, cart_id, product_name, quantity, final_price, commit=True)

    def update_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        UPDATE cart_products
        SET
        quantity = quantity + ?,
        final_price = final_price + ?
        WHERE product_name = ? AND cart_id = ?
        '''
        self.manager(sql, quantity, final_price, product_name, cart_id, commit=True)
