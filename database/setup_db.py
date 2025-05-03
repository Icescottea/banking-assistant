import sqlite3

def run_sql_script(sql_file, db_name="banking.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    with open(sql_file, "r") as file:
        sql_script = file.read()
    
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print(f"✅ Database '{db_name}' created successfully.")

if __name__ == "__main__":
    run_sql_script("database/db_init.sql")
