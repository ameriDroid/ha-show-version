#!/usr/bin/env python3
"""Add or update a release in versions.json.

    tools/add_release.py xmos     <file.bin> <version> [--channel stable|beta|all] [--notes "..."]
    tools/add_release.py firmware <file>     <version> [--channel ...] [--notes "..."]

Copies nothing: put the file under xmos/ or firmware/ yourself first, then pass its path. The script records the
path (relative to versions.json), size and SHA-256 so clients can verify the download.
"""
import argparse
import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FEED = ROOT / "versions.json"

ap = argparse.ArgumentParser()
ap.add_argument("kind", choices=["xmos", "firmware"])
ap.add_argument("file")
ap.add_argument("version")
ap.add_argument("--channel", default="all", choices=["stable", "beta", "all"])
ap.add_argument("--notes", default="")
a = ap.parse_args()

f = pathlib.Path(a.file).resolve()
rel = f.relative_to(ROOT).as_posix()
data = f.read_bytes()
entry = {
    "version": a.version,
    "path": rel,
    "sha256": hashlib.sha256(data).hexdigest(),
    "size": len(data),
    "notes": a.notes,
}

feed = json.loads(FEED.read_text())
channels = list(feed["channels"]) if a.channel == "all" else [a.channel]
for ch in channels:
    old = feed["channels"].setdefault(ch, {}).get(a.kind, {})
    if a.kind == "xmos":
        entry["id"] = old.get("id", "xvf3800-ua-io48-lin-aic3104")
    feed["channels"][ch][a.kind] = dict(entry)
feed["updated"] = datetime.date.today().isoformat()
FEED.write_text(json.dumps(feed, indent=2) + "\n")
print(f"{a.kind} {a.version} -> {', '.join(channels)}  ({rel}, {len(data)} bytes, sha256 {entry['sha256'][:12]}...)")
