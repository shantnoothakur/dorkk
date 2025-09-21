#!/usr/bin/env python3
from advaitzz.banner_anim import print_banner
from advaitzz.template_manager import TemplateManager
from advaitzz.history import HistoryDB
from advaitzz.exports import export_results

def main():
    print_banner()
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
