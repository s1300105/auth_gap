"""What host would real clients connect to for authority strings the new code calls 'local'."""
import sys
import urllib.request
from urllib.parse import urlparse

import requests
import urllib3.util

AUTH = [
    "[::1]:8080", "user:pw@localhost", "localhost.", "[2002:808:808::1]:80", "localhost..", "localhost.:8080",
    "evil.example@localhost", "a@b@localhost", "evil.example\t@localhost", "\nlocalhost",
    "[::1%@evil.example]", "evil.example .localhost", "[fe80::1%25eth0]", "[::1%25@evil.example]",
    "localhost%00.evil.example", "localhost\x00.evil.example", "127.0.0.1%2f@evil.example",
]
print(sys.version.split()[0])
for a in AUTH:
    url = "http://" + a + "/x"
    out = {}
    try:
        out["urlparse"] = urlparse(url).hostname
    except Exception as e:
        out["urlparse"] = f"EXC {type(e).__name__}"
    try:
        out["urllib3"] = urllib3.util.parse_url(url).host
    except Exception as e:
        out["urllib3"] = f"EXC {type(e).__name__}"
    try:
        p = requests.PreparedRequest()
        p.prepare_url(url, None)
        out["requests"] = urllib3.util.parse_url(p.url).host
    except Exception as e:
        out["requests"] = f"EXC {type(e).__name__}: {str(e)[:40]}"
    try:
        out["urllib.request"] = urllib.request.Request(url).host
    except Exception as e:
        out["urllib.request"] = f"EXC {type(e).__name__}"
    print(repr(a), out)
