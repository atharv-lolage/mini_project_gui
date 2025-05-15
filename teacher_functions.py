import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
def load_data(filename):
    import json, os
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Apply for leave dialog
def apply_leave(username, users):
    leave_requests = load_data("leave_requests.json")
    # Prompt details
    req_type = simpledialog.askstring("Apply Leave", "Enter leave type (sick/annual):")
    if not req_type: return
    date_str = simpledialog.askstring("Apply Leave", "Enter start date (YYYY-MM-DD):")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except:
        messagebox.showerror("Error", "Invalid date format.")
        return
    duration = simpledialog.askinteger("Apply Leave", "Enter duration (days):", minvalue=1)
    if not duration: return
    reason = simpledialog.askstring("Apply Leave", "Enter reason:")
    if not reason: return

    # Build request entry
    leave_requests[username] = {
        "type": req_type,
        "date": date_str,
        "duration": duration,
        "reason": reason,
        "status": "Pending"
    }
    save_data(leave_requests, "leave_requests.json")
    messagebox.showinfo("Success", "Leave request submitted.")

# Check leave status
def check_leave_status(username):
    leave_requests = load_data("leave_requests.json")
    req = leave_requests.get(username)
    if not req:
        messagebox.showinfo("Status", "No leave request found.")
        return
    status = req.get("status", "")
    info = (f"Type: {req.get('type')}\n"
            f"Date: {req.get('date')}\n"
            f"Duration: {req.get('duration')} days\n"
            f"Reason: {req.get('reason')}\n"
            f"Status: {status}")
    messagebox.showinfo("Leave Status", info)
