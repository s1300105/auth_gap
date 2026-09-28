import sys, ipaddress, urllib.request
from urllib.parse import urlparse
import requests, urllib3.util
sys.path.insert(0, sys.argv[1])
from types import SimpleNamespace
from authgap import dparse
from authgap.ir import lit
from authgap.effects import _split_url_slots
print(sys.version.split()[0], sys.argv[1].rsplit("/",1)[1])
for url in ["http://::1%x@evil.example/", "http://fe80::1%x@evil.example/", "http://::1%25@evil.example/", "http://127.0.0.1%x@evil.example/", "http://::ffff:127.0.0.1%a@evil.example:80/"]:
    s = _split_url_slots({"url.host": lit(url)})
    host = s["url.host"].const
    e = SimpleNamespace(kind="NET", slots=s, http_method="GET")
    r = {}
    try: r["ipaddress"] = str(ipaddress.ip_address(host))
    except Exception as ex: r["ipaddress"] = "ValueError"
    try: r["urlparse"] = urlparse(url).hostname
    except Exception as ex: r["urlparse"] = f"EXC {type(ex).__name__}"
    try: r["urllib3"] = urllib3.util.parse_url(url).host
    except Exception as ex: r["urllib3"] = f"EXC {type(ex).__name__}"
    try:
        p = requests.PreparedRequest(); p.prepare_url(url, None); r["requests"] = urllib3.util.parse_url(p.url).host
    except Exception as ex: r["requests"] = f"EXC {type(ex).__name__}"
    print(url, "url.host=", repr(host), "D3=", dparse._d3(e), r)
