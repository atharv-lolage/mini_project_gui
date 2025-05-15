from utils import load_data, save_data
from datetime import datetime

def apply_leave(username, users):
    print("\nApply for Leave")
    leave_requests = load_data("leave_requests.json")

    req_type = input("Enter leave type (sick/annual): ").strip()
    date_str = input("Enter start date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid date format.")
        return
    duration = input("Enter duration (days): ").strip()
    if not duration.isdigit() or int(duration) <= 0:
        print("Error: Duration must be a positive integer.")
        return
    reason = input("Enter reason: ").strip()

    leave_requests[username] = {
        "type": req_type,
        "date": date_str,
        "duration": int(duration),
        "reason": reason,
        "status": "Pending"
    }
    save_data(leave_requests, "leave_requests.json")
    print("Success: Leave request submitted.")

def check_leave_status(username):
    print("\nCheck Leave Status")
    leave_requests = load_data("leave_requests.json")
    req = leave_requests.get(username)
    if not req:
        print("No leave request found.")
        return
    print("\nLeave Request Details:")
    print(f"Type: {req.get('type')}")
    print(f"Date: {req.get('date')}")
    print(f"Duration: {req.get('duration')} days")
    print(f"Reason: {req.get('reason')}")
    print(f"Status: {req.get('status')}")
