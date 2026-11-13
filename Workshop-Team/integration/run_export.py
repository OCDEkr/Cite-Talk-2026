"""Bounded native export. Does not close/save unrelated presentations or quit PowerPoint."""
from pathlib import Path
import json
import subprocess
import sys
import time

source = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve()
team = Path(__file__).resolve().parent.parent
assert source.is_relative_to(team) and target.is_relative_to(team)
assert not target.exists(), 'Use a fresh export path; existing PDF is preserved.'
start = time.monotonic()
command = ['/usr/bin/osascript', str(Path(__file__).with_name('export_powerpoint.applescript')),
           str(source), str(target), source.name]
try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=50)
    record = dict(command=command, exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
except subprocess.TimeoutExpired as exc:
    record = dict(command=command, exit_code=None, error='50-second process timeout',
                  stdout=str(exc.stdout or ''), stderr=str(exc.stderr or ''))
record.update(elapsed_seconds=round(time.monotonic()-start, 2),
              pdf_exists=target.exists(), pdf_bytes=target.stat().st_size if target.exists() else 0)
target.with_suffix('.export.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
sys.exit(0 if record.get('exit_code') == 0 and record['pdf_bytes'] else 1)
