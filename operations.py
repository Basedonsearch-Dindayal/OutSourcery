from database import Database

class Operations:
    def __init__(self):
        """Initialize the database connection."""
        self.db = Database()

    def insert_employee(self, emp_data):
        """Insert an employee into the database."""
        sql = '''
            INSERT INTO employees (id, name, phone, email,password)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.db.cursor.execute(sql, tuple(emp_data.values()))
        self.db.conn.commit()

    def insert_freelancer(self, freelancer_data):
        """Insert a freelancer into the database."""
        sql = '''
            INSERT INTO freelancers (id, name, phone, email)
            VALUES (?, ?, ?, ?)
        '''
        self.db.cursor.execute(sql, tuple(freelancer_data.values()))
        self.db.conn.commit()

    def insert_project(self, project_data):
        """Insert a project into the database."""
        sql = '''
            INSERT INTO projects (id, name, client_name, client_phone, client_email, description, 
                                  end_date, commission, employee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.db.cursor.execute(sql, tuple(project_data.values()))
        self.db.conn.commit()

    def update_project_status(self, project_id, new_status):
        """Update the project status."""
        sql = '''UPDATE projects SET status = ? WHERE id = ?'''
        self.db.cursor.execute(sql, (new_status, project_id))
        self.db.conn.commit()

    def get_all_projects_undone(self,employee_id):
        """Retrieve all projects."""
        sql = '''SELECT * FROM projects WHERE status = 0 AND employee_id = ?'''
        self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def login(self,username,password,role):
        """Login the user."""
        sql='''SELECT id, name FROM employees WHERE id=? AND password=? AND is_super_admin=?'''
        self.db.cursor.execute(sql,(username,password,role))
        return self.db.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        self.db.close()
