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
    
    def insert_admin(self, emp_data):
        """Insert admin into the database."""
        sql = '''
            INSERT INTO employees (id, name, phone, email,password,is_super_admin)
            VALUES (?, ?, ?, ?, ?, ?)
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
            INSERT INTO projects (id, name, client_name, client_phone, client_email, description, end_date, commission, employee_id)
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
    
    def get_all_projects_undone_today(self,employee_id):
        """Retrieve all projects with end date today."""
        sql='''SELECT * FROM projects WHERE status = 0 AND employee_id = ? AND end_date = DATE('now')'''
        self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def get_all_projects_undone_tomorrow(self,employee_id):
        """Retrieve all projects with end date tomorrow."""
        sql='''SELECT * FROM projects WHERE status = 0 AND employee_id = ? AND end_date = DATE('now','+1 day')'''
        self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def get_all_projects_undone_late(self,employee_id):
        """Retrieve all projects with end date late."""
        sql='''SELECT * FROM projects WHERE status = 0 AND employee_id = ? AND end_date < DATE('now')'''
        self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def login(self,username,password,role):
        """Login the user."""
        sql='''SELECT id, name FROM employees WHERE id=? AND password=? AND is_super_admin=?'''
        self.db.cursor.execute(sql,(username,password,role))
        return self.db.cursor.fetchall()
    
    def get_all_freelancers(self):
        """Retrieve all freelancers"""
        sql='''SELECT * FROM freelancers'''
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()
    
    def change_password(self,employee_id,password):
        """Change the password of the employee."""
        sql='''UPDATE employees SET password=? WHERE id=?'''
        self.db.cursor.execute(sql,(password,employee_id))
        self.db.conn.commit()
    
    def check_password(self,employee_id,password):
        """Check the password of the employee."""
        sql='''SELECT * FROM employees WHERE id=? AND password=?'''
        self.db.cursor.execute(sql,(employee_id,password))
        return self.db.cursor.fetchall()
    
    def assign_project(self,project_id,freelance_id,freelance_commission,project):
        """assign project"""
        sql='''UPDATE projects SET freelancer_commission = ? , freelancer_id = ? WHERE id = ? '''
        self.db.cursor.execute(sql,(freelance_commission,freelance_id,project_id))
        self.db.conn.commit()
        sql='''UPDATE freelancers SET currently_available = ? , project_assigned = ? WHERE id = ? '''
        self.db.cursor.execute(sql,(False,project,freelance_id))
        self.db.conn.commit()
     
    def get_freelancer_data(self,id):
        """retrieve freelancer data"""
        sql='''SELECT currently_available FROM freelancers WHERE id = ?'''
        self.db.cursor.execute(sql,(id,))
        return self.db.cursor.fetchall()
    
    def update_completion_freelancer_emp_status(self,free_id,emp_id):
        """update completion status"""
        sql='''UPDATE freelancers SET project_done = project_done + 1, currently_available = ? WHERE id = ?'''
        self.db.cursor.execute(sql,(True,free_id,))
        self.db.conn.commit()
        sql='''UPDATE employees SET project_done = project_done + 1 WHERE id = ?'''
        self.db.cursor.execute(sql,(emp_id,))
        self.db.conn.commit()

    def get_all_emp(self):
        """Retrieve all employees"""
        sql='''SELECT * FROM employees'''
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()
    
    def get_all_projects_done(self,isAll,employee_id):
        """Retrieve all projects done"""
        if isAll:
            sql='''SELECT * FROM projects WHERE status = 1'''
            self.db.cursor.execute(sql)
        else:
            sql='''SELECT * FROM projects WHERE status = 1 AND employee_id = ?'''
            self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def get_all_projects_late(self,isAll,employee_id):
        """Retrieve all projects late"""
        if isAll:
            sql='''SELECT * FROM projects WHERE end_date < DATE('now') AND status = 0'''
            self.db.cursor.execute(sql)
        else:
            sql='''SELECT * FROM projects WHERE end_date < DATE('now') AND status = 0 AND employee_id = ?'''
            self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def get_all_projects_pending(self,isAll,employee_id):
        """Retrieve all projects pending"""
        if isAll:
            sql='''SELECT * FROM projects WHERE status = 0'''
            self.db.cursor.execute(sql)
        else:
            sql='''SELECT * FROM projects WHERE status = 0 AND employee_id = ?'''
            self.db.cursor.execute(sql,(employee_id,))
        return self.db.cursor.fetchall()
    
    def get_emp_data(self,id):
        """Retrieve employee data"""
        sql='''SELECT * FROM employees WHERE id = ?'''
        self.db.cursor.execute(sql,(id,))
        return self.db.cursor.fetchall()
    
    def delete_emp(self,id):
        """Delete employee"""
        sql='''DELETE FROM employees WHERE id = ?'''
        self.db.cursor.execute(sql,(id,))
        self.db.conn.commit()   

    def close_connection(self):
        """Close the database connection."""
        self.db.close()
