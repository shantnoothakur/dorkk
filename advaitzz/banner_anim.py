import time
import sys

BANNER = r"""
    ___    ____  __      __    ___   ___ ___  ____
   /   |  / __ \/ /     / /   /   | /   |__ \/ __ \
  / /| | / / / / /     / /   / /| |/ /| |_/ / / / /
 / ___ |/ /_/ / /___  / /___/ ___ / ___ |/ /_/ / 
/_/  |_/_____ /_____/ /_____/_/  |_/_/  |_/_____/  
"""

def print_banner(delay=0.02):
    for line in BANNER.splitlines():
        print(line)
        time.sleep(delay)
    print("\n")
