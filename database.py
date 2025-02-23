import sqlite3

class Database:
    def __init__(self, db_name="local.db"):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates tables if they do not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id VARCHAR(6) PRIMARY KEY NOT NULL UNIQUE,
                name VARCHAR(50) NOT NULL,
                phone VARCHAR(10) NOT NULL UNIQUE,
                email VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(10) NOT NULL,
                joining_date DATE NOT NULL DEFAULT (DATE('now')),
                ending_date DATE,
                project_done INTEGER DEFAULT 0,
                is_super_admin BOOLEAN NOT NULL DEFAULT FALSE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS freelancers (
                id VARCHAR(6) PRIMARY KEY NOT NULL UNIQUE,
                name VARCHAR(50) NOT NULL,
                phone VARCHAR(10) NOT NULL UNIQUE,
                email VARCHAR(50) NOT NULL UNIQUE,
                project_assigned VARCHAR(100),
                currently_available BOOLEAN NOT NULL DEFAULT TRUE,
                project_done INTEGER DEFAULT 0
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id VARCHAR(6) PRIMARY KEY NOT NULL UNIQUE,
                name VARCHAR(50) NOT NULL,
                client_name VARCHAR(50) NOT NULL,
                client_phone VARCHAR(10) NOT NULL,
                client_email VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                start_date DATE NOT NULL DEFAULT (DATE('now')),
                end_date DATE NOT NULL,
                commission REAL NOT NULL,
                freelancer_commission REAL,
                status BOOLEAN NOT NULL DEFAULT FALSE,
                employee_id VARCHAR(6) NOT NULL,
                freelancer_id VARCHAR(6)
            )
        ''')
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
