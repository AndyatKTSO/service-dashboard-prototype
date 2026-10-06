"""Excel in Dashboard-JSON umwandeln. Bei Fehler bleibt die letzte JSON erhalten."""
import argparse, json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
import openpyxl

FIELDS = ['Titel (SO-Standard)', 'Departement', 'Amt', 'Service-Owner (Dienststelle)', 'Service-Owner (Name Vorname)', 'Service-Owner (E-Mail)', 'Link zu Service', 'Service-Zustand', 'Pendenzen', 'Bemerkungen']
KEYS = ['title','department','office','ownerUnit','owner','email','link','status','tasks','notes']

def convert(source, target):
    wb = openpyxl.load_workbook(source, data_only=True, read_only=True)
    try:
        rows = iter(wb.active.values)
        headers = [str(v).strip() if v is not None else '' for v in next(rows)]
        missing = [h for h in FIELDS if h not in headers]
        if missing: raise ValueError('Fehlende Spalten: ' + ', '.join(missing))
        indices = [headers.index(h) for h in FIELDS]
        services = []
        for row in rows:
            if not any(v is not None for v in row): continue
            item = {k: str(row[i]).strip() if i < len(row) and row[i] is not None else '' for k,i in zip(KEYS,indices)}
            if not item['title']: raise ValueError('Service ohne Titel gefunden')
            services.append(item)
        payload = {'generatedAt':datetime.now(timezone.utc).isoformat(), 'services': services}
        target = Path(target); target.parent.mkdir(parents=True, exist_ok=True)
        name = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent, delete=False) as f:
                name=f.name; json.dump(payload,f,ensure_ascii=False,indent=2)
            os.replace(name,target)
        finally:
            if name and os.path.exists(name): os.unlink(name)
        print(f'{len(services)} Services → {target}')
    finally: wb.close()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--excel',default=str(Path(__file__).with_name('dashboard.xlsx')))
    parser.add_argument('--output',default=str(Path(__file__).with_name('dashboard.json')))
    args=parser.parse_args(); convert(args.excel,args.output)
