import sqlite3

def connect_db():
    return sqlite3.connect("banking.db")

def get_account_types():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM account_types")
    data = cursor.fetchall()
    conn.close()
    return data

def get_loan_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, interest_rate, description FROM loan_products")
    data = cursor.fetchall()
    conn.close()
    return data

def get_fixed_deposits():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT duration_months, interest_rate FROM fixed_deposits")
    data = cursor.fetchall()
    conn.close()
    return data

def get_credit_cards():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, annual_fee, benefits FROM credit_cards")
    data = cursor.fetchall()
    conn.close()
    return data

