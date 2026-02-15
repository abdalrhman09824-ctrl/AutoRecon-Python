# AutoRecon

Fast and lightweight reconnaissance tool for port scanning and basic service analysis.

---

## Overview

AutoRecon is a multi-threaded Python-based reconnaissance tool designed to quickly scan common ports, detect running services, and identify potential security weaknesses.

---

## Features

* Fast port scanning (multi-threaded)
* Target resolution (domain to IP)
* Service detection for common ports
* Banner grabbing
* Basic vulnerability hints
* Stealth delay using randomized timing

---

## Usage

```bash
python auto_recon.py -t example.com
```

---

## Example Output

```
==== RESULTS ====
80/tcp - HTTP
  ↳ HTTP/1.1 200 OK

22/tcp - SSH
  [!] Old SSH version
```

---

## Notes

* Requires Python 3
* Designed for educational and authorized testing only
* Do not use without permission

---

## Author

Developed by Abdulrahman Hann
