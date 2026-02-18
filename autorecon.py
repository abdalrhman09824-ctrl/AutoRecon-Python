import socket
from datetime import datetime
from threading import Thread, Lock

print("=== AutoRecon - Professional ===")

# Loop to repeat input until valid
while True:
    target = input("Enter target domain or IP: ")
    try:
        target_ip = socket.gethostbyname(target)
        break
    except:
        print("Error: Invalid domain or IP. Please try again.\n")

# Reverse DNS Lookup
try:
    reverse_dns = socket.gethostbyaddr(target_ip)[0]
except:
    reverse_dns = "N/A"

print(f"\nTarget: {target}")
print(f"IP: {target_ip}")
print(f"Reverse DNS: {reverse_dns}\n")

# Port scan range
start_port = 20
end_port = 1024
open_ports = []
lock = Lock()

print("Scanning ports... (Press Ctrl+C to stop anytime)")

# Function to scan a single port + banner grabbing
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            banner = "Unknown"
            try:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                pass

            with lock:
                open_ports.append((port, banner))
                print(f"[OPEN] Port {port} | {banner[:50]}")  # Show first 50 characters only

        sock.close()
    except:
        pass

# Create threads for each port
threads = []
try:
    for port in range(start_port, end_port + 1):
        t = Thread(target=scan_port, args=(port,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

except KeyboardInterrupt:
    print("\nScan stopped by user.")

# Ask user if they want to save the report (input validation)
while True:
    save_report = input("\nDo you want to save the report? (y/n): ").lower()
    if save_report in ['y', 'n']:
        break
    else:
        print("Invalid input! Please enter 'y' or 'n'.")

# Save report if user chooses 'y'
if save_report == 'y':
    report_file = f"{target}_recon_report.txt"
    with open(report_file, "w") as f:
        f.write(f"=== AutoRecon v4 Report ===\n")
        f.write(f"Target: {target}\n")
        f.write(f"IP: {target_ip}\n")
        f.write(f"Reverse DNS: {reverse_dns}\n")
        f.write(f"Scan Date: {datetime.now()}\n\n")
        f.write("Open Ports & Banners:\n")
        for port, banner in open_ports:
            f.write(f"{port} - {banner}\n")
    print(f"\nReport saved: {report_file}")
else:
    print("\nReport not saved.")

input("Press Enter to exit...")
