#!/usr/bin/env python3
"""
BlackVault — OSINT Toolkit
Author : venkatsai
"""

import sys
import os
import time
import importlib.util
from modules import geo_lookup
from modules import username_search
from modules import dns_lookup
from modules import ping_user   

# ── Bootstrap rich ─────────────────────────────────────────────────────────────
def _bootstrap():
    if not importlib.util.find_spec("rich"):
        print("\n  Installing rich…")
        os.system(f'"{sys.executable}" -m pip install rich --quiet')

_bootstrap()

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.text import Text

console = Console()

VERSION = "v1.0"
AUTHOR  = "By Quantum-Root09"

BANNER = r"""
██████╗ ██╗      █████╗  ██████╗██╗  ██╗      ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝      ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
██████╔╝██║     ███████║██║     █████╔╝       ██║   ██║███████║██║   ██║██║     ██║
██╔══██╗██║     ██╔══██║██║     ██╔═██╗       ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗       ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝        ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝

                          B L A C K   V A U L T
"""

# ── UI helpers ────────────────────────────────────────────────────────────────

def show_main_menu() -> None:
    console.clear()
    console.print(f"[bold red]{BANNER}[/bold red]")
    console.print(Align.center(
        f"[bold white]  {VERSION}   ·   {AUTHOR}[/bold white]"
    ))
    console.print()
    console.print(Panel(
        "\n"
        "  [bold cyan]\[1][/bold cyan]  [bold white]QR / Localhost Beacon[/bold white]"
        "      [dim]─ Track who scans your QR in real time[/dim]\n\n"
        "  [bold cyan]\[2][/bold cyan]  [bold white]Geolocation[/bold white]"
        "               [dim]─ Deep IP address intelligence[/dim]\n\n"
        "  [bold cyan]\[3][/bold cyan]  [bold white]Username Search[/bold white]"
        "            [dim]─ Hunt a username across platforms[/dim]\n\n"
        "  [bold cyan]\[4][/bold cyan]  [bold white]DNS Lookup[/bold white]"
        "             [dim]─ Uncover domain details[/dim]\n\n"
        "  [bold cyan]\[5][/bold cyan]  [bold white]Ping User[/bold white]"
        "              [dim]─ Send's ICMP ping requests to the user[/dim]\n\n"
        "  [bold red]\[Q][/bold red]  [bold white]Quit[/bold white]\n",
        title="[bold cyan]⬛  BLACKVAULT  ⬛[/bold cyan]",
        border_style="cyan",
        padding=(0, 4),
    ))
    console.print()


def post_tool_menu() -> bool:
    """
    Shown after each tool exits.
    Returns True  → back to main menu
    Returns False → quit BlackVault
    """
    console.print()
    console.print(Rule(style="dim cyan"))
    console.print(
        "  [bold cyan]\[0][/bold cyan]  Back to Main Menu"
        "   [bold red]\[Q][/bold red]  Quit BlackVault"
    )
    console.print(Rule(style="dim cyan"))
    console.print()
    while True:
        try:
            choice = input("  → ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return False
        if choice == "0":
            return True
        if choice in ("q", "quit"):
            return False
        console.print("  [yellow]⚠  Please enter [0] or [Q][/yellow]")


def quit_blackvault() -> None:
    console.print()
    console.print(
        "[bold red]  [✖]  Exiting Black Vault... Stay in the shadows.[/bold red]"
    )
    console.print()
    sys.exit(0)


# ── Tool launchers ────────────────────────────────────────────────────────────

def run_qr_tracker() -> None:
    try:
        from modules.qr_tracker import main as qr_main
        qr_main()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        console.print(f"\n  [bold red]✗  Error:[/bold red] {exc}")
    if not post_tool_menu():
        quit_blackvault()


def run_geolocation() -> None:
    try:
        from modules import geo_lookup
        geo_lookup.run()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        console.print(f"\n  [bold red]✗  Error:[/bold red] {exc}")
    if not post_tool_menu():
        quit_blackvault()


def run_username_search() -> None:
    try:
        from modules import username_search
        username_search.run()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        console.print(f"\n  [bold red]✗  Error:[/bold red] {exc}")
    if not post_tool_menu():
        quit_blackvault()


def run_ping_user() -> None:
    try:
        from modules import ping_user
        ping_user.run()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        console.print(f"\n  [bold red]✗  Error:[/bold red] {exc}")
    if not post_tool_menu():
        quit_blackvault()


def run_dns_lookup() -> None:
    try:
        from modules import dns_lookup
        dns_lookup.run()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        console.print(f"\n  [bold red]✗  Error:[/bold red] {exc}")
    if not post_tool_menu():
        quit_blackvault()




# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    while True:
        try:
            show_main_menu()
            choice = input("  Select option: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            quit_blackvault()

        if choice == "1":
            run_qr_tracker()
        elif choice == "2":
            run_geolocation()
        elif choice == "3":
            run_username_search()
        elif choice == "4":
            run_dns_lookup()
        elif choice == "5":
            run_ping_user()
        elif choice in ("q", "quit"):
            quit_blackvault()
        else:
            console.print(
                "\n  [yellow]⚠  Invalid option. Choose 1, 2, 3, 4, 5 or Q.[/yellow]"
            )
            time.sleep(1.2)


if __name__ == "__main__":
    main()
