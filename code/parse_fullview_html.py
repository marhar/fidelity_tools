import re
import csv
from bs4 import BeautifulSoup

ASSET_SECTIONS = {'Cash equivalents': 'cash_equivalents', 'Investments': 'investments'}

def parse_fidelity_fullview_html(input_file='~/Downloads/Net Worth-Full View.html', output_file='networth.csv'):
    import os
    input_file = os.path.expanduser(input_file)

    with open(input_file) as f:
        soup = BeautifulSoup(f, 'html.parser')

    date_el = soup.find(class_='acc--asof-date')
    m = re.search(r'(\d{2}/\d{2}/\d{4})', date_el.get_text()) if date_el else None
    extraction_date = m.group(1) if m else ''

    rows = []
    for cat in soup.find_all(class_='asset-category'):
        label_el = cat.find(class_='asset-cat-label')
        label = label_el.get_text(strip=True) if label_el else ''
        section = ASSET_SECTIONS.get(label)
        if not section:
            continue

        for acct in cat.find_all(class_='asset-account'):
            account_name = acct.find(class_='account-name')
            account_val  = acct.find(class_='account-val')
            account_type = acct.find(class_='account-type')
            account_time = acct.find(class_='account-time')
            account_inst = acct.find(class_='account-insti')

            amount_str = account_val.get_text(strip=True).lstrip('$').replace(',', '') if account_val else '0'
            rows.append({
                'extraction_date': extraction_date,
                'section':         section,
                'account_name':    account_name.get_text(strip=True) if account_name else '',
                'amount':          float(amount_str),
                'category':        account_type.get_text(strip=True) if account_type else '',
                'staleness':       account_time.get_text(strip=True) if account_time else '',
                'institution':     account_inst.get_text(strip=True) if account_inst else '',
            })

    fieldnames = ['extraction_date', 'section', 'account_name', 'amount', 'category', 'staleness', 'institution']
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} rows to {output_file}")
    for r in rows:
        print(f"  [{r['section']:18s}] {r['account_name'][:45]:45s} ${r['amount']:>14,.2f}  {r['institution']}")

if __name__ == '__main__':
    parse_fidelity_fullview_html()
