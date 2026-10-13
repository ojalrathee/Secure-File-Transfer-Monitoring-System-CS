# Secure File Transfer Monitoring System

Hey there! This is my cybersecurity internship project. Basically, it's a lightweight Python tool that watches folders, logs file transfers, checks for file tampering using SHA-256 hashes, and shouts alerts if someone moves sensitive files where they aren't supposed to go (like a random USB or external folder).

---

## What does it actually do?
- **File Logging:** Keeps track of when files are created, moved, or modified.
- **Integrity Checks:** Generates SHA-256 hashes so you can tell if a file got messed with or corrupted.
- **Unauthorized Movement Detection:** Triggers an alert if sensitive extensions (like `.env`, `.pem`, `.xlsx`) get dumped into restricted folders.
- **Audit Trail:** Dumps everything into an `audit_trail.log` file so you have proof.

---

## Project Structure
```text
secure_file_monitor/
│
├── monitor.py      # The main engine watching the folder
├── integrity.py    # Handles the SHA-256 hashing logic
├── logger.py       # Handles console colors and writing to audit_trail.log
└── monitored_folder/ # The sandbox folder being watched
```

---

## How to Run It (Quick Setup)

**1. Clone or download this repo & open your terminal inside the folder:**
```bash
cd secure_file_monitor
```

**2. Install dependencies:**
You only need `watchdog` for tracking file system events.
```bash
pip install watchdog psutil
```

**3. Run the script:**
```bash
python monitor.py
```
*It will automatically create a folder called `monitored_folder`. Drop some files in there, move them around, and watch the terminal work its magic!*

---

## Testing it out
1. Run `python monitor.py`.
2. Drop a regular text file inside `monitored_folder` -> Check the console for the hash log.
3. Make a subfolder named `external_usb` inside `monitored_folder`.
4. Drop a file named `config.env` in there and drag it into the USB folder -> **Boom! Red alert.**

---

## Tech Stack
- **Python** (Cuz it's awesome and fast to write)
- **Watchdog library** (For real-time file system monitoring)
- **Hashlib** (For SHA-256 integrity checksums)

Feel free to fork or use this as a base for your own security projects! Peace out. ✌️