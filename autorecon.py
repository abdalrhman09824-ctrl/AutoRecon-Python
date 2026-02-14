import socket
import argparse
import threading
import random
import time

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

open_ports = []
lock = threading.Lock()


def show_banner():
    print("""
========================
       AutoRecon
========================
Fast Recon Tool
""")


def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except:
        return None


def grab_service_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))

        try:
            s.send(b"GET / HTTP/1.0\r\n\r\n")
        except:
            pass

        data = s.recv(1024).decode(errors="ignore")
        s.close()

        return data.split("\n")[0] if data else ""
    except:
        return ""


def check_vuln(port, banner):
    issues = []

    if port == 21:
        issues.append("FTP (weak security)")
    if port == 23:
        issues.append("Telnet (unencrypted)")
    if "Apache/2.2" in banner:
        issues.append("Old Apache (possible CVE)")
    if "OpenSSH_5" in banner:
        issues.append("Old SSH version")

    return issues


def scan_port(ip, port):
    try:
        time.sleep(random.uniform(0.05, 0.3))  # stealth delay

        s = socket.socket()
        s.settimeout(1)

        if s.connect_ex((ip, port)) == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            banner = grab_service_banner(ip, port)
            vulns = check_vuln(port, banner)

            with lock:
                open_ports.append((port, service, banner, vulns))

        s.close()

    except:
        pass


def run_scan(ip):
    threads = []

    for port in COMMON_PORTS:
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True)
    args = parser.parse_args()

    show_banner()

    ip = resolve_target(args.target)
    if not ip:
        print("[-] Invalid target")
        return

    print(f"[+] Target: {args.target}")
    print(f"[+] IP: {ip}\n")

    print("[+] Scanning (fast & stealth)...\n")
    run_scan(ip)

    results = sorted(open_ports)

    print("==== RESULTS ====")
    for port, service, banner, vulns in results:
        print(f"{port}/tcp - {service}")

        if banner:
            print(f"  -> {banner}")

        for v in vulns:
            print(f"  [!] {v}")

        print()


if __name__ == "__main__":
    main()
