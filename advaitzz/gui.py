#!/usr/bin/env python3
import PySimpleGUI as sg
from advaitzz.banner_anim import BANNER
from advaitzz.template_manager import TemplateManager
from advaitzz.history import HistoryDB
from advaitzz.api_keys import APIKeyStore
from advaitzz.exports import export_results

tm = TemplateManager()
history_db = HistoryDB()
apikey_store = APIKeyStore()

sg.theme('DarkBlue14')

layout = [
    [sg.Text(BANNER, font=('Courier', 12))],
    [sg.Text('Target Domain'), sg.Input(key='-DOMAIN-', size=(30,1))],
    [sg.Button('Generate', key='-GEN-'), sg.Button('Export', key='-EXPORT-')],
    [sg.Multiline(key='-OUT-', size=(80,20))]
]

window = sg.Window('ADVAITZZ GUI', layout, resizable=True, finalize=True)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-GEN-':
        domain = values['-DOMAIN-'].strip()
        if not domain:
            sg.popup("Enter a domain first")
            continue
        results = []
        for cat in tm.list_categories():
            for tpl in tm.get_templates(cat):
                results.append({'domain': domain, 'category': cat, 'dork': tpl.format(d=domain)})
        window['-OUT-'].update('\n'.join(r['dork'] for r in results))
        history_db.record_run([domain], tm.list_categories(), '', len(results))
    if event == '-EXPORT-':
        text = values['-OUT-'].strip()
        if not text:
            sg.popup("Nothing to export")
            continue
        fn = sg.popup_get_file('Save dorks as', save_as=True, no_window=True, default_extension='txt',
                               file_types=(('Text','*.txt'),('CSV','*.csv'),('JSON','*.json'),('Excel','*.xlsx')))
        if fn:
            results = [{'domain':'','category':'','dork':l} for l in text.splitlines() if l.strip()]
            fmt = fn.split('.')[-1]
            export_results(results, fn, fmt)
            sg.popup(f"Saved {len(results)} dorks to {fn}")

window.close()
