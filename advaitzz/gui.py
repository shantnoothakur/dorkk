#!/usr/bin/env python3
"""ADVAITZZ GUI - PySimpleGUI front-end for the dork generator and passive recon
"""
import os
import io
import sys
import csv
import json
import socket
import threading
from pathlib import Path
import PySimpleGUI as sg
import requests
import pandas as pd
import whois
import dns.resolver


# basic config
BASE_DIR = Path(__file__).resolve().parent
LOGO = BASE_DIR / "static" / "banner.png" # put banner.png here


# templates similar to CLI TEMPLATES
TEMPLATES = {
'Login Pages': [
'site:{d} inurl:login',
'site:{d} intitle:login',
'site:{d} inurl:signin'
],
'Documents': [
'site:{d} ext:pdf',
'site:{d} ext:docx',
'site:{d} ext:xlsx'
],
'Index Of': [
"s
