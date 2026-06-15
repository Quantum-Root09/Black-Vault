# BlackVault v1.0

Terminal-based Intelligence & Network Utility Toolkit

Created by **Quantumroot09**

---

# Overview

BlackVault is a Python-based terminal toolkit that combines multiple reconnaissance, lookup, and network utilities into a single interface.

The toolkit currently includes:

* QR Link Tracker
* IP Geolocation Lookup
* Username Intelligence Search
* DNS Lookup
* Host Ping Utility

---

# Features

## 1. QR Link Tracker

Generate a QR code that redirects visitors to any URL while logging scan information in real time.

### Capabilities

* Generate QR codes instantly
* Local Network mode
* Public Internet mode using Ngrok
* Real-time scan monitoring
* Detect visitor IP address
* Detect platform/device
* Detect browser language
* Retrieve timezone information
* Automatic redirect after scan

### Logged Information

* IP Address
* Device Platform
* Timezone
* Browser Language
* User Agent
* Scan Timestamp

---

## 2. Geolocation Module

Perform deep IP intelligence lookups using public IP databases.


### Data Source

* ip-api.com

No API key required.

---

## 3. Username Intelligence Search

Search usernames across dozens of platforms and generate realistic username variations.

### Basic Search

Checks username presence across platforms including:

* GitHub
* Instagram
* Facebook
* Reddit
* Telegram
* TikTok
* YouTube
and more ..

### Advanced Search

Uses:

* GitHub Public API
* Wikipedia Search API
* Username pattern analysis
* Name extraction
* Social media naming conventions

### Smart Username Generation

Automatically creates:

* Prefix variations
* Suffix variations
* Birth-year combinations
* First/Last name combinations
* Regional surname combinations
* Instagram-style usernames

---

## 4. DNS Lookup

Retrieve DNS information about domains.

### Supported Records

* A Records
* AAAA Records
* MX Records
* NS Records
* TXT Records
* CNAME Records

Useful for domain intelligence and troubleshooting.

---

## 5. Host Ping Utility

Send ICMP Echo Requests to hosts.

### Features

* Hostname resolution
* IP resolution
* ICMP packet generation
* Round-trip timing
* Packet loss statistics
* Ping summary report

### Output

* Resolved IP Address
* Response Time
* Packets Sent
* Packets Received
* Packet Loss Percentage

Note:

Raw sockets require elevated privileges.

Linux/macOS:

```bash
sudo python blackvault.py
```

Windows:

Run Command Prompt or PowerShell as Administrator.

---

# Requirements

Python 3.10+

## Required Packages

```bash
pip install requests
pip install flask
pip install rich
pip install qrcode
pip install dnspython
```

Or:

```bash
pip install -r requirements.txt
```

---

# Installation

## Linux

```bash
git clone https://github.com/yourusername/blackvault.git

cd blackvault

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python blackvault.py
```

## Windows

```powershell
git clone https://github.com/yourusername/blackvault.git

cd blackvault

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python blackvault.py
```

---

# Main Menu

```text
[1] QR / Localhost Beacon
[2] Geolocation
[3] Username Search
[4] DNS Lookup
[5] Ping User

[0] Quit
```

---

# Project Structure

```text
blackvault/
│
├── blackvault.py
│
├── modules/
│   ├── qr_tracker.py
│   ├── geo_lookup.py
│   ├── username_search.py
│   ├── dns_lookup.py
│   └── ping_user.py
│
├── requirements.txt
├── README.md
│
├── setup.sh
└── setup.bat
```

---

# Disclaimer

This project is intended for:

* Education
* Research
* Learning
* Authorized Security Testing

Users are responsible for complying with local laws and regulations.

The author assumes no responsibility for misuse of this software.

---

╔══════════════════════════════════════════════╗
║              SUPPORT BLACKVAULT             ║
╚══════════════════════════════════════════════╝

If BlackVault proved useful during your journey,
consider leaving a ⭐ on the repository.

Every star helps keep the project alive,
improves visibility, and fuels future updates.

⭐ Star the Repo
🚀 Share the Project
🖤 Stay in the Shadows

Thank you for your support.

---

BlackVault v1.0

"Stay in the Shadows."
