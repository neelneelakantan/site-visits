# site-visits

A small, self‑contained utility for inspecting high‑level browsing patterns from
Chrome’s history database. The script copies Chrome’s locked SQLite file into a
local working copy, extracts recent visit events, aggregates domains, and
produces simple visual summaries.

All processing is local. No data is transmitted or stored outside the machine.

---

## Features

- Local copy of Chrome’s history database (avoids file‑locking issues)
- Extraction of recent visit events (URL, title, timestamp)
- Conversion of Chrome’s WebKit timestamps to standard datetimes
- Domain‑level aggregation and frequency counts
- Optional visualizations:
  - Top domains (horizontal bar chart)
  - Long‑tail distribution (log‑scale plot)
- Minimal, dependency‑light implementation

---

## Installation

Requires Python 3.10+.

Optional (for charts):

```bash
pip install matplotlib
```

## Usage

Run the script directly:
```
python history_extractor.py
```