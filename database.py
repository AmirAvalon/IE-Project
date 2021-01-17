import sqlite3
import logging

# Initializing logs
log = logging.getLogger(__name__)

log.debug("Trying to connect to database.db or create new if not exist")
conn = sqlite3.connect("database.db", check_same_thread=False)

with conn:
    log.debug("Initializing cursor")
    cursor = conn.cursor()

    # Creating user table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS users
        (
             chat_id INTEGER not null
                primary key,
            first_name VARCHAR not null,
            username VARCHAR,
            phone_number VARCHAR,
            cart TEXT,
            is_making_order BOOLEAN,
            is_operator BOOLEAN,
            is_administrator BOOLEAN
        );
        """)

        # Creating operator table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS operator
        (
             chat_id INTEGER not null
            primary key,
            first_name VARCHAR not null,
            username VARCHAR,
            phone_number VARCHAR,
            cart TEXT,
            is_making_order BOOLEAN,
            is_operator BOOLEAN,
            is_administrator BOOLEAN
        );
        """)

    # Creating category table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS categories
        (
             category_id INTEGER not null
                primary key autoincrement,
            title VARCHAR
        );
        """)

    # Creating products table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS products
        (
             id INTEGER not null
                primary key autoincrement,
            title VARCHAR,
            description TEXT,
            price INTEGER,
            image BLOB,
            category_id INTEGER,
            bot_shows BOOLEAN
        );
        """)

    # Creating orders table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS orders
        (
             order_id INTEGER not null
                primary key autoincrement,
            chat_id INTEGER,
            contacts TEXT,
            order_items TEXT,
            order_date DATE,
            status INTEGER,
            note TEXT
        );
        """)
    conn.commit()


def if_user_exists(chat_id):
    try:
        cursor.execute("SELECT * FROM users WHERE chat_id LIKE ?", [chat_id])
        g_user = cursor.fetchall()
        log.debug(g_user[0][1] + " was checked on existing")
        return True
    except IndexError:
        return False


def new_user(chat_id, first_name, username, phone_number):
    cursor.execute("""INSERT INTO users (chat_id, first_name, username, phone_number, is_making_order, is_operator,
     is_administrator) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, first_name, username, phone_number, 0, 0, 0))
    conn.commit()

def new_user_operator(chat_id, first_name, username, phone_number,is_operator):
    cursor.execute("""INSERT INTO operator (chat_id, first_name, username, phone_number, is_making_order, is_operator,
     is_administrator) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, first_name, username, phone_number, 0, 1, 0))
    conn.commit()


def new_order(chat_id, contacts, order_items, order_date, status, note):
    cursor.execute("""
    INSERT INTO orders (chat_id, contacts, order_items, order_date, status, note) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, (chat_id, contacts, order_items, order_date, status, note))
    conn.commit()


def add_category(title):
    cursor.execute("INSERT INTO category (title) VALUES (?)",
                   [title])
    conn.commit()
    log.debug(f"Added category: {title}")


def add_product(title, description, price, image, category_id):
    cursor.execute("""INSERT INTO products (title, description, price, image, category_id, bot_shows) 
    VALUES (?, ?, ?, ?, ?, ?)""", (title, description, price, image, category_id, 1))
    conn.commit()


def get_categories():
    cursor.execute("SELECT * FROM categories")
    return cursor.fetchall()


def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def get_product_ids():
    cursor.execute("SELECT id FROM products")
    return cursor.fetchall()


def get_product_by_id(prod_id):
    cursor.execute("SELECT * FROM products WHERE id LIKE ?", [prod_id])
    product = cursor.fetchall()
    return product[0]


def get_user_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE chat_id LIKE ?", [user_id])
    g_user = cursor.fetchall()
    try:
        return g_user[0]
    except IndexError:
        return None


def get_cart_by_id(user_id):
    cursor.execute("SELECT cart FROM users WHERE chat_id LIKE ?", [user_id])
    user_cart = cursor.fetchall()
    return user_cart[0][0]


def get_orders_by_id(user_id):
    cursor.execute("SELECT * FROM orders WHERE chat_id LIKE ?", [user_id])
    user_cart = cursor.fetchall()
    return user_cart


def get_orders_ids_by_id(user_id):
    cursor.execute("SELECT order_id FROM orders WHERE chat_id LIKE ?", [user_id])
    order_ids = cursor.fetchall()
    return order_ids


def get_making_order_by_id(user_id):
    cursor.execute("SELECT is_making_order FROM users WHERE chat_id LIKE ?", [user_id])
    making_orders = cursor.fetchall()
    return making_orders[0][0]


def get_operators():
    cursor.execute("SELECT chat_id FROM operator WHERE is_operator LIKE ?", [1])
    operators = cursor.fetchall()
    try:
        return operators[0]
    except IndexError:
        return None


def set_cart_to_user(user_id, cart):
    cursor.executemany("""UPDATE users 
    SET cart = ? WHERE chat_id = ?""", ((cart, user_id), ))
    conn.commit()


def set_making_order_status_to_user(user_id, status):
    cursor.executemany("""UPDATE users 
    SET is_making_order = ? WHERE chat_id = ?""", ((status, user_id), ))
    conn.commit()


def set_phone_number_to_user(user_id, phone):
    cursor.executemany("""UPDATE users 
    SET phone_number = ? WHERE chat_id = ?""", ((phone, user_id), ))
    conn.commit()

new_user_operator("357677914", "Amir", "@AmirN8ri", "None",1)
add_product("پرنده آبی", "(نمایش نامه)", 2500000, "images/item_1.png", 1)
add_product("آیشمن در اورشلیم", "(تاریخ)", 5500000, "images/item_2.png", 2)
add_product("مرگ فروشنده", "(نمایشنامه)", 2000000, "images/item_3.png", 3)
add_product("سووشون", "(رمان ایرانی)", 450000, "images/item_4.png", 4)
add_product("هنر در گذر زمان", "(تاریخ هنر)", 450000, "images/item_5.png", 5)
add_product("ابله", "(رمان خارجی)", 1750000, "images/item_6.png", 6)
add_product("شور زندگی", "(رمان خارجی)", 1000000, "images/item_7.png", 7)
add_product("پیرمرد و دریا", "(رمان خارجی)", 350000, "images/item_8.png", 8)
add_product("آتش بدون دود", "(داستان کوتاه ایرانی)", 3750000, "images/item_9.png", 9)
add_product("بلندیهای بادگیر", "(رمان خارجی)", 600000, "images/item_10.png", 10)