from operations import Operations

if __name__ == "__main__":
    ops = Operations()

    # # Insert employees
    # employees = [
    #     {"id": "E001", "name": "Alice Johnson", "phone": "1234567890", "email": "alice@example.com","password":"abc1"},
    #     {"id": "E002", "name": "Bob Williams", "phone": "9876543210", "email": "bob@example.com","password":"abc2"},
    #     {"id": "E003", "name": "Charlie Davis", "phone": "4561237890", "email": "charlie@example.com","password":"abc3"},
    #     {"id": "E004", "name": "Daisy Parker", "phone": "8529637410", "email": "daisy@example.com","password":"abc4"},
    #     {"id": "E005", "name": "Ethan Moore", "phone": "3692581470", "email": "ethan@example.com","password":"abc5"},
    # ]
    
    # for emp in employees:
    #     ops.insert_employee(emp)
    # print("Employees inserted successfully!")

    # # Insert freelancers
    # freelancers = [
    #     {"id": "F001", "name": "Freelancer One", "phone": "7412589630", "email": "f1@example.com"},
    #     {"id": "F002", "name": "Freelancer Two", "phone": "3698521470", "email": "f2@example.com"},
    #     {"id": "F003", "name": "Freelancer Three", "phone": "1597534862", "email": "f3@example.com"},
    #     {"id": "F004", "name": "Freelancer Four", "phone": "2589631470", "email": "f4@example.com"},
    #     {"id": "F005", "name": "Freelancer Five", "phone": "3579514682", "email": "f5@example.com"},
    # ]
    
    # for freelancer in freelancers:
    #     ops.insert_freelancer(freelancer)
    # print("Freelancers inserted successfully!")

    # Insert projects
    projects = [
        {"id": "P0016", 
         "name": "E-commerce Website", 
         "client_name": "Charlie Brown", 
         "client_phone": "1239874560", 
         "client_email": "charlie@example.com", 
         "description": "Developing an e-commerce platform", 
         "end_date": "2025-05-10", 
         "commission": 5000.00, 
         "employee_id": "E001"},
        
        {"id": "P0017", "name": "CRM System", "client_name": "Sophia Johnson", "client_phone": "7896541230", "client_email": "sophia@example.com", "description": "Building a customer management system", "end_date": "2025-06-15", "commission": 7000.00, "employee_id": "E001"},
        {"id": "P0018", "name": "Inventory App", "client_name": "Michael Scott", "client_phone": "9874563210", "client_email": "michael@example.com", "description": "Developing an inventory tracking app", "end_date": "2025-07-20", "commission": 6000.00, "employee_id": "E001"},
        {"id": "P0019", "name": "Social Media Tool", "client_name": "Emma Watson", "client_phone": "3216549870", "client_email": "emma@example.com", "description": "A marketing automation tool", "end_date": "2025-08-01", "commission": 8000.00, "employee_id": "E001"},
        {"id": "P0020", "name": "Blockchain Wallet", "client_name": "James Carter", "client_phone": "4569873210", "client_email": "james@example.com", "description": "A secure cryptocurrency wallet", "end_date": "2025-09-12", "commission": 9000.00, "employee_id": "E001"},
    ]
    
    for project in projects:
        ops.insert_project(project)
    print("Projects inserted successfully!")


    # Close connection
    ops.close_connection()
