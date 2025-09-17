cat > advaitzz/gui.py <<'PY'
#!/usr/bin/env python3
"""ADVAITZZ GUI - PySimpleGUI front-end for the dork generator and passive recon"""
import threading
from pathlib import Path
import PySimpleGUI as sg

# local imports (ensure these modules exist)
from .template_manager import TemplateManager
from .history import HistoryDB
from .api_keys import APIKeyStore
from .exports import export_results

BASE = Path(__file__).resolve().parent
banner = BASE / 'static' / 'banner.png'

# Basic UI theme
sg.theme('DarkBlue14')

# Initialize managers
tm = TemplateManager()
history_db = HistoryDB()
apikey_store = APIKeyStore()

# Left column: controls
layout_left = [
    [sg.Text('Target Domain')],
    [sg.Input(key='-DOMAIN-', size=(30,1))],
    [sg.Text('Categories')],
]

for cat in tm.list_categories():
    # checkbox keys must be valid identifiers, replace spaces with underscores for keys
    key = f"-CAT-{cat.replace(' ','_')}-"
    layout_left.append([sg.Checkbox(cat, key=key, default=True)])

layout_left += [[sg.Button('Generate', key='-GEN-'), sg.Button('Export', key='-EXPORT-')]]

# Right column: results
layout_right = [
    [sg.Text('Results')],
    [sg.Multiline(key='-OUT-', size=(80,20))]
]

# Templates tab layout
tmpl_layout = [
    [sg.Listbox(values=tm.list_categories(), size=(30,6), key='-T-CATS-'),
     sg.Column([[sg.Button('Add Cat', key='-T-ADD-C-')],
                [sg.Button('Remove Cat', key='-T-REMOVE-C-')]])],
    [sg.Text('Templates for selected category')],
    [sg.Listbox(values=[], size=(60,6), key='-T-LIST-')],
    [sg.Input(key='-T-NEW-'), sg.Button('Add Template', key='-T-ADD')],
    [sg.Button('Remove Selected Template', key='-T-REMOVE')]
]

# History tab
history_layout = [
    [sg.Button('Refresh History', key='-H-REF-')],
    [sg.Listbox(values=[], size=(100,10), key='-H-LIST-')]
]

# Settings tab
keys = apikey_store.load()
settings_layout = [
    [sg.Text('API Keys (encrypted)')],
    [sg.Multiline(key='-KEYS-', size=(80,10), default_text=str(keys))],
    [sg.Button('Save Keys', key='-SAVE-')]
]

# Build TabGroup
tabs = [
    sg.Tab('Dork Generator', [[sg.Column(layout_left), sg.VerticalSeparator(), sg.Column(layout_right)]]),
    sg.Tab('Templates', tmpl_layout),
    sg.Tab('History', history_layout),
    sg.Tab('Settings', settings_layout)
]

layout = [
    [sg.Image(str(banner)) if banner.exists() else sg.Text('ADVAITZZ', font=('Any', 20))],
    [sg.TabGroup([tabs], key='-TABGROUP-', expand_x=True, expand_y=True)],
    [sg.StatusBar('', key='-STATUS-', size=(100,1))]
]

window = sg.Window('ADVAITZZ', layout, resizable=True, finalize=True)

# Helper functions
def refresh_template_list(values):
    sel = values.get('-T-CATS-')
    if sel:
        cat = sel[0]
        window['-T-LIST-'].update(tm.get_templates(cat))

# Event loop
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == '-GEN-':
        domain = values['-DOMAIN-'].strip()
        if not domain:
            window['-STATUS-'].update('Enter a domain first')
            continue
        # collect checked categories
        cats = []
        for cat in tm.list_categories():
            key = f"-CAT-{cat.replace(' ','_')}-"
            if values.get(key):
                cats.append(cat)
        results = []
        for c in cats:
            for tpl in tm.get_templates(c):
                results.append({'domain': domain, 'category': c, 'dork': tpl.format(d=domain)})
        window['-OUT-'].update('\n'.join(r['dork'] for r in results))
        window['-STATUS-'].update(f'Generated {len(results)} dorks')
        history_db.record_run([domain], cats, '', len(results))

    if event == '-EXPORT-':
        text = values['-OUT-'].strip()
        if not text:
            window['-STATUS-'].update('Nothing to export')
            continue
        fn = sg.popup_get_file('Save dorks as', save_as=True, no_window=True, default_extension='txt', file_types=(('Text','*.txt'),('CSV','*.csv'),('JSON','*.json'),('Excel','*.xlsx')))
        if fn:
            # Build simple results list for exporters
            results = [{'domain': '', 'category': '', 'dork': l} for l in text.splitlines() if l.strip()]
            fmt = fn.split('.')[-1]
            try:
                export_results(results, fn, fmt)
                window['-STATUS-'].update(f'Saved {len(results)} dorks to {fn}')
            except Exception as e:
                window['-STATUS-'].update(f'Error saving: {e}')

    if event == '-T-ADD-C-':
        name = sg.popup_get_text('New category name')
        if name:
            tm.add_category(name)
            window['-T-CATS-'].update(tm.list_categories())
            # also add checkbox dynamically in generator tab is non-trivial in-place; user can restart GUI to see new checkbox

    if event == '-T-REMOVE-C-':
        sel = values.get('-T-CATS-')
        if sel:
            tm.remove_category(sel[0])
            window['-T-CATS-'].update(tm.list_categories())
            window['-T-LIST-'].update([])

    if event == '-T-CATS-':
        refresh_template_list(values)

    if event == '-T-ADD':
        sel = values.get('-T-CATS-')
        if not sel:
            sg.popup('Select a category first')
            continue
        cat = sel[0]
        tpl = values.get('-T-NEW-').strip()
        if tpl:
            tm.add_template(cat, tpl)
            refresh_template_list(values)
            window['-T-NEW-'].update('')

    if event == '-T-REMOVE':
        sel_cat = values.get('-T-CATS-')
        sel_tpl = values.get('-T-LIST-')
        if sel_cat and sel_tpl:
            cat = sel_cat[0]
            tpl = sel_tpl[0]
            lst = tm.get_templates(cat)
            if tpl in lst:
                idx = lst.index(tpl)
                tm.remove_template(cat, idx)
                refresh_template_list(values)

    if event == '-H-REF-':
        runs = history_db.list_runs()
        window['-H-LIST-'].update([f"{r[0]} | {r[1]} | {r[2]} | {r[4]} | {r[5]}" for r in runs])

    if event == '-SAVE-':
        txt = values.get('-KEYS-')
        try:
            # Expecting a Python dict literal in textbox; save it as a dict
            data = eval(txt) if txt.strip() else {}
            apikey_store.save(data)
            sg.popup('Saved API keys (encrypted)')
        except Exception as e:
            sg.popup('Error saving keys', str(e))

window.close()
PY
