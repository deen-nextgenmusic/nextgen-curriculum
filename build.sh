#!/usr/bin/env bash
# Rebuild the handbook and the website. Run from the repository root.
set -euo pipefail
# Once the Cloudflare DNS record exists, run: CUSTOM_DOMAIN=curriculum.nextgenmusic.org ./build.sh
cd src
python3 build.py 00_start.txt 01_warmup.txt 02_mainroom.txt 03_headliner.txt 04_toolkit.txt handbook.html
python3 make_site.py handbook.html ../docs "${CUSTOM_DOMAIN:-}"
rm handbook.html
