#!/usr/bin/env python3
"""Delete encrypted My-files blobs whose 2-hour window has passed (see vault/expiry.json)."""
import json, os, time

path = "vault/expiry.json"
if not os.path.exists(path):
    raise SystemExit("no expiry list")
expiry = json.load(open(path))
now = time.time()
gone = [b for b, t in expiry.items() if t <= now]
for b in gone:
    f = f"vault/{b}.bin"
    if os.path.exists(f):
        os.remove(f)
        print("deleted", f)
    del expiry[b]
# also forget entries whose file is already missing
for b in [b for b in expiry if not os.path.exists(f"vault/{b}.bin")]:
    del expiry[b]
json.dump(expiry, open(path, "w"), indent=1, sort_keys=True)
print(f"{len(gone)} expired, {len(expiry)} still waiting")
