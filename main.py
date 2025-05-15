from admin_functions import add_hod, add_teacher, view_roles_table, manage_user
from hod_functions import view_leave_requests, approve_deny_leave
from teacher_functions import apply_leave, check_leave_status
from utils import load_data

def main():
    users = load_data("users.json")
    current_user = {'username': None, 'role': None}

    def login():
        print("Login")
        uname = input("Enter Username: ").strip()
        pwd = input("Enter Password: ").strip()
        role = input("Enter Role (admin/hod/teacher): ").strip()

        # Admin login
        if role == 'admin':
            if uname == 'admin' and pwd == 'admin_pass':
                print("Login Successful! Welcome Admin!")
                current_user.update(username=uname, role=role)
                show_admin_menu()
            else:
                print("Login Failed: Invalid Admin credentials.")
        # HOD/Teacher login
        else:
            user = users.get(uname)
            if user and user['password'] == pwd and user['role'] == role:
                print(f"Login Successful! Welcome {user['name']} (Role: {role.capitalize()})")
                current_user.update(username=uname, role=role)
                if role == 'hod':
                    show_hod_menu()
                else:
                    show_teacher_menu()
            else:
                print("Login Failed: Invalid username or password.")

    def show_admin_menu():
        while True:
            print("\nAdmin Dashboard")
            print("1. Add HOD")
            print("2. Add Teacher")
            print("3. View HODs & Teachers")
            print("4. Manage User")
            print("5. Logout")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                add_hod(users)
            elif choice == '2':
                add_teacher(users)
            elif choice == '3':
                view_roles_table(users)
            elif choice == '4':
                manage_user(users)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def show_hod_menu():
        while True:
            print("\nHOD Dashboard")
            print("1. View Leave Requests")
            print("2. Approve/Deny Leave")
            print("3. Logout")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                view_leave_requests(current_user['username'], users)
            elif choice == '2':
                approve_deny_leave(current_user['username'], users)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def show_teacher_menu():
        while True:
            print("\nTeacher Dashboard")
            print("1. Apply for Leave")
            print("2. Check Leave Status")
            print("3. Logout")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                apply_leave(current_user['username'], users)
            elif choice == '2':
                check_leave_status(current_user['username'])
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    # Start with the Login screen
    login()

if __name__ == "__main__":
    main()
