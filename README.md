<img width="815" height="235" alt="image" src="https://github.com/user-attachments/assets/63bda267-4941-49ba-a80b-02b3f28edb73" />

<div align="center">
  <b>ADVANCED OSINT, RECONNAISSANCE & DEVICE FINGERPRINTING FRAMEWORK</b>
  <br><br>

  <a href="https://github.com/trmxvibs/ip-tracker">
    <img src="https://img.shields.io/badge/Language-Python_3-14354C?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://github.com/trmxvibs/ip-tracker">
    <img src="https://img.shields.io/badge/Platform-Linux_|_Windows_|_Termux-000000?style=for-the-badge&logo=linux&logoColor=white" alt="Platform">
  </a>
  <a href="https://github.com/trmxvibs/ip-tracker/releases">
    <img src="https://img.shields.io/badge/Version-1.0-red?style=for-the-badge" alt="Version">
  </a>
  <a href="https://github.com/trmxvibs">
    <img src="https://img.shields.io/github/repo-size/trmxvibs/ip-tracker?color=orange&style=for-the-badge&logo=github" alt="Size">
  </a>
  <a href="https://github.com/trmxvibs/ip-tracker/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  </a>

  <br><br>

  <p>
    <b>Ip-tracker (Chakravyuh)</b> is a reconnaissance tool designed for red teaming and authorized security research.
    It combines passive OSINT capabilities with active social engineering modules to extract precise target data.
    <br><br>
    Features <b>Auto-Tunneling</b>, <b>Telegram Real-time Alerts</b>, and <b>Advanced Device Fingerprinting</b>
    without requiring manual port forwarding.
  </p>
</div>

---

## CORE CAPABILITIES

| MODULE | DESCRIPTION |
|--------|-------------|
| **IP INTELLIGENCE** | Geo-locate targets with map generation. Integrates Shodan to detect OS, open ports, and vulnerabilities. |
| **DEVICE TRAPPER** | Deploys social engineering pages (Fake Cloudflare / Update). Captures GPU model, CPU, RAM, battery, network type, and timezone. |
| **PHONE RECON** | Validates phone numbers and extracts carrier, location, and timezone information globally. |
| **PORT SCANNER** | Multi-threaded active scan for critical open ports (21, 22, 80, 443, 3389, etc.). |
| **DOMAIN INTEL** | Resolves host IPs and enumerates subdomains via Shodan DNS database. |
| **REAL-TIME ALERTS** | Sends captured victim details instantly to your Telegram bot. |
| **AUTO-TUNNELING** | Built-in support for Cloudflared and Serveo. No manual configuration needed. |

---

## INSTALLATION

### AUTO-INSTALLER INCLUDED
Upon first launch, the tool automatically installs missing dependencies (`shodan`, `folium`, `phonenumbers`, etc.).

---

### [TERMUX (ANDROID)]

```bash
# Update repositories
pkg update && pkg upgrade -y

# Install dependencies
pkg install python git openssh -y

# Clone repository
git clone https://github.com/trmxvibs/ip-tracker

# Navigate and run
cd ip-tracker
python chakravyuh.py
```


###  - KALI LINUX / UBUNTU - 
```bash
# Update system
sudo apt update

# Install dependencies
sudo apt install python3 python3-pip git -y

# Clone repository
git clone https://github.com/trmxvibs/ip-tracker

# Navigate and run
cd ip-tracker
python3 chakravyuh.py
```
### WINDOWS

Download and install Python 3.x (check “Add to PATH”).

Download this repository.

Open CMD inside the folder.
Run
```sh
python chakravyuh.py
```

<div align="center">

##  MENU OVERVIEW

</div>

---

> ### **[1] IP Tracker**
> Enter any IP address to retrieve city, country, ISP, and map file (`.html`).  
> *If Shodan API is active, it also fetches vulnerabilities and ports.*

> ### **[2] Port Scanner**
> Checks for open ports on the target IP (FTP, SSH, Telnet, HTTP, HTTPS, SMB, RDP, etc.).

> ### **[3] Phone Number Tracker**
> Enter number with country code (example: `+919876543210`).  
> Returns valid carrier, region, and timezone data.

> ### **[4] Domain Intel**
> Resolves domain names to IP addresses and lists subdomains found in public databases.

> ### **[5] Device Trapper (Honeypot)**
> Hosts a fake page (Cloudflare / System Update) via secure tunnel.

---

### Captures:
---
- GPU model
- Battery percentage
- Screen resolution
- Browser
- Public IP
---
### Logs:

- Saves data to loot_log.txt

### Alerts:

- Sends captured data to Telegram.

> ### **[6] Settings**

- Configure API keys:

- Shodan API Key — for deep reconnaissance

- Telegram Bot Token & Chat ID — receive captured data alerts

## PREVIEW

<img width="1315" height="911" alt="image" src="https://github.com/user-attachments/assets/4e022d9d-f0ca-40e4-857a-8f2654a3b1e8" />

## LEGAL DISCLAIMER
---
# CRITICAL WARNING
---
**This repository and the code provided are for educational purposes and authorized security research only.
The developer (Lokesh Kumar) assumes no liability and is not responsible for any misuse or damage caused by this program.
Using this tool to track or exploit targets without prior mutual consent may be illegal.
It is the end user's responsibility to obey all applicable local, state, and federal laws.**


<div align="center"> <b>Project maintained by <a href="https://github.com/trmxvibs">trmxvibs</a></b> </div>


<!-- AUTO_TIMESTAMP Mon Feb 16 01:03:04 UTC 2026 -->
