#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║               📡  QR Link Tracker  📡                    ║
║     Track who scans your QR code — in real time.         ║
╚══════════════════════════════════════════════════════════╝

  Usage:  python qr_tracker.py
  Pick (1) Local Network  or  (2) Ngrok Tunnel.
  Share the QR — visitor info prints as each scan arrives.
"""

import os
import sys
import socket
import threading
import datetime
import json
import time
import logging
import importlib
import urllib.request

# ── Silence Flask/Werkzeug startup noise ──────────────────────────────────────
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.getLogger("pyngrok").setLevel(logging.ERROR)
os.environ.setdefault("WERKZEUG_RUN_MAIN", "true")

# ── Auto-install missing packages ─────────────────────────────────────────────

REQUIRED_PACKAGES = {
    "flask":  "flask",
    "rich":   "rich",
    "qrcode": "qrcode",
}

def ensure_packages() -> None:
    missing = [
        pkg for pkg, mod in REQUIRED_PACKAGES.items()
        if not importlib.util.find_spec(mod)
    ]
    if missing:
        print(f"\n  📦  Installing: {', '.join(missing)} …\n")
        os.system(
            f'"{sys.executable}" -m pip install {" ".join(missing)} --quiet'
        )

ensure_packages()

# ── Imports ───────────────────────────────────────────────────────────────────

from flask import Flask, request, redirect          # noqa: E402
from werkzeug.serving import make_server           # noqa: E402
from rich.console import Console                   # noqa: E402
from rich.prompt import Prompt                     # noqa: E402
from rich.align import Align                       # noqa: E402
import qrcode                                      # noqa: E402

console = Console()
app     = Flask(__name__)

# ── Globals ───────────────────────────────────────────────────────────────────

REDIRECT_URL: str  = "https://example.com"
PORT:         int  = 5000
scan_count:   int  = 0
BORDER             = "═" * 56
_http_server       = None           # holds the werkzeug WSGIServer instance

# ── Utility functions ─────────────────────────────────────────────────────────

def get_local_ip() -> str:
    """Return this machine's outbound LAN IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def detect_platform(ua: str) -> str:
    """Guess device platform from the User-Agent string."""
    u = ua.lower()
    for kw, label in [
        ("iphone",    "iPhone"),
        ("ipad",      "iPad"),
        ("android",   "Android"),
        ("windows",   "Windows"),
        ("macintosh", "macOS"),
        ("linux",     "Linux"),
    ]:
        if kw in u:
            return label
    return "Unknown"


def fetch_ip_info(ip: str) -> dict:
    """
    Fetch timezone / location for an IP via ip-api.com (free, no key needed).
    Returns an empty dict on any error.
    """
    if ip in ("127.0.0.1", "::1"):
        return {"timezone": "localhost"}
    try:
        endpoint = f"http://ip-api.com/json/{ip}?fields=timezone,country,city,status"
        with urllib.request.urlopen(endpoint, timeout=4) as resp:
            data = json.loads(resp.read())
            if data.get("status") == "success":
                return data
    except Exception:
        pass
    return {}


def print_qr(url: str) -> None:
    """Render the QR code as ASCII block art in the terminal."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    console.print()
    qr.print_ascii(invert=True)
    console.print()


def print_scan_log(n: int, ip: str, platform: str, timezone: str,
                   lang: str, ua: str, redir: str) -> None:
    """Print a formatted scan entry that matches the requested style."""
    ts       = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ua_short = (ua[:55] + "…") if len(ua) > 55 else ua

    console.print(f"\n[bold cyan]{BORDER}[/bold cyan]")
    console.print(f"  [bold yellow]🔔  Scan #{n}[/bold yellow]   ·   [dim]{ts}[/dim]")
    console.print(f"[bold cyan]{BORDER}[/bold cyan]")
    console.print(f"  [bold white]IP       :[/bold white] {ip}")
    console.print(f"  [bold white]Platform :[/bold white] {platform}")
    console.print(f"  [bold white]Timezone :[/bold white] {timezone}")
    console.print(f"  [bold white]Language :[/bold white] {lang}")
    console.print(f"  [bold white]UA       :[/bold white] [dim]{ua_short}[/dim]")
    console.print(f"  [bold green]→ Redirected to[/bold green] [underline]{redir}[/underline]")
    console.print(f"[bold cyan]{BORDER}[/bold cyan]")

# ── Flask route ───────────────────────────────────────────────────────────────

@app.route("/")
def track():
    global scan_count
    scan_count += 1

    # --- Collect request metadata ---
    forwarded = request.headers.get("X-Forwarded-For", "")
    ip        = forwarded.split(",")[0].strip() if forwarded else request.remote_addr
    ua        = request.headers.get("User-Agent", "Unknown")
    lang_raw  = request.headers.get("Accept-Language", "Unknown")
    lang      = lang_raw.split(",")[0].split(";")[0].strip()

    platform  = detect_platform(ua)
    info      = fetch_ip_info(ip)
    timezone  = info.get("timezone", "Unknown")

    # Log in a background thread so the redirect is immediate
    threading.Thread(
        target=print_scan_log,
        args=(scan_count, ip, platform, timezone, lang, ua, REDIRECT_URL),
        daemon=True,
    ).start()

    return redirect(REDIRECT_URL, code=302)

# ── Terminal UI ───────────────────────────────────────────────────────────────

def show_banner() -> None:
    console.clear()
    console.print()
    console.print(Align.center(
        "[bold cyan]"
        "╔══════════════════════════════════════════════════════╗\n"
        "║       📡  [bold white]QR LINK TRACKER[/bold white]  📡                     ║\n"
        "║  [dim]Track who scans your QR code — in real time.[/dim]    ║\n"
        "╚══════════════════════════════════════════════════════╝"
        "[/bold cyan]"
    ))
    console.print()


def show_menu() -> None:
    console.print("[bold]  Select tunnel mode:\n[/bold]")
    console.print(
        "  [bold cyan](1)[/bold cyan]  [bold]Local Network[/bold]  "
        "[dim]─ Works on the same Wi-Fi / LAN[/dim]"
    )
    console.print(
        "  [bold cyan](2)[/bold cyan]  [bold]Ngrok Tunnel[/bold]   "
        "[dim]─ Public internet URL via ngrok[/dim]"
    )
    console.print()


def show_live_header(url: str, mode: str) -> None:
    console.print()
    console.rule("[bold cyan]Scan QR Code[/bold cyan]")
    print_qr(url)
    console.rule()
    console.print(
        f"\n  [bold]Mode :[/bold] {mode}\n"
        f"  [bold]URL  :[/bold] [underline cyan]{url}[/underline cyan]\n"
    )
    console.print(
        "  [dim]Waiting for scans … "
        "Press [bold white]Ctrl+C[/bold white] to quit.[/dim]\n"
    )

# ── Tunnel runners ────────────────────────────────────────────────────────────

def _start_flask() -> None:
    """
    Serve the Flask app using werkzeug's make_server().

    WHY NOT app.run()?
      app.run() → werkzeug run_simple() → tries to install OS signal handlers,
      which Python only allows in the *main* thread.  Called from a daemon
      thread it raises ValueError (or silently breaks on Windows).

    make_server() creates the raw WSGIServer directly — no signal handler
    setup — so it works perfectly from any thread.
    """
    global _http_server
    _http_server = make_server("0.0.0.0", PORT, app)
    _http_server.serve_forever()


def _stop_flask() -> None:
    """Gracefully shut down the WSGIServer from the main thread."""
    global _http_server
    if _http_server:
        _http_server.shutdown()
        _http_server = None


def run_local() -> None:
    """Mode 1 — serve on the local network."""
    local_ip = get_local_ip()
    url      = f"http://{local_ip}:{PORT}"

    console.print(f"\n  [bold green]✓  Starting local server …[/bold green]")
    threading.Thread(target=_start_flask, daemon=True).start()
    time.sleep(0.7)

    show_live_header(url, "Local Network")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _stop_flask()
        console.print("\n\n  [bold red]✗  Server stopped.[/bold red]\n")


def run_ngrok() -> None:
    """Mode 2 — expose via an ngrok public tunnel."""

    try:
        from pyngrok import ngrok as _ngrok
    except ImportError:
        console.print("\n[yellow]📦 Installing pyngrok ...[/yellow]")
        os.system(f'"{sys.executable}" -m pip install pyngrok --quiet')
        from pyngrok import ngrok as _ngrok

    # Ask user for token
    token = Prompt.ask(
        "\n[bold yellow]🔑 Enter your ngrok auth token[/bold yellow]"
    ).strip()

    if not token:
        console.print("\n[bold red]✗ No token entered.[/bold red]")
        return

    try:
        _ngrok.set_auth_token(token)
    except Exception as exc:
        console.print(f"\n[bold red]✗ Invalid token:[/bold red] {exc}")
        return

    # Start Flask
    threading.Thread(target=_start_flask, daemon=True).start()
    time.sleep(1)

    console.print("\n[bold green]✓ Connecting to ngrok ...[/bold green]")

    try:
        tunnel = _ngrok.connect(PORT)
        url = tunnel.public_url
    except Exception as exc:
        console.print(f"\n[bold red]✗ Ngrok error:[/bold red] {exc}")
        try:
            _ngrok.kill()
        except Exception:
            pass
        return

    show_live_header(url, "Ngrok Public Tunnel")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _stop_flask()
        try:
            _ngrok.kill()
        except Exception:
            pass
        console.print("\n\n[bold red]✗ Server stopped.[/bold red]\n")

# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    global REDIRECT_URL

    show_banner()

    REDIRECT_URL = Prompt.ask(
        "  [bold yellow]↩  Redirect visitors to URL[/bold yellow]",
        default="https://example.com",
    )
    console.print()

    show_menu()
    choice = Prompt.ask("  [bold]Option[/bold]", choices=["1", "2"])

    if choice == "1":
        run_local()
    else:
        run_ngrok()


if __name__ == "__main__":
    main()
