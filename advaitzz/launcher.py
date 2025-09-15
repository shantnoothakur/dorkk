#!/usr/bin/env python3
"""
ADVAITZZ Launcher - ASCII banner + interactive menu
Drop-in launcher that shows stylized ASCII art header and main menu.
"""

import sys
import time
from pathlib import Path

# Attempt to import pyfiglet for ASCII art; fallback to plain text
try:
    import pyfiglet
except Exception:
    pyfiglet = None

# Import core modules from the package (assumes they exist in package)
from .template_manager import TemplateManager
from .history import HistoryDB
from .exports import export_results

# Optional: GUI launcher
def launch_gui():
    try:
        # Import lazily to avoid GUI deps in pure-CLI env
        from . import gui as gui_module
        # If gui exposes a main() function or can be run as module:
        # Run it as a module to keep this launcher simple
        import runpy
        runpy.run_module('advaitzz.gui', run_name='__main__')
    except Exception as e:
        print("Failed to launch GUI:", e)

def print_header():
    name = "ADVAITZZ"
    subtitle = "Advanced Dork & Recon Toolkit"
    if pyfiglet:
        f = pyfiglet.Figlet(font='slant')
        print(f.renderText(name))
    else:
        # fallback ASCII-ish banner
        print("=" * 60)
        print(f"  {name}")
        print("=" * 60)
    print(subtitle)
    print()

def pause_msg(msg="Press ENTER to continue..."):
    try:
        input(msg)
    except KeyboardInterrupt:
        print()
        return

def generate_dorks_interactive(tm, history_db):
    domain = input("Enter target domain (example.com): ").strip()
    if not domain:
        print("No domain entered.")
        return
    cats = tm.list_categories()
    print("\nSelect categories (comma separated indices) or 'all':")
    for i, c in enumerate(cats):
        print(f" {i+1}. {c}")
    sel = input("\nYour choice (e.g. 1,3 or all): ").strip()
    if sel.lower() == 'all':
        use = cats
    else:
        try:
            idxs = [int(x.strip()) - 1 for x in sel.split(',') if x.strip()]
            use = [cats[i] for i in idxs if 0 <= i < len(cats)]
        except Exception:
            print("Invalid selection, using default (all).")
            use = cats

    results = []
    for c in use:
        for tpl in tm.get_templates(c):
            results.append({'domain': domain, 'category': c, 'dork': tpl.format(d=domain)})

    print(f"\nGenerated {len(results)} dorks:\n")
    for r in results:
        print(r['dork'])
    # Ask to export
    exp = input("\nSave results? [y/N]: ").strip().lower()
    if exp == 'y':
        fname = input("Filename (example: out.txt or out.csv or out.json or out.xlsx): ").strip()
        if fname:
            fmt = fname.split('.')[-1]
            export_results(results, fname, fmt)
            print("Saved ->", fname)
            history_db.record_run([domain], use, fname, len(results))
    else:
        history_db.record_run([domain], use, '', len(results))

def templates_menu(tm):
    while True:
        print("\nTemplates Manager")
        cats = tm.list_categories()
        for i, c in enumerate(cats):
            print(f" {i+1}. {c} ({len(tm.get_templates(c))} templates)")
        print(" A. Add Category")
        print(" R. Remove Category")
        print(" V. View Templates in Category")
        print(" B. Back to main menu")
        choice = input("Choice: ").strip().lower()
        if choice == 'a':
            name = input("New category name: ").strip()
            if name:
                tm.add_category(name)
                print("Added category:", name)
        elif choice == 'r':
            idx = input("Category index to remove: ").strip()
            try:
                i = int(idx) - 1
                if 0 <= i < len(cats):
                    tm.remove_category(cats[i])
                    print("Removed", cats[i])
            except Exception:
                print("Invalid index.")
        elif choice == 'v':
            idx = input("Category index to view templates: ").strip()
            try:
                i = int(idx) - 1
                if 0 <= i < len(cats):
                    cat = cats[i]
                    lst = tm.get_templates(cat)
                    print(f"\nTemplates for {cat}:")
                    for j, t in enumerate(lst):
                        print(f" {j+1}. {t}")
                    sub = input("Add (a) / Remove (r) / Back (Enter): ").strip().lower()
                    if sub == 'a':
                        tpl = input("Template (use {d} for domain): ").strip()
                        if tpl:
                            tm.add_template(cat, tpl)
                            print("Added.")
                    elif sub == 'r':
                        ridx = input("Template index to remove: ").strip()
                        try:
                            rj = int(ridx) - 1
                            tm.remove_template(cat, rj)
                            print("Removed.")
                        except Exception:
                            print("Invalid.")
                else:
                    print("Invalid index.")
            except Exception:
                print("Invalid input.")
        elif choice == 'b':
            break
        else:
            print("Unknown choice.")

def history_menu(history_db):
    rows = history_db.list_runs(limit=50)
    if not rows:
        print("\nNo history entries yet.")
        pause_msg()
        return
    print("\nHistory (latest first):")
    for r in rows:
        print(f"ID:{r[0]} | Domains:{r[1]} | Cats:{r[2]} | Count:{r[4]} | Time:{r[5]}")
    pause_msg()

def settings_menu():
    print("\nSettings")
    print(" - GUI launch (if available)")
    print(" - API Keys managed via advaitzz/api_keys.py (encrypted store)")
    print(" - Proxy & user-agent settings can be configured in settings file (not yet implemented)")
    pause_msg()

def consent_prompt():
    print("\nBefore using any active modules, you must confirm you have permission to test the target.")
    confirm = input("Type `I_HAVE_PERMISSION` to confirm and continue: ").strip()
    return confirm == "I_HAVE_PERMISSION"

def main_menu():
    tm = TemplateManager()
    history_db = HistoryDB()

    while True:
        print_header()
        print("Main Menu:")
        print(" 1) Generate Dorks")
        print(" 2) Templates Manager")
        print(" 3) History")
        print(" 4) Launch GUI")
        print(" 5) Settings")
        print(" 6) Consent & Active Features (disabled by default)")
        print(" 0) Exit")
        ch = input("\nChoose an option: ").strip()
        if ch == '1':
            generate_dorks_interactive(tm, history_db)
        elif ch == '2':
            templates_menu(tm)
        elif ch == '3':
            history_menu(history_db)
        elif ch == '4':
            launch_gui()
        elif ch == '5':
            settings_menu()
        elif ch == '6':
            ok = consent_prompt()
            if ok:
                print("Consent recorded. (Note: active modules are still opt-in and not executed automatically.)")
            else:
                print("Consent not provided.")
            pause_msg()
        elif ch == '0' or ch.lower() == 'q':
            print("Goodbye — stay legal.")
            time.sleep(0.3)
            break
        else:
            print("Unknown option.")
        # After action return to menu
        print("\nReturning to menu...")
        time.sleep(0.4)

if __name__ == '__main__':
    main_menu()
