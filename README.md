# ha-show-version

The version feed for the ameriDroid HA Show. The **HA Show Manager** service on the device reads
`versions.json` from here to tell the user what is installed and whether something newer is available:

* **XMOS XVF3800 mic array firmware**: USB DFU images, flashed from the device.
* **HA Show firmware** (main system image): OTA is not published yet; the entry is a placeholder so the
  device can already show its version.

Feed URL (public repo, no token needed):

    https://raw.githubusercontent.com/ameriDroid/ha-show-version/main/versions.json

## `versions.json`

```json
{
  "schema": 1,
  "updated": "2026-10-10",
  "channels": {
    "stable": {
      "xmos":     { "id": "xvf3800-ua-io48-lin-aic3104", "version": "1.0.1",
                    "path": "xmos/xvf3800_ua-io48-lin_aic3104_v1.0.1.bin",
                    "sha256": "…", "size": 921600, "notes": "…" },
      "firmware": { "version": "0.1.0", "path": "", "sha256": "", "size": 0, "notes": "…" }
    },
    "beta": { "xmos": { … }, "firmware": { … } }
  }
}
```

| Field | Meaning |
| --- | --- |
| `schema` | Feed format version. Clients ignore feeds they do not understand. |
| `channels.<name>` | `stable` (default) or `beta`. The device picks one in the manager's settings. |
| `xmos` / `firmware` | The newest release of that component in the channel. |
| `version` | Dotted numeric version, compared part by part (`1.0.10` is newer than `1.0.9`). |
| `path` | File location relative to `versions.json`. Empty means "not downloadable yet": the version is shown but no update is offered. A full `url` field may be used instead of `path`. |
| `sha256`, `size` | Verified by the device before it installs anything. |
| `id` (xmos) | Hardware/build variant of the image (`ua-io48-lin` target, `aic3104` codec). |
| `notes` | Short release notes shown next to the update. |

An update is offered when `version` is newer than what the device reports (XMOS: the `VERSION` control
command, firmware: `ro.hashow.version`).

## Publishing a release

1. Put the file under `xmos/` (or `firmware/`).
2. Register it: `tools/add_release.py xmos xmos/<file>.bin 1.2.0 --channel stable --notes "what changed"`
   (this records the path, size and SHA-256 and bumps `updated`; use `--channel beta` to stage it first).
3. Commit and push. Devices pick it up on their next check (every few hours, or when the user taps
   **Check for updates**).

`xmos/xvf3800_ua-io48-lin_aic3104_v1.0.0.bin` is kept as a downgrade image for flash/OTA testing; it is not
listed in the feed.
