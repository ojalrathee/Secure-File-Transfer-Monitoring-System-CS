import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from integrity import calculate_sha256
from logger import log_event

# Configuration
SENSITIVE_EXTENSIONS = ['.env', '.pem', '.kdbx', '.docx', '.xlsx']
RESTRICTED_KEYWORDS = ['usb', 'external', 'public', 'unauthorized']

class SecurityFileHandler(FileSystemEventHandler):
    def on_moved(self, event):
        if event.is_directory:
            return
        
        src = event.src_path
        dest = event.dest_path
        
        log_event("FILE_MOVED", f"From {src} To {dest}", severity="INFO")
        
        # Security rules
        file_ext = os.path.splitext(dest)[1].lower()
        is_sensitive = file_ext in SENSITIVE_EXTENSIONS
        is_restricted_target = any(keyword in dest.lower() for keyword in RESTRICTED_KEYWORDS)
        
        if is_sensitive and is_restricted_target:
            log_event("POLICY_VIOLATION", f"Sensitive file '{os.path.basename(dest)}' moved to restricted target: {dest}", severity="ALERT")
            
        # Verify file integrity hash post-transfer
        file_hash = calculate_sha256(dest)
        if file_hash:
            log_event("INTEGRITY_CHECK", f"SHA-256 for {os.path.basename(dest)}: {file_hash}", severity="INFO")

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        file_hash = calculate_sha256(file_path)
        log_event("FILE_CREATED", f"New file added: {file_path} [Hash: {file_hash}]", severity="INFO")

if __name__ == "__main__":
    monitored_dir = "./monitored_folder"
    os.makedirs(monitored_dir, exist_ok=True)
    
    event_handler = SecurityFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=monitored_dir, recursive=True)
    
    print(f"secure file transfer monitoring system active.")
    print(f"Watching directory: {os.path.abspath(monitored_dir)}")
    print(f"Ctrl + C to stop.\n")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()