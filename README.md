<img width="815" height="235" alt="image" src="https://github.com/user-attachments/assets/63bda267-4941-49ba-a80b-02b3f28edb73" />

<div align="center">

![CHAKRAVYUH](https://img.shields.io/badge/CHAKRAVYUH-FRAMEWORK-red?style=for-the-badge&logo=kali-linux&logoColor=white)

<br>

![Python](https://img.shields.io/badge/LANGUAGE-PYTHON_3-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/PLATFORM-LINUX_|_TERMUX_|_WINDOWS-black?style=for-the-badge&logo=linux&logoColor=white)
![Security](https://img.shields.io/badge/SECURITY-RED_TEAM-crimson?style=for-the-badge&logo=security&logoColor=white)
![License](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)

<br>

![Stars](https://img.shields.io/github/stars/trmxvibs/ip-tracker?style=for-the-badge&color=gold&label=STARS)
![Forks](https://img.shields.io/github/forks/trmxvibs/ip-tracker?style=for-the-badge&color=orange&label=FORKS)
![Size](https://img.shields.io/github/repo-size/trmxvibs/ip-tracker?style=for-the-badge&color=blue&label=SIZE)
![Maintenance](https://img.shields.io/badge/MAINTAINED-YES-success?style=for-the-badge)

</div>

---
**CHAKRAVYUH is the ultimate Offensive OSINT & Reconnaissance Framework designed for high-level penetration testing and red teaming. This is not just an IP tracker; it is a sophisticated Cyber Trap Engine.
It leverages advanced Social Engineering techniques combined with Shodan Intelligence to extract critical hardware and network data from targets. Whether you are operating on Kali Linux, Termux, or Windows, CHAKRAVYUH provides a tactical advantage in information gathering.
DOMINATE THE NETWORK. TRACK THE UNTRACKABLE.**
---

##  1.  ADVANCED GEO-INTELLIGENCE
- Precision Tracking: Extract exact Latitude/Longitude, Country, City, and Zip Codes.

- ISP Enumeration: Identify Internet Service Providers and detect VPN/Proxy usage.

- Visual Recon: Auto-generates satellite maps using Folium for real-time location visualization.

```sh
[?] Target IP: 8.8.8.8

[*] IP Analysis...
 Geo    : Ashburn, United States
 ISP    : Google LLC
 Proxy  : False
 Map    : Saved as map_8.8.8.8.html
```


## 2.  HARDWARE FINGERPRINTING (THE TRAP)
- GPU Detection: Identifies Adreno, Mali, or Apple graphics renderers to pinpoint specific mobile devices (Samsung, OnePlus, iPhone).
- System Diagnostics: Extracts CPU Core count, RAM availability, and Screen Resolution.
- Power Analysis: Detects Battery Percentage and Charging Status live.
- Stealth Tunnels: Uses Cloudflared and Serveo to create secure, anonymous HTTPS links that bypass firewalls.

<img width="1404" height="961" alt="image" src="https://github.com/user-attachments/assets/93166843-6ddc-4d0e-9a63-bbb050ec34de" />

```python
 ──────────────────────────────────────────
  █▀▄▀█ ▄▀█ █▄█ ▄▀█      ░░░ ░░░ ░░░
  █ ▀ █ █▀█  █  █▀█ v1.0
 ═══════════════════════════════════════════
 LOKESH-KUMAR | traps | recon | osint

Youtube : https://youtube.com/@termux2
Github :  https://github.com/trmxvibs
[1] IP Tracker
[2] Port Scanner
[3] Phone Number Tracker
[4] Domain Intel (DNS)
[5] Device Traper
[6] Settings
[0] Exit

chakravyuh > 5

[?] Select Trap Template:
 [1] Standard Loading
 [2] Fake Cloudflare
 [3] System Update
 > 1
[+] Local: http://localhost:27174
[*] Starting Tunnel...

 >>> LINK: https://details-meaning-with-trackback.trycloudflare.com <<<

Waiting for victims... (Ctrl+C to stop)

```



## 3.  NETWORK WARFARE
- Shodan Integration: Scans targets for Open Ports, Vulnerabilities (CVEs), and Operating System details.

- Port Scanning: Multi-threaded analysis of critical ports (FTP, SSH, HTTP, RDP).

- Domain Intel: Extracts DNS records and resolves Host IPs instantly.

```python
[?] Target IP: 135.148.100.147

[*] IP Analysis...
 Geo    : Los Angeles, United States
 ISP    : OVH SAS
 Proxy  : True
 Map    : Saved as map_135.148.100.147.html

Enter to return...
```


# INSTALLATION
## >> TERMUX & LINUX (ROOT NOT REQUIRED)
```python
# UPDATE REPOSITORIES
apt update && apt upgrade -y

# INSTALL DEPENDENCIES
pkg install git python -y

# CLONE REPOSITORY
git clone https://github.com/trmxvibs/ip-tracker

# ENTER DIRECTORY
cd ip-tracker

# EXECUTE CHAKRAVYUH
python3 chakravyuh.py
```

## >> WINDOWS
+ Install Python 3.x.

+ Download the Repository.


+ Launch via CMD: `python chakravyuh.py.`

## OPERATIONAL PREVIEW
```html
[+] VICTIM CAPTURED: 103.112.x.x @ 14:30:22
--- IDENTITY ---
 OS      : Android 13
 Browser : Chrome Mobile 112.0
 Loc     : Asia/Kolkata

--- HARDWARE INTEL ---
 Model   : Redmi/OnePlus/Poco (Snapdragon Detected)
 GPU     : Adreno (TM) 640
 CPU     : 8 Cores | RAM: 8 GB
 Screen  : 1080x2400
 Battery : 45% (Charging: YES)
 Net     : 4G
```
##   LEGAL DISCLAIMER 
**`READ THIS BEFORE USE:`**

This repository is for EDUCATIONAL PURPOSES and ETHICAL SECURITY RESEARCH only. The developer (Lokesh Kumar) creates tools to help security professionals and researchers understand the importance of privacy and digital footprints.

DO NOT use this tool for illegal tracking or harassment.

DO NOT use this tool on systems you do not own or have permission to test.

The author is NOT responsible for any misuse or damage caused by this program.




