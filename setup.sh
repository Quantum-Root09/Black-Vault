#!/bin/bash
set -e

echo ""
echo "  ╔════════════════════════════════════════╗"
echo "  ║     BlackVault — Setup Script          ║"
echo "  ║     by venkatsai                       ║"
echo "  ╚════════════════════════════════════════╝"
echo ""

# ── Check Python ──────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "  [!] Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

PYTHON=$(command -v python3)
PYVER=$($PYTHON --version 2>&1)
echo "  [+] Python found: $PYVER"

# ── Minimum version check ─────────────────────────────────
MIN_MINOR=8
MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")
MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt "$MIN_MINOR" ]); then
    echo "  [!] Python 3.$MIN_MINOR+ is required. Found: $PYVER"
    exit 1
fi

# ── Create virtual environment ────────────────────────────
if [ -d "venv" ]; then
    echo "  [~] Existing venv found — skipping creation."
else
    echo "  [+] Creating virtual environment..."
    $PYTHON -m venv venv
fi

# ── Activate ──────────────────────────────────────────────
# shellcheck disable=SC1091
source venv/bin/activate

# ── Install dependencies ──────────────────────────────────
echo "  [+] Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ""
echo "  ╔════════════════════════════════════════╗"
echo "  ║  [✔]  Setup complete!                  ║"
echo "  ╚════════════════════════════════════════╝"
echo ""
echo "  To launch BlackVault:"
echo ""
echo "    source venv/bin/activate"
echo "    python blackvault.py"
echo ""
