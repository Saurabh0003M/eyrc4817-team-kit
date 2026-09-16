#!/usr/bin/env python3
"""
Link checker for the team docs (RESOURCES.md, README.md, the roadmap source).

    python3 learning/tools/check_links.py                 # checks the default files
    python3 learning/tools/check_links.py some_file.md    # or specific files

YouTube links are checked through YouTube's oEmbed service (a normal page request always says
"200 OK", even for deleted videos). Colab links are checked on the GitHub file they open.
Portal links need a login and are skipped. docs.opencv.org blocks automated requests, so it's
reported as "blocked", not "broken".
"""
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_FILES = ['RESOURCES.md', 'README.md', 'learning/source/roadmap.md']
URL_PATTERN = re.compile(r'https?://[^\s)\]>"\'`|]+')
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) eyrc4817-link-check'}


def probe_url(url):
    if 'portal.e-yantra.org' in url:
        return url, 'skip', 'portal login needed'
    target = url
    if 'youtube.com' in url or 'youtu.be' in url:
        target = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(url, safe='')
    elif 'colab.research.google.com/github/' in url:
        target = url.replace('colab.research.google.com/github/', 'github.com/')
    request = urllib.request.Request(target.split('#')[0], headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return url, 'ok', str(response.status)
    except urllib.error.HTTPError as error:
        if error.code in (401, 403, 429) and 'youtube' not in target:
            return url, 'blocked', f'HTTP {error.code} (bot protection; open in a browser)'
        return url, 'broken', f'HTTP {error.code}'
    except Exception as error:  # timeouts, DNS, TLS
        return url, 'broken', type(error).__name__


def main():
    files = sys.argv[1:] or [str(REPO / f) for f in DEFAULT_FILES]
    urls = sorted({m.rstrip('.,;') for f in files for m in URL_PATTERN.findall(Path(f).read_text(encoding='utf-8'))
                   if '<' not in m})
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(probe_url, urls))
    counts = {}
    for url, status, detail in results:
        counts[status] = counts.get(status, 0) + 1
        if status in ('broken', 'blocked'):
            print(f'[{status}] {url}  —  {detail}')
    print(f'\nChecked {len(urls)} unique links: ' + ', '.join(f'{v} {k}' for k, v in sorted(counts.items())))
    sys.exit(1 if counts.get('broken') else 0)


if __name__ == '__main__':
    main()
