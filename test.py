import sqlite3
from datetime import datetime, timedelta

# Connect to the existing SQLite3 database
conn = sqlite3.connect("local.db")  # Replace with your actual DB file
cursor = conn.cursor()

# 🔹 Insert Employees (10 Records)
employees = [
    ("EMP001", "Alice Johnson", "123-456-7890", "alice@example.com", "pass123"),
    ("EMP002", "Bob Smith", "234-567-8901", "bob@example.com", "pass123"),
    ("EMP003", "Charlie Brown", "345-678-9012", "charlie@example.com", "pass123"),
    ("EMP004", "David Wilson", "456-789-0123", "david@example.com", "pass123"),
    ("EMP005", "Emma Davis", "567-890-1234", "emma@example.com", "pass123"),
    ("EMP006", "Frank Thomas", "678-901-2345", "frank@example.com", "pass123"),
    ("EMP007", "Grace Lee", "789-012-3456", "grace@example.com", "pass123"),
    ("EMP008", "Henry Moore", "890-123-4567", "henry@example.com", "pass123"),
    ("EMP009", "Isabel White", "901-234-5678", "isabel@example.com", "pass123"),
    ("EMP010", "Jack Martin", "012-345-6789", "jack@example.com", "pass123"),
]

cursor.executemany("INSERT INTO employees (id, name, phone, email, password) VALUES (?, ?, ?, ?, ?)", employees)
conn.commit()

# 🔹 Insert Freelancers (10 Records)
freelancers = [
    ("FR001", "Liam Walker", "111-222-3333", "liam@example.com"),
    ("FR002", "Mia Clark", "222-333-4444", "mia@example.com"),
    ("FR003", "Noah Scott", "333-444-5555", "noah@example.com"),
    ("FR004", "Olivia Hall", "444-555-6666", "olivia@example.com"),
    ("FR005", "Peter Adams", "555-666-7777", "peter@example.com"),
    ("FR006", "Quinn Nelson", "666-777-8888", "quinn@example.com"),
    ("FR007", "Rachel Carter", "777-888-9999", "rachel@example.com"),
    ("FR008", "Samuel Green", "888-999-0000", "samuel@example.com"),
    ("FR009", "Tina Harris", "999-000-1111", "tina@example.com"),
    ("FR010", "Umar Brooks", "000-111-2222", "umar@example.com"),
]

cursor.executemany("INSERT INTO freelancers (id, name, phone, email) VALUES (?, ?, ?, ?)", freelancers)
conn.commit()

# 🔹 Insert Projects (40 Total)
project_statuses = {
    "late": -5,        # 10 projects with past deadlines
    "today": 0,        # 10 projects due today
    "tomorrow": 1,     # 10 projects due tomorrow
    "pending": 7       # 10 projects due in future (pending)
}

projects = []
project_id = 1

for status, days_offset in project_statuses.items():
    for i in range(10):
        proj_name = f"Project {status.capitalize()} {i+1}"
        client_name = f"Client {i+1}"
        client_phone = f"555-000-{1000+i}"
        client_email = f"client{i+1}@example.com"
        description = f"This is a {status} project description."
        end_date = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")  # Ensures YYYY-MM-DD format
        commission = 1000 + (i * 100)
        employee_id = employees[i % len(employees)][0]  # Assign employees in round-robin fashion
        status_flag = 0  # All projects start as pending (status = 0)

        projects.append((f"PROJ{project_id:03d}", proj_name, client_name, client_phone, client_email, description, end_date, commission, employee_id, status_flag))
        project_id += 1

cursor.executemany(
    "INSERT INTO projects (id, name, client_name, client_phone, client_email, description, end_date, commission, employee_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    projects
)
conn.commit()

print("✅ Hardcoded data inserted successfully!")

# Close the database connection
conn.close()
