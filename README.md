# =========================
# ADVAITZZ — Quick start
# =========================

ADVAITZZ is an interactive Google Dork generator and recon helper aimed for **legal** bug-bounty researchers and OSINT investigators.


**Features**
- Interactive CLI and non-interactive (CLI flags) modes.
- Multiple categories (login pages, sensitive files, docs, index-of, subdomains, cloud, secrets patterns).
- Export results to TXT/CSV.
- Single/multi-domain input (file or args).
- Quick `--all` mode to generate every category.
- `--quiet` for scripting, `--output` to save, `--format` (txt/csv).


**Disclaimer**: Use only on targets that allow reconnaissance. Do not use ADVAITZZ for unauthorized access or abuse.


# 1) Clone the repo (or copy files into a folder)
git clone https://github.com/shantnoothakur/dorkk
cd dorkk

# 2) Create & activate a Python virtual environment (recommended)
python3 -m venv venv
. venv/bin/activate        # Bash / Zsh (Kali / Linux)
# On Fish shell: source venv/bin/activate.fish
# On Windows (PowerShell): .\venv\Scripts\Activate.ps1

# 3) Install CLI-only dependencies (fast)
pip install -r requirements.txt

# 4) Install GUI dependencies (if you plan to run the GUI)
# (optional) only if you want GUI mode
pip install -r requirements_gui.txt

# 5) Install ADVAITZZ in editable/developer mode so changes are immediate
pip install -e .

# 6) Show help for the CLI
advaitzz --help
# or (if entrypoint isn't available)
python -m advaitzz.cli --help

# =========================
# Basic usage examples
# =========================

# Interactive CLI (prompts for domain if none provided)
advaitzz

# Non-interactive: generate login dorks for example.com and print to stdout
advaitzz example.com --categories login

# Save results as a text file
advaitzz example.com --categories login,docs --output example_dorks.txt --format txt

# Save results as CSV
advaitzz example.com --categories login,docs --output example_dorks.csv --format csv

# Generate all categories for a domain
advaitzz example.com --all --output all_dorks.txt

# Quiet mode suitable for piping
advaitzz example.com --categories login --quiet

# Batch mode: supply a file with domains (one per line)
# domains.txt contents example:
# example.com
# target.example
advaitzz --input domains.txt --categories login,docs --output batch_dorks.txt

# =========================
# Running the GUI (optional)
# =========================

# Ensure GUI requirements installed (see earlier)
# Then run:
python advaitzz/gui.py

# If you installed with `pip install -e .` you can still run the module directly:
python -m advaitzz.gui

# =========================
# Packaging / install from GitHub
# =========================

# Install from your GitHub repo (users can install directly)
pip install git+https://github.com/yourusername/advaitzz.git

# Install a specific release tag
pip install git+https://github.com/yourusername/advaitzz.git@v0.1.0

# Build source distribution and wheel
python setup.py sdist bdist_wheel
# Output will be in dist/  (upload to PyPI if you want)

# =========================
# Make it convenient on Kali (system command)
# =========================

# Option A — install system-wide (not generally recommended):
sudo pip install .

# Option B — symlink the CLI script to a directory in PATH
# (ensure advaitzz/cli.py has #!/usr/bin/env python3 and is executable)
chmod +x advaitzz/cli.py
sudo ln -s "$(pwd)/advaitzz/cli.py" /usr/local/bin/advaitzz

# Now you can call `advaitzz` from any shell

# =========================
# Dev & CI (lint / test)
# =========================

# install dev-tools
pip install flake8 pytest

# run linter
flake8 .

# run tests (if you add them)
pytest -q

# create & push a release tag
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0

# =========================
# Banner generation (optional)
# =========================

# If you want to auto-generate a banner PNG from the repository SVG:
# 1. Make sure you installed these Python libs:
pip install pillow cairosvg

# 2. Run the provided script (make_banner.py) — it will create advaitzz/banner.png
python make_banner.py

# =========================
# Uninstall
# =========================
pip uninstall -y advaitzz

# =========================
# Important: legal & safety
# =========================
# Use ADVAITZZ only for passive recon, OSINT, and for targets/programs you are explicitly authorized to test.
# Do NOT use these dorks to access or attack systems you do not own or have permission to test.
