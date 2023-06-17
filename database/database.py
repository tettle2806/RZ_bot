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
           ('Фирменное комбо','Фирменный бургер, картошка-фри и кола 0.5 мл. Отличный выбор для тез кто любит утонченный вкус бургера с нашим фирменным соусом', 47500,'photo/1.jpg' , 1),
           ('BBQ Delight','Комбо, которое включает в себя BBQ гамбургер, порцию картофеля фри и роскошный миндальный молочный коктейль.', 55000, 'photo/3.jpg', 1),
           ('Комбо для гурманов','Комбо состоит из 6 палочек молотого шашлыка, 500 грамм куриных бедер и 500 грамм жаренных криветок во фритюре',320000, 'photo/2.jpg', 1),
           ('Тройной Бургер',' Это комбо, включающее в себя три бургера на выбор: классический куриный, бекон-чеддер и бургер с брускеттой. К ним подается порция луковых колечек и газированный напиток на выбор из ассортимента',155000,'photo/4.jpeg', 1),
           ('Большой Аппетит','Это комбо, идеальное для голодных гурманов! Оно включает в себя двойной гамбургер с квестом, большую порцию картофеля фри и большой несладкий чай',65000, 'photo/5.jpg', 1),
           ('Kids-Комбо','Комбо для маленьких героев, куриный гамбургер с сыром и картошкой-фри и конечно же растишка что-бы наш герой рос большим ',40000, 'photo/6.jpg', 1)
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
