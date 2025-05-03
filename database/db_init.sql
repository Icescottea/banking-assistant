CREATE TABLE account_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE loan_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    interest_rate REAL,
    description TEXT
);

CREATE TABLE fixed_deposits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration_months INTEGER,
    interest_rate REAL
);

CREATE TABLE credit_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    annual_fee REAL,
    benefits TEXT
);
