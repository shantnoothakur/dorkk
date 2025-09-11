#!/usr/bin/env python3
# Tool Name: ADVAITZZ Dork Maker (Interactive)
# Author: ADVAITZZ
# Purpose: Generate Google Dorks for Recon & Bug Bounty (Legal Use Only)

import sys

def generate_dorks(domain):
    return {
        "1": ("Login Pages", [
            f"site:{domain} inurl:login",
            f"site:{domain} intitle:'login'",
            f"site:{domain} inurl:auth",
            f"site:{domain} inurl:signin"
        ]),
        "2": ("Sensitive Files", [
            f"site:{domain} ext:sql | ext:xml | ext:conf | ext:log",
            f"site:{domain} ext:env | ext:ini | ext:bak",
            f"site:{domain} intitle:'index of' 'config'"
        ]),
        "3": ("Documents (PDF/DOCX)", [
            f"site:{domain} ext:pdf",
            f"site:{domain} ext:docx",
            f"site:{domain} ext:xlsx",
        ]),
        "4": ("Exposed Directories", [
            f"site:{domain} intitle:'index of' 'backup'",
            f"site:{domain} intitle:'index of' 'admin'",
            f"site:{domain} intitle:'index of' 'uploads'"
        ]),
        "5": ("Subdomains", [
            f"site:*.{domain} -www.{domain}"
        ]),
        "0": ("Exit", [])
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python advaitzz.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    dorks = generate_dorks(domain)

    print("\n=== ADVAITZZ Dork Maker (Interactive) ===")
    print(f"Target Domain: {domain}\n")

    while True:
        print("Choose a category:")
        for key, (name, _) in dorks.items():
            print(f" {key}. {name}")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "0":
            print("\nGoodbye! Stay legal. ✌️")
            break
        elif choice in dorks:
            name, queries = dorks[choice]
            print(f"\n[{name}]")
            for q in queries:
                print("  " + q)
            print()
        else:
            print("Invalid choice, try again.\n")

if __name__ == "__main__":
    main()
