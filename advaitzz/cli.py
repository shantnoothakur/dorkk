#!/usr/bin/env python3
import sys
import time
from advaitzz.template_manager import TemplateManager
from advaitzz.history import HistoryDB
from advaitzz.exports import export_results

# Animated ASCII banner
BANNER = r"""
    ___    ____  __      __    ___   ___ ___  ____
   /   |  / __ \/ /     / /   /   | /   |__ \/ __ \
  / /| | / / / / /     / /   / /| |/ /| |_/ / / / /
 / ___ |/ /_/ / /___  / /___/ ___ / ___ |/ /_/ / 
/_/  |_/_____ /_____/ /_____/_/  |_/_/  |_/_____/  
"""

def animate_banner(text, delay=0.005):
    """Prints the banner with a typewriter effect"""
    for line in text.splitlines():
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(0.03)
    print("\n")

def main():
    animate_banner(BANNER)

    tm = TemplateManager()
    history = HistoryDB()

    print("Categories available:")
    for c in tm.list_categories():
        print(" -", c)

    domain = input("\nEnter target domain: ").strip()
    if not domain:
        print("No domain entered, exiting.")
        return

    results = []
    print("\nGenerating dorks...\n")
    for cat in tm.list_categories():
        for tpl in tm.get_templates(cat):
            dork = tpl.format(d=domain)
            results.append({'domain': domain, 'category': cat, 'dork': dork})
            print(f"[{cat}] {dork}")

    history.record_run([domain], tm.list_categories(), '', len(results))

    choice = input("\nSave results? (y/n) ")
    if choice.lower() == 'y':
        fname = input("Filename (with extension txt/csv/json/xlsx): ").strip()
        fmt = fname.split('.')[-1]
        export_results(results, fname, fmt)
        print(f"Saved {len(results)} dorks to {fname}")

if __name__ == "__main__":
    main()
