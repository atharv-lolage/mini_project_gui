from utils import save_data, calculate_age

def add_hod(users):
    print("\nAdd HOD")
    username = input("Enter Username: ").strip()
    if username in users:
        print("Error: Username already exists.")
        return
    password = input("Enter Password: ").strip()
    name = input("Enter Full Name: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    qualification = input("Enter Qualification: ").strip()
    dept = input("Enter Department: ").strip()
    doj = input("Enter Date of Joining (YYYY-MM-DD): ").strip()
    address = {}
    print("Enter Address (key: value format, one per line, blank line to finish):")
    while True:
        line = input().strip()
        if not line:
            break
        key, value = line.split(":")
        address[key.strip()] = value.strip()

    try:
        age = calculate_age(dob)
    except ValueError:
        print("Error: Invalid date format for DOB. Use YYYY-MM-DD.")
        return

    users[username] = {
        'role': 'hod',
        'password': password,
        'name': name,
        'dob': dob,
        'age': age,
        'qualification': qualification,
        'dept': dept,
        'doj': doj,
        'address': address
    }
    save_data(users, 'users.json')
    print(f"Success: HOD '{username}' added.")

def add_teacher(users):
    print("\nAdd Teacher")
    username = input("Enter Username: ").strip()
    if username in users:
        print("Error: Username already exists.")
        return
    password = input("Enter Password: ").strip()
    name = input("Enter Full Name: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    qualification = input("Enter Qualification: ").strip()
    dept = input("Enter Department: ").strip()
    doj = input("Enter Date of Joining (YYYY-MM-DD): ").strip()
    subjects = input("Enter Subjects (comma-separated): ").strip()
    address = {}
    print("Enter Address (key: value format, one per line, blank line to finish):")
    while True:
        line = input().strip()
        if not line:
            break
        key, value = line.split(":")
        address[key.strip()] = value.strip()

    try:
        age = calculate_age(dob)
    except ValueError:
        print("Error: Invalid date format for DOB. Use YYYY-MM-DD.")
        return

    users[username] = {
        'role': 'teacher',
        'password': password,
        'name': name,
        'dob': dob,
        'age': age,
        'qualification': qualification,
        'dept': dept,
        'doj': doj,
        'subjects': [s.strip() for s in subjects.split(',')],
        'address': address
    }
    save_data(users, 'users.json')
    print(f"Success: Teacher '{username}' added.")

def view_roles_table(users):
    print("\n--- HODs ---")
    hods = [f"{u} | {d.get('name','')} | {d.get('dept','')} | {d.get('qualification','')}" for u, d in users.items() if d.get('role') == 'hod']
    print("\n".join(hods) if hods else "(none)")
    print("\n--- Teachers ---")
    teachers = [f"{u} | {d.get('name','')} | {d.get('dept','')} | {d.get('qualification','')}" for u, d in users.items() if d.get('role') == 'teacher']
    print("\n".join(teachers) if teachers else "(none)")

def manage_user(users):
    print("\nManage User")
    username = input("Enter Username: ").strip()
    user = users.get(username)
    if not user:
        print("Error: User not found.")
        return

    print("\nUser Details:")
    for key, value in user.items():
        if key == "address":
            print(f"{key.capitalize()}:")
            for k, v in value.items():
                print(f"  {k.capitalize()}: {v}")
        else:
            print(f"{key.capitalize()}: {value}")

    print("\nOptions:")
    print("1. Update User")
    print("2. Delete User")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        for key in user.keys():
            if key == "address":
                print("Update Address (key: value format, one per line, blank line to finish):")
                address = {}
                while True:
                    line = input().strip()
                    if not line:
                        break
                    k, v = line.split(":")
                    address[k.strip()] = v.strip()
                user[key] = address
            else:
                user[key] = input(f"Enter new value for {key.capitalize()} (leave blank to keep current): ").strip() or user[key]
        save_data(users, "users.json")
        print(f"Success: User '{username}' updated.")
    elif choice == '2':
        del users[username]
        save_data(users, "users.json")
        print(f"Success: User '{username}' deleted.")
    else:
        print("Invalid choice.")
