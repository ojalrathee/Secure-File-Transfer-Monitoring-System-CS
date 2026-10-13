import datetime
import os

LOG_FILE = "audit_trail.log"

def log_event(event_type, details, severity="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{severity}] {event_type}: {details}"
    
    # Print to console with color/formatting cues
    if severity == "ALERT":
        print(f"\033[91m{log_entry}\033[0m")  # Red text for alerts
    else:
        print(f"\033[92m{log_entry}\033[0m")  # Green text for normal logs

    # Save to file for your audit report deliverable
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")