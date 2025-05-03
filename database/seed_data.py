import sqlite3

def insert_sample_data():
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()

    # Account Types
    cursor.executemany("""
        INSERT INTO account_types (name, description) VALUES (?, ?)
    """, [
        ("Savings Account", "Earn interest with easy access to your funds."),
        ("Current Account", "Ideal for frequent transactions with no interest."),
        ("Fixed Deposit", "Higher returns with fixed-term deposits.")
    ])

    # Loan Products
    cursor.executemany("""
        INSERT INTO loan_products (name, interest_rate, description) VALUES (?, ?, ?)
    """, [
        ("Personal Loan", 14.5, "For your personal financial needs."),
        ("Home Loan", 10.75, "Buy your dream home with low interest rates."),
        ("Education Loan", 9.5, "Support your higher studies locally or abroad.")
    ])

    # Fixed Deposits
    cursor.executemany("""
        INSERT INTO fixed_deposits (duration_months, interest_rate) VALUES (?, ?)
    """, [
        (3, 6.0),
        (6, 7.5),
        (12, 9.0)
    ])

    # Credit Cards
    cursor.executemany("""
        INSERT INTO credit_cards (name, annual_fee, benefits) VALUES (?, ?, ?)
    """, [
        ("Platinum Card", 5000.0, "Cashback + Lounge access + Travel insurance."),
        ("Gold Card", 3000.0, "Fuel discounts + Dining offers."),
        ("Student Card", 0.0, "No annual fee. Great for students.")
    ])

    conn.commit()
    conn.close()
    print("✅ Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
