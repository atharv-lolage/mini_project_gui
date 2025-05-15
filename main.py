import tkinter as tk
from tkinter import messagebox
from admin_functions import add_hod, add_teacher, view_roles_table, manage_user
from hod_functions   import view_leave_requests, approve_deny_leave
from teacher_functions import apply_leave, check_leave_status
from utils import load_data

def main():
    root = tk.Tk()
    root.title("Leave Management System")
    root.geometry("400x350")

    users = load_data("users.json")
    current_user = {'username': None, 'role': None}

    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    def build_login():
        clear_screen()
        tk.Label(root, text="Username:").pack(pady=5)
        entry_username = tk.Entry(root)
        entry_username.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        entry_password = tk.Entry(root, show="*")
        entry_password.pack(pady=5)

        # Create a frame for Role label and dropdown
        role_frame = tk.Frame(root)
        role_frame.pack(pady=5)
        tk.Label(role_frame, text="Role:").pack(side=tk.LEFT, padx=5)
        role_var = tk.StringVar(value="hod")  # Default role
        role_dropdown = tk.OptionMenu(role_frame, role_var, "hod", "teacher", "admin")
        role_dropdown.pack(side=tk.LEFT)

        tk.Button(root, text="Login", width=20,
                  command=lambda: login_role(
                      role_var.get(),
                      entry_username.get().strip(),
                      entry_password.get().strip()
                  )).pack(pady=10)

    def login_role(role, uname, pwd):
        # Admin login
        if role == 'admin':
            if uname == 'admin' and pwd == 'admin_pass':
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                current_user.update(username=uname, role=role)
                show_admin_menu()
            else:
                messagebox.showerror("Login Failed", "Invalid Admin credentials.")
        # HOD/Teacher login
        else:
            user = users.get(uname)
            if user and user['password'] == pwd and user['role'] == role:
                messagebox.showinfo("Login Successful",
                                    f"Welcome {user['name']}!\nRole: {role.capitalize()}")
                current_user.update(username=uname, role=role)
                if role == 'hod':
                    show_hod_menu()
                else:
                    show_teacher_menu()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_admin_menu():
        clear_screen()
        tk.Label(root, text="Admin Dashboard",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="1. Add HOD",            width=25,
                  command=lambda: add_hod(users)).pack(pady=5)
        tk.Button(root, text="2. Add Teacher",        width=25,
                  command=lambda: add_teacher(users)).pack(pady=5)
        tk.Button(root, text="3. View HODs & Teachers", width=25,
                  command=lambda: view_roles_table(users)).pack(pady=5)
        tk.Button(root, text="4. View Department-wise Roles", width=25,
                  command=lambda: view_department_roles(users)).pack(pady=5)
        tk.Button(root, text="5. Manage User",        width=25,
                  command=lambda: manage_user(users)).pack(pady=5)
        tk.Button(root, text="6. Logout",             width=25,
                  command=build_login).pack(pady=5)

    def view_department_roles(users):
        clear_screen()
        tk.Label(root, text="Department-wise Roles",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Organize users by department
        departments = {}
        for username, user in users.items():
            dept = user.get("dept", "Unknown")
            if dept not in departments:
                departments[dept] = []
            departments[dept].append((username, user.get("name", ""), user.get("role", "").capitalize()))

        # Display in tabular format
        for dept, members in departments.items():
            tk.Label(root, text=f"Department: {dept}", font=("Arial", 12, "bold")).pack(pady=5)
            table_frame = tk.Frame(root)
            table_frame.pack(pady=5)
            tk.Label(table_frame, text="Username", width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
            tk.Label(table_frame, text="Name", width=25, borderwidth=1, relief="solid").grid(row=0, column=1)
            tk.Label(table_frame, text="Role", width=10, borderwidth=1, relief="solid").grid(row=0, column=2)
            for i, (username, name, role) in enumerate(members, start=1):
                tk.Label(table_frame, text=username, width=15, borderwidth=1, relief="solid").grid(row=i, column=0)
                tk.Label(table_frame, text=name, width=25, borderwidth=1, relief="solid").grid(row=i, column=1)
                tk.Label(table_frame, text=role, width=10, borderwidth=1, relief="solid").grid(row=i, column=2)

        tk.Button(root, text="Back", width=20, command=show_admin_menu).pack(pady=10)

    def show_hod_menu():
        clear_screen()
        tk.Label(root, text="HOD Dashboard",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="1. View Leave Requests", width=25,
                  command=lambda: view_leave_requests(current_user['username'], users)
                  ).pack(pady=5)
        tk.Button(root, text="2. Approve/Deny Leave",  width=25,
                  command=lambda: approve_deny_leave(current_user['username'], users)
                  ).pack(pady=5)
        tk.Button(root, text="3. Logout",              width=25,
                  command=build_login).pack(pady=5)

    def show_teacher_menu():
        clear_screen()
        tk.Label(root, text="Teacher Dashboard",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="1. Apply for Leave",    width=25,
                  command=lambda: apply_leave(current_user['username'], users)
                  ).pack(pady=5)
        tk.Button(root, text="2. Check Leave Status", width=25,
                  command=lambda: check_leave_status(current_user['username'])
                  ).pack(pady=5)
        tk.Button(root, text="3. Logout",             width=25,
                  command=build_login).pack(pady=5)

    # Start with the Login screen
    build_login()
    root.mainloop()

if __name__ == "__main__":
    main()
