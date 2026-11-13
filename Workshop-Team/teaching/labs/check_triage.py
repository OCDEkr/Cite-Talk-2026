"""Check main-fixture output against a hand-specified key, not generated code."""
import csv
import sys
from pathlib import Path

EXPECTED = {
    'E06': ('staff-c', '2026-10-26T09:20:00Z', {'failure_burst'}),
    'E07': ('staff-a', '2026-10-26T12:00:00Z', {'outside_baseline'}),
    'E10': ('staff-f', '2026-10-26T19:00:00Z', {'outside_hours'}),
    'E11': ('staff-g', '2026-10-27T06:59:00Z', {'outside_hours'}),
}


def check(path):
    with Path(path).open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == ['event_id', 'user', 'timestamp_utc', 'reasons'], 'Wrong columns'
        rows = list(reader)
    assert [row['event_id'] for row in rows] == list(EXPECTED), 'Wrong IDs/order or duplicate/missing rows'
    for row in rows:
        user, timestamp, reasons = EXPECTED[row['event_id']]
        assert row['user'] == user and row['timestamp_utc'] == timestamp, 'Source values changed'
        assert set(row['reasons'].split(';')) == reasons, 'Wrong reasons'
    return 'PASS: exact IDs, order, source values and reasons'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 check_triage.py OUTPUT.csv')
    try:
        print(check(sys.argv[1]))
    except (AssertionError, KeyError, OSError) as error:
        raise SystemExit(f'FAIL: {error}')
