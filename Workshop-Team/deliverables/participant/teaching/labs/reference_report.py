"""Generate static local HTML; no JavaScript, server or external assets."""
import csv
import html
import sys
from pathlib import Path

FIELDS = ['event_id', 'user', 'timestamp_utc', 'reasons']


def read_rows(path):
    with Path(path).open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle, strict=True)
        if reader.fieldnames != FIELDS:
            raise ValueError('Expected columns: ' + ','.join(FIELDS))
        rows = list(reader)
    if any(set(row) != set(FIELDS) or any(not row[key] for key in FIELDS)
           for row in rows):
        raise ValueError('Each event must have exactly four nonempty fields')
    return rows


def render(rows):
    reasons = {reason for row in rows for reason in row['reasons'].split(';') if reason}
    table = ''.join('<tr>' + ''.join('<td>' + html.escape(row[key]) + '</td>'
                    for key in ('event_id', 'user', 'timestamp_utc', 'reasons')) + '</tr>'
                    for row in rows)
    return f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Synthetic sign-in review</title>
<meta http-equiv="Content-Security-Policy" content="default-src 'none'">
<h1>Synthetic sign-in review</h1>
<p>{len(rows)} events for review; {len(reasons)} reason categories.</p>
<p>Training signals only. These flags do not establish compromise.</p>
<table><caption>Flagged synthetic events</caption><thead><tr>
<th scope="col">Event ID</th><th scope="col">User</th><th scope="col">UTC time</th>
<th scope="col">Reasons</th></tr></thead><tbody>{table}</tbody></table></html>'''


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python3 reference_report.py INPUT.csv OUTPUT.html')
    try:
        rows = read_rows(sys.argv[1])
        content = render(rows)
        with Path(sys.argv[2]).open('x', encoding='utf-8') as handle:
            handle.write(content)
    except (OSError, ValueError, csv.Error) as error:
        raise SystemExit(f'ERROR: {error}')
    print(f'{len(rows)} events rendered as local HTML')
