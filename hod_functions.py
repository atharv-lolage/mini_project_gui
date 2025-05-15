from utils import load_data, save_data
from datetime import datetime

def view_leave_requests(username, users):
    print("\nView Leave Requests")
    leave_requests = load_data("leave_requests.json")
    hod_dept = users[username].get("dept")
    today = datetime.today().date()

    # Filter upcoming leave requests
    upcoming = {tid: req for tid, req in leave_requests.items()
                if users.get(tid, {}).get("dept") == hod_dept
                and _parse_date(req.get("date")) > today}

    if not upcoming:
        print("No upcoming leave requests for your department.")
        return

    print(f"Upcoming Leave Requests (as of {today}):")
    for tid, req in upcoming.items():
        print(f"\nTeacher: {tid}")
        print(f"  Type    : {req.get('type')}")
        print(f"  From    : {req.get('date')}")
        print(f"  Duration: {req.get('duration')} days")
        print(f"  Reason  : {req.get('reason')}")
        print(f"  Status  : {req.get('status')}")

def approve_deny_leave(username, users):
    print("\nApprove/Deny Leave Requests")
    leave_requests = load_data("leave_requests.json")
    hod_dept = users[username].get("dept")
    today = datetime.today().date()

    # Filter pending & upcoming leave requests
    pending = {tid: req for tid, req in leave_requests.items()
               if users.get(tid, {}).get("dept") == hod_dept
               and req.get("status", "").lower() == "pending"
               and _parse_date(req.get("date")) > today}

    if not pending:
        print("No pending upcoming leave requests.")
        return

    print("Pending Upcoming Requests:")
    for tid, req in pending.items():
        print(f"{tid}: {req['type']} on {req['date']} ({req['duration']} days)")

    choice = input("Enter teacher username to process: ").strip()
    if not choice or choice not in pending:
        print("Error: Invalid selection.")
        return

    action = input("Approve or Deny? (A/D): ").strip().lower()
    if action == 'a':
        leave_requests[choice]['status'] = 'Approved'
        print(f"Leave for {choice} approved.")
    elif action == 'd':
        leave_requests[choice]['status'] = 'Denied'
        print(f"Leave for {choice} denied.")
    else:
        print("No changes made.")
        return

    save_data(leave_requests, "leave_requests.json")

def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return datetime.min.date()
