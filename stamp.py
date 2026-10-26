"""Nightly OpenTimestamps job for Off Consensus Research Academy.
Gets salted certificate fingerprints (no personal data) from the portal, stamps new ones, upgrades
earlier proofs until they are anchored in a Bitcoin block, and reports the status back."""
import os, subprocess, datetime, requests, pathlib, re

URL, KEY = os.environ['PORTAL_URL'], os.environ['STAMP_KEY']
PROOFS = pathlib.Path('proofs'); PROOFS.mkdir(exist_ok=True)

items = requests.get(URL, params={'action': 'pending', 'key': KEY}, timeout=60).json().get('items', [])
report = []
for it in items:
    fp = it['fp']
    if not re.fullmatch(r'[0-9a-f]{64}', fp):
        continue
    f = PROOFS / f'{fp}.txt'; ots = PROOFS / f'{fp}.txt.ots'
    if not f.exists():
        f.write_text(fp + '\n')
    if not ots.exists():
        r = subprocess.run(['ots', 'stamp', str(f)], capture_output=True, text=True)
        if r.returncode == 0:
            report.append({'fp': fp, 'status': 'stamped'})
        continue
    r = subprocess.run(['ots', 'upgrade', str(ots)], capture_output=True, text=True)
    out = (r.stdout + r.stderr).lower()
    if ('success' in out or 'complete' in out) and 'not complete' not in out:
        report.append({'fp': fp, 'status': 'anchored', 'date': datetime.datetime.utcnow().isoformat() + 'Z'})

if report:
    requests.post(URL, params={'action': 'stamped'}, json={'key': KEY, 'items': report}, timeout=60)
print(f'{len(items)} fingerprints checked, {len(report)} updated')
