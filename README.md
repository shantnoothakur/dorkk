# ADVAITZZ — Advanced Dork & Recon Toolkit

**Codename:** ADVAITZZ  
**Author:** Shantnoo thakur / ADVAITZZ
**Repo:** https://github.com/shantnoothakur/dorkk

**Short:** ADVAITZZ is an interactive Google Dork generator and passive recon helper for legal bug-bounty researchers, OSINT investigators, and defenders. It helps create targeted search queries (dorks), collect passive intelligence, and export results for further analysis.

> ⚠️ **Legal disclaimer:** Use this tool **only** on targets you have explicit permission to test (bug bounty programs, your own assets, or public OSINT research). ADVAITZZ is intended for passive information gathering and automation — it does **not** perform active exploitation. The author is not responsible for misuse.

---

## Table of Contents
- Features
- Quick Install (Kali / Debian / Windows)
- Usage (CLI & GUI)
- Commands & Options (reference)
- Examples
- Extra Tools & Utilities
- Development & Contributing
- Security & Responsible Disclosure
- Changelog & Roadmap
- License

---

## Features (what it does)
ADVAITZZ focuses on safe, repeatable recon and dork generation. Major features:

- Interactive CLI and non-interactive (flags) modes.
- PySimpleGUI desktop front-end (cross-platform).
- Multiple dork categories: Login Pages, Sensitive Files, Documents, Index-Of, Subdomains, Cloud buckets, Secrets patterns, Custom templates.
- Multi-domain input (single domain, file with domains).
- Export to TXT and CSV.
- `--all` to generate every category.
- `--quiet` for piping and scripting.
- Passive recon helpers: WHOIS, DNS A records, crt.sh certificate enumeration (passive), subdomain list aggregation (passive).
- Proxy support (for search engines where allowed) and random user-agent support to avoid trivial blocking.
- Banner generation utility (SVG → PNG) for README and documentation.
- Encoding/Decoding utilities: Base64, MD5 (local transforms).
- Safe-by-default: no active scanning modules installed by default. Any active features require opt-in and explicit warnings.
- Extensible templates and a GUI to manage templates, history, settings, API keys (optional).
- Exportable project history (SQLite) for audit/repeatability.

---

## Quick Install

### 1) Clone the repo
```bash
git clone https://github.com/yourusername/advaitzz.git
cd advaitzz
2) Create & activate a virtualenv (recommended)
Linux / macOS:

bash
Copy code
python3 -m venv venv
. venv/bin/activate
Windows (PowerShell):

powershell
Copy code
python -m venv venv
.\venv\Scripts\Activate.ps1
3) Install dependencies
CLI only:

bash
Copy code
pip install -r requirements.txt
GUI (optional):

bash
Copy code
pip install -r requirements_gui.txt
4) Install ADVAITZZ (editable mode for development)
bash
Copy code
pip install -e .
If you prefer a global command on Kali:

bash
Copy code
sudo pip install .
# or create a symlink:
chmod +x advaitzz/cli.py
sudo ln -s "$(pwd)/advaitzz/cli.py" /usr/local/bin/advaitzz
Run / Usage
CLI (interactive)
bash
Copy code
advaitzz
Prompts for domain and options interactively.

CLI (non-interactive)
bash
Copy code
advaitzz example.com --categories login,docs --output example_dorks.txt
CLI options (compact)
bash
Copy code
advaitzz <domain> [--input file] [--categories login,docs] [--all] [--output file] [--format txt|csv] [--quiet]
GUI (PySimpleGUI)
bash
Copy code
python advaitzz/gui.py
# or
python -m advaitzz.gui
The GUI includes tabs for:

Dork Generator (select categories, generate, export)

Passive Recon (WHOIS, DNS, crt.sh)

Templates (add/edit dork templates)

Settings (proxy, user-agent pool, API keys)

History (saved runs, exports)

Commands & Options — Full Reference
lua
Copy code
Usage:
  advaitzz [domain] [options]

Options:
  domain                  Single target domain (e.g., example.com)
  --input, -i <file>      File with domains (one per line)
  --categories, -c <cats> Comma separated categories (login,sensitive,docs,index,subdomains,cloud,secrets)
  --all                   Generate all categories
  --output, -o <file>     Save dorks to file (txt or csv if --format=csv)
  --format <txt|csv>      Output format (default: txt)
  --quiet                 Quiet mode (print dorks only — good for piping)
  --help, -h              Show help
  --version               Show version
  --repair                Repair or reinstall tool (helper)
  --update                Check for updates (git pull) — optional
  --gui                   Launch GUI (same as `python -m advaitzz.gui`)
Examples
Interactive:

bash
Copy code
advaitzz
# follow prompts: enter example.com, choose categories, export
Non-interactive:

bash
Copy code
advaitzz example.com --categories login,docs
Save results to txt:

bash
Copy code
advaitzz example.com --categories login,docs --output mydorks.txt
Save results to csv:

bash
Copy code
advaitzz example.com --all --output all_dorks.csv --format csv
Batch from file:

bash
Copy code
advaitzz --input domains.txt --categories docs,subdomains --output results.csv --format csv
Quiet mode (pipe into another tool):

bash
Copy code
advaitzz example.com --categories login --quiet | tee login_dorks.txt
Generate README banner (SVG → PNG):

bash
Copy code
python make_banner.py
# produces advaitzz/banner.png
Install from GitHub:

bash
Copy code
pip install git+https://github.com/yourusername/advaitzz.git
# or for a release tag:
pip install git+https://github.com/yourusername/advaitzz.git@v0.1.0
Uninstall:

bash
Copy code
pip uninstall -y advaitzz
Extra Tools & Utilities
make_banner.py — generate README banner PNG from advaitzz/logo.svg.

advaitzz/gui.py — GUI front-end (optional).

advaitzz/cli.py — main CLI entrypoint.

requirements.txt / requirements_gui.txt — dependency lists.

Safe-by-default policy & what I will not add
To keep ADVAITZZ ethical and legally safe:

No built-in active exploitation (RCE, exploit chains), interactive web shells, or automated attack modules will be added by default.

Active network scanning (nmap-style port scanning) is not enabled by default; any active features must be explicitly opt-in, with clear warnings and an "I have permission" checkbox in the GUI.

I will not provide exploit payloads or instructions to break into systems.

If you want to add active modules, we will:

Require explicit user confirmation.

Add scope/targets verification and a local log of consent (for audit).

Make modules optional and clearly labeled with risk.

Development & Contributing
Contributions are welcome — please follow these guidelines:

Fork the repository.

Create a feature branch: git checkout -b feat/some-feature

Add tests where appropriate and update requirements*.txt.

Run linter and tests: flake8 . / pytest -q

Submit a PR with a clear description of the feature and the rationale.

Files to pay attention to:

advaitzz/cli.py — main CLI logic

advaitzz/gui.py — GUI front-end

advaitzz/templates/ — add new dork templates here

make_banner.py — banner generation

Security & Responsible Disclosure
If you discover a vulnerability in ADVAITZZ:

Do not publish exploit code.

Open a private issue or email: security@yourdomain.tld (add address).

Provide steps to reproduce, logs, and impact. We will respond within 7 days.

Changelog & Roadmap
v0.1.0 — Initial release

Interactive CLI

Dork templates

Export to TXT/CSV

GUI prototype (PySimpleGUI)

Banner generator

Planned

Template marketplace / template import/export

SQLite history and session export

Optional Shodan/Bing integration behind API keys

Optional active modules (opt-in, explicit confirmation & consent)

Installer scripts for Kali packaging

License
This project is released under the MIT License. See LICENSE for details.

Acknowledgments & credits
Inspired by OSINT and dorking tools in the community.

UI inspiration: PySimpleGUI for quick cross-platform front ends.

Please respect other people's systems and privacy.
