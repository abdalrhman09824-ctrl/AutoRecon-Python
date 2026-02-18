# AutoRecon - Python Recon Tool

## Description
AutoRecon is a Python-based reconnaissance tool for penetration testing. It gathers key information about a target to assist in penetration testing.

## Features
- Validate domain/IP input
- Resolve domain to IP address
- Reverse DNS lookup
- Scan open ports (20-1024) using threading for speed
- Banner grabbing to detect service types and versions
- Optional report saving
- Ctrl+C interrupt support

## Usage
1. Run `autorecon.py`
2. Enter target domain or IP
3. Wait for scan to complete
4. Optionally save the report

## Example Output
Target: example.com
IP: 93.184.216.34
Reverse DNS: example.com
Open Ports & Banners:
22 - SSH-2.0-OpenSSH_7.6p1 Ubuntu
80 - HTTP/1.1 500 Internal Server Error

Report saved: example.com_recon_report.txt

## Technologies
- Python
- Socket module
- Threading
