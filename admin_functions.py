import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import datetime
from utils import save_data, calculate_age, load_data

# Helper to prompt and validate date strings
def ask_date(prompt):
    while True:
        date_str = simpledialog.askstring("Date Input", f"{prompt} (YYYY-MM-DD):")
        if date_str is None:
            return None
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")

# Display all HODs and Teachers in a popup window
def view_roles_table(users):
    root = tk.Tk()
    root.withdraw()
    text = []
    text.append("--- HODs ---")
    hods = [f"{u} | {d.get('name','')} | {d.get('dept','')} | {d.get('qualification','')}" for u,d in users.items() if d.get('role')=='hod']
    text.extend(hods if hods else ["(none)"])
    text.append("\n--- Teachers ---")
    teachers = [f"{u} | {d.get('name','')} | {d.get('dept','')} | {d.get('qualification','')}" for u,d in users.items() if d.get('role')=='teacher']
    text.extend(teachers if teachers else ["(none)"])

    # show in scrolled text
    win = tk.Toplevel()
    win.title("Roles Overview")
    txt = scrolledtext.ScrolledText(win, width=60, height=20)
    txt.pack()
    txt.insert(tk.END, "\n".join(text))
    txt.configure(state='disabled')
    tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
    root.mainloop()

# Add a new HOD via dialogs
def add_hod(users):
    def submit_form():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        name = entry_name.get().strip()
        dob = entry_dob.get().strip()
        qualification = entry_qualification.get().strip()
        dept = entry_dept.get().strip()
        doj = entry_doj.get().strip()
        address_lines = text_address.get("1.0", tk.END).strip().split("\n")
        address = {line.split(":")[0].strip().lower(): line.split(":")[1].strip() for line in address_lines if ":" in line}

        if not username or username in users:
            messagebox.showerror("Error", "Invalid or existing username.")
            return
        if not password or not name or not dob or not qualification or not dept or not doj or not address:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            age = calculate_age(dob)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format for DOB. Use YYYY-MM-DD.")
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
        messagebox.showinfo("Success", f"HOD '{username}' added.")
        form_window.destroy()

    # Create a new window for the form
    form_window = tk.Toplevel()
    form_window.title("Add HOD")

    tk.Label(form_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(form_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(form_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Full Name:").grid(row=2, column=0, padx=10, pady=5)
    entry_name = tk.Entry(form_window)
    entry_name.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
    entry_dob = tk.Entry(form_window)
    entry_dob.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Qualification:").grid(row=4, column=0, padx=10, pady=5)
    entry_qualification = tk.Entry(form_window)
    entry_qualification.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Department:").grid(row=5, column=0, padx=10, pady=5)
    entry_dept = tk.Entry(form_window)
    entry_dept.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Date of Joining (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5)
    entry_doj = tk.Entry(form_window)
    entry_doj.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Address (key: value format, one per line):").grid(row=7, column=0, padx=10, pady=5)
    text_address = tk.Text(form_window, width=40, height=5)
    text_address.grid(row=7, column=1, padx=10, pady=5)

    tk.Button(form_window, text="Submit", command=submit_form).grid(row=8, column=0, columnspan=2, pady=10)

# Add a new Teacher via dialogs
def add_teacher(users):
    def submit_form():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        name = entry_name.get().strip()
        dob = entry_dob.get().strip()
        qualification = entry_qualification.get().strip()
        dept = entry_dept.get().strip()
        doj = entry_doj.get().strip()
        subjects = entry_subjects.get().strip()
        address_lines = text_address.get("1.0", tk.END).strip().split("\n")
        address = {line.split(":")[0].strip().lower(): line.split(":")[1].strip() for line in address_lines if ":" in line}

        if not username or username in users:
            messagebox.showerror("Error", "Invalid or existing username.")
            return
        if not password or not name or not dob or not qualification or not dept or not doj or not subjects or not address:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            age = calculate_age(dob)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format for DOB. Use YYYY-MM-DD.")
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
        messagebox.showinfo("Success", f"Teacher '{username}' added.")
        form_window.destroy()

    # Create a new window for the form
    form_window = tk.Toplevel()
    form_window.title("Add Teacher")

    tk.Label(form_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(form_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(form_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Full Name:").grid(row=2, column=0, padx=10, pady=5)
    entry_name = tk.Entry(form_window)
    entry_name.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
    entry_dob = tk.Entry(form_window)
    entry_dob.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Qualification:").grid(row=4, column=0, padx=10, pady=5)
    entry_qualification = tk.Entry(form_window)
    entry_qualification.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Department:").grid(row=5, column=0, padx=10, pady=5)
    entry_dept = tk.Entry(form_window)
    entry_dept.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Date of Joining (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5)
    entry_doj = tk.Entry(form_window)
    entry_doj.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Subjects (comma-separated):").grid(row=7, column=0, padx=10, pady=5)
    entry_subjects = tk.Entry(form_window)
    entry_subjects.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Address (key: value format, one per line):").grid(row=8, column=0, padx=10, pady=5)
    text_address = tk.Text(form_window, width=40, height=5)
    text_address.grid(row=8, column=1, padx=10, pady=5)

    tk.Button(form_window, text="Submit", command=submit_form).grid(row=9, column=0, columnspan=2, pady=10)

# Manage a user (view, update, delete)
def manage_user(users):
    def view_user():
        username = entry_username.get().strip()
        user = users.get(username)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        # Format address if it exists
        address = user.get("address", {})
        if address:
            address_str = "\n".join([f"  {key.capitalize()}: {value}" for key, value in address.items()])
        else:
            address_str = "Not available"

        # Prepare user details
        details = "\n".join([
            f"{key.capitalize()}: {value}" if key != "address" else f"Address:\n{address_str}"
            for key, value in user.items()
        ])
        messagebox.showinfo("User Details", details)

    def update_user():
        username = entry_username.get().strip()
        user = users.get(username)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        def submit_update():
            for key, entry in entries.items():
                if key == "address":
                    # Parse address back into a dictionary
                    address_lines = entry.get("1.0", tk.END).strip().split("\n")
                    user[key] = {line.split(":")[0].strip().lower(): line.split(":")[1].strip() for line in address_lines if ":" in line}
                else:
                    user[key] = entry.get().strip()
            save_data(users, "users.json")
            messagebox.showinfo("Success", f"User '{username}' updated.")
            update_window.destroy()

        update_window = tk.Toplevel()
        update_window.title("Update User")
        entries = {}
        for i, (key, value) in enumerate(user.items()):
            tk.Label(update_window, text=f"{key.capitalize()}:").grid(row=i, column=0, padx=10, pady=5)
            if key == "address":
                # Use a Text widget for multi-line address input
                text_widget = tk.Text(update_window, width=40, height=5)
                if isinstance(value, dict):
                    address_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in value.items()])
                else:
                    address_text = value
                text_widget.insert(tk.END, address_text)
                text_widget.grid(row=i, column=1, padx=10, pady=5)
                entries[key] = text_widget
            else:
                entry = tk.Entry(update_window)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[key] = entry
        tk.Button(update_window, text="Submit", command=submit_update).grid(row=len(user), column=0, columnspan=2, pady=10)

    def delete_user():
        username = entry_username.get().strip()
        if username not in users:
            messagebox.showerror("Error", "User not found.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?")
        if confirm:
            del users[username]
            save_data(users, "users.json")
            messagebox.showinfo("Success", f"User '{username}' deleted.")

    # Create a new window for managing users
    manage_window = tk.Toplevel()
    manage_window.title("Manage User")

    tk.Label(manage_window, text="Enter Username:").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(manage_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(manage_window, text="View User", command=view_user).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(manage_window, text="Update User", command=update_user).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(manage_window, text="Delete User", command=delete_user).grid(row=3, column=0, columnspan=2, pady=5)
