"""Training oracle, not a production detector. Standard library; no network access."""
import csv
import sys
from datetime import datetime
from pathlib import Path


def triage(rows):
    events = []
    seen = set()
    for row in rows:
        if row['event_id'] in seen:
            raise ValueError('Duplicate event ID')
        seen.add(row['event_id'])
        if row['result'] not in {'success', 'failure'}:
            raise ValueError('Unknown result')
        moment = datetime.strptime(row['timestamp_utc'], '%Y-%m-%dT%H:%M:%SZ')
        events.append((moment, row))
    events.sort(key=lambda item: (item[0], item[1]['event_id']))
    flagged = []
    for moment, row in events:
        if row['result'] != 'success':
            continue
        reasons = []
        if not 7 <= moment.hour < 19:
            reasons.append('outside_hours')
        if row['country'] != 'US':
            reasons.append('outside_baseline')
        failures = sum(
            prior['user'] == row['user'] and prior['result'] == 'failure'
            and 0 < (moment - earlier).total_seconds() <= 600
            for earlier, prior in events
        )
        if failures >= 3:
            reasons.append('failure_burst')
        if reasons:
            flagged.append({**{key: row[key] for key in
                           ('event_id', 'user', 'timestamp_utc')},
                           'reasons': ';'.join(reasons)})
    return flagged


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python3 reference_triage.py INPUT.csv OUTPUT.csv')
    source, target = map(Path, sys.argv[1:])
    if source.resolve() == target.resolve():
        raise SystemExit('Output must differ from input')
    with source.open(newline='', encoding='utf-8') as handle:
        flagged = triage(list(csv.DictReader(handle)))
    # Exclusive creation prevents accidental replacement of an earlier result.
    with target.open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=
                                ['event_id', 'user', 'timestamp_utc', 'reasons'])
        writer.writeheader()
        writer.writerows(flagged)
    print(f'{len(flagged)} flagged events written to {target.name}')


if __name__ == '__main__':
    main()
