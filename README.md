# ADVAITZZ


ADVAITZZ is an interactive Google Dork generator and recon helper aimed for **legal** bug-bounty researchers and OSINT investigators.


**Features**
- Interactive CLI and non-interactive (CLI flags) modes.
- Multiple categories (login pages, sensitive files, docs, index-of, subdomains, cloud, secrets patterns).
- Export results to TXT/CSV.
- Single/multi-domain input (file or args).
- Quick `--all` mode to generate every category.
- `--quiet` for scripting, `--output` to save, `--format` (txt/csv).


**Disclaimer**: Use only on targets that allow reconnaissance. Do not use ADVAITZZ for unauthorized access or abuse.


## Installation (Kali Linux / Debian-based)


```bash
# Clone repository (if you've copied files into a local folder)
cd /path/to/advaitzz
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
# Optional: install as a system command
sudo pip install .
# Now you can run:
advaitzz --help
