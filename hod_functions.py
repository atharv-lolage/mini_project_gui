import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from datetime import datetime
from utils import load_data, save_data

# Display upcoming leave requests for this HOD's department
def view_leave_requests(username, users):
    leave_requests = load_data("leave_requests.json")
    hod_dept = users[username].get("dept")
    today = datetime.today().date()

    # Filter upcoming
    upcoming = {tid: req for tid, req in leave_requests.items()
                if users.get(tid, {}).get("dept") == hod_dept
                and _parse_date(req.get("date")) > today}

    if not upcoming:
        messagebox.showinfo("Leave Requests", "No upcoming leave requests for your department.")
        return

    # Prepare display text
    lines = [f"Upcoming Leave Requests (as of {today}):", ""]
    for tid, req in upcoming.items():
        lines.append(f"Teacher: {tid}")
        lines.append(f"  Type    : {req.get('type')}")
        lines.append(f"  From    : {req.get('date')}")
        lines.append(f"  Duration: {req.get('duration')} days")
        lines.append(f"  Reason  : {req.get('reason')}")
        lines.append(f"  Status  : {req.get('status')}")
        lines.append("------")

    _show_text_window("Upcoming Requests", "\n".join(lines))

# Approve or deny a pending upcoming leave request
def approve_deny_leave(username, users):
    leave_requests = load_data("leave_requests.json")
    hod_dept = users[username].get("dept")
    today = datetime.today().date()

    # Filter pending & upcoming
    pending = {tid: req for tid, req in leave_requests.items()
               if users.get(tid, {}).get("dept") == hod_dept
               and req.get("status", "").lower() == "pending"
               and _parse_date(req.get("date")) > today}

    if not pending:
        messagebox.showinfo("Approve/Deny", "No pending upcoming leave requests.")
        return

    # Show pending list
    lines = ["Pending Upcoming Requests:", ""]
    for tid, req in pending.items():
        lines.append(f"{tid}: {req['type']} on {req['date']} ({req['duration']} days)")
    _show_text_window("Pending Requests", "\n".join(lines))

    # Ask for selection
    choice = simpledialog.askstring("Select Request", "Enter teacher username to process:")
    if not choice or choice not in pending:
        messagebox.showerror("Error", "Invalid selection.")
        return

    action = simpledialog.askstring("Action", "Approve or Deny? (A/D):")
    if not action:
        return
    action = action.strip().lower()
    if action == 'a':
        leave_requests[choice]['status'] = 'Approved'
        messagebox.showinfo("Success", f"Leave for {choice} approved.")
    elif action == 'd':
        leave_requests[choice]['status'] = 'Denied'
        messagebox.showinfo("Success", f"Leave for {choice} denied.")
    else:
        messagebox.showinfo("No Action", "No changes made.")
        return

    save_data(leave_requests, "leave_requests.json")

# Utility: parse date string to date, default far past if invalid

def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return datetime.min.date()

# Show scrollable text window
def _show_text_window(title, text):
    win = tk.Toplevel()
    win.title(title)
    txt = scrolledtext.ScrolledText(win, width=60, height=20)
    txt.pack(padx=10, pady=10)
    txt.insert(tk.END, text)
    txt.configure(state='disabled')
    tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
