"""資料の引用が、その URL の中に本当にあるかを確かめ、どこにあるかを返す。

文献・文書の調査（例: 宣言の使われ方の資料集）で、[確認] の印を付ける前に使う。
LLM の要約には頼らず、取ってきた中身を文字列で照らし合わせる（CLAUDE.md 規則 1）。

使い方:
    python scripts/verify_quote.py URL "引用の文"            # 1 件
    python scripts/verify_quote.py --batch in.json --out out.json  # 複数件

in.json は [{"id": ..., "url": ..., "quote": ...}, ...]。

照合のしかた（どれで当たったかを match に書く）:
- exact: 空白のつながり方だけを無視して、文字どおり一致した。
- loose: 加えて、Markdown の記号（` * _）と引用符の形（“ ” ’ など）と大文字小文字を無視して一致した。
- script_only: ページの本文には無く、<script> の中（ページを組み立てるデータ）にだけあった。
- none: 見つからなかった。

場所（どこに書いてあるか）:
- HTML: 一致した位置より前の見出し（h1〜h6）の連なりと、見出しの id（URL#id で直接開ける）。
- Markdown / ソースコード / テキスト: 行番号（1 始まり）と、直前の Markdown 見出し。
- PDF: ページ番号（pypdf があれば）。

取ってきた中身は sha256 と取得日時を記録する。キャッシュは環境変数 VERIFY_QUOTE_CACHE の
ディレクトリ（既定は /tmp/verify_quote_cache）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

CACHE = os.environ.get("VERIFY_QUOTE_CACHE", "/tmp/verify_quote_cache")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

BLOCK = {"p", "div", "section", "article", "main", "header", "footer", "li", "ul", "ol", "table", "tr",
         "td", "th", "br", "pre", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "dt", "dd", "aside",
         "nav", "summary", "details", "figure", "figcaption"}
HEAD = {"h1", "h2", "h3", "h4", "h5", "h6"}


def fetch(url: str) -> dict:
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    body_p = os.path.join(CACHE, key + ".body")
    meta_p = os.path.join(CACHE, key + ".json")
    if os.path.exists(body_p) and os.path.exists(meta_p):
        meta = json.load(open(meta_p))
        meta["body"] = open(body_p, "rb").read()
        return meta
    cmd = ["curl", "-sS", "-L", "--max-time", "45", "-A", UA, "-o", body_p,
           "-w", "%{http_code}\t%{content_type}\t%{url_effective}", url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    parts = (r.stdout or "").split("\t")
    meta = {"url": url, "status": parts[0] if parts else "",
            "content_type": parts[1] if len(parts) > 1 else "",
            "final_url": parts[2] if len(parts) > 2 else "",
            "fetched_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "curl_error": r.stderr.strip()[:300]}
    body = open(body_p, "rb").read() if os.path.exists(body_p) else b""
    meta["sha256"] = hashlib.sha256(body).hexdigest()
    meta["bytes"] = len(body)
    if meta["status"] == "200":
        json.dump(meta, open(meta_p, "w"))
    meta["body"] = body
    return meta


class _Text(HTMLParser):
    """HTML を本文の文字列にし、見出しの位置と id を控える。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.script: list[str] = []
        self.heads: list[tuple[int, int, str, str]] = []  # (offset, level, text, id)
        self._skip = 0
        self._in_script = 0
        self._head = None  # [level, id, [text]]
        self._last_id = ""

    def _len(self):
        return sum(len(s) for s in self.out)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "template"):
            self._in_script += 1
            return
        if tag in ("svg",):
            self._skip += 1
        if a.get("id"):
            self._last_id = a["id"]
        if tag in HEAD:
            self._head = [int(tag[1]), a.get("id", ""), []]
        elif self._head is not None and tag == "a" and (a.get("id") or (a.get("href", "").startswith("#"))):
            if not self._head[1]:
                self._head[1] = a.get("id") or a.get("href", "")[1:]
        if tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template"):
            self._in_script = max(0, self._in_script - 1)
            return
        if tag == "svg":
            self._skip = max(0, self._skip - 1)
        if tag in HEAD and self._head is not None:
            lvl, hid, txt = self._head
            t = _norm_chars(re.sub(r"\s+", " ", "".join(txt))).strip().rstrip("#").strip()
            self.heads.append((self._len(), lvl, t, hid))
            self._head = None
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self._in_script:
            self.script.append(data)
            return
        if self._skip:
            return
        self.out.append(data)
        if self._head is not None:
            self._head[2].append(data)


_QUOTES = {"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'", "\u00a0": " ", "\u2014": "-",
           "\u2013": "-", "\u2026": "...", "\u200b": "", "\u200c": "", "\u200d": "", "\ufeff": ""}


def _norm_chars(s: str) -> str:
    for k, v in _QUOTES.items():
        s = s.replace(k, v)
    return s


_HSPACE = set(" \t\r\f\v")


def _norm_map(s: str, collapse_hspace: bool = False) -> tuple[str, list[int]]:
    """_norm_chars と同じ置き換えをし、置き換えた後の各文字が元の何文字目かの表も返す。

    置き換えで長さが変わる文字（… → ...、ゼロ幅の文字の削除）があっても、一致した位置を元の文字列の
    位置に戻せる。見出しや行番号は元の位置で引く（前は置き換えた後の位置で引いていたので、前に
    長さの変わる文字があると、見出しが前の節に、行番号が後ろの行にずれた）。
    """
    out: list[str] = []
    idx: list[int] = []
    prev_space = False
    for i, ch in enumerate(s):
        rep = _QUOTES.get(ch, ch)
        if collapse_hspace and rep in _HSPACE:
            if prev_space:
                continue
            rep = " "
        prev_space = collapse_hspace and rep == " "
        for c in rep:
            out.append(c)
            idx.append(i)
    idx.append(len(s))
    return "".join(out), idx


def _pattern(quote: str, loose: bool) -> re.Pattern:
    q = _norm_chars(html.unescape(quote)).strip()
    if loose:
        q = re.sub(r"[`*_]", " ", q)
        q = q.replace('"', " ").replace("'", " ")
    toks = [t for t in re.split(r"\s+", q) if t]
    if not toks:
        raise ValueError("empty quote")
    sep = r"[\s`*_\"'\\]*" if loose else r"\s+"
    body = sep.join(re.escape(t) for t in toks)
    return re.compile(body, re.I if loose else 0)


def _search(text: str, quote: str, normalized: bool = False):
    t = text if normalized else _norm_chars(text)
    for mode, loose in (("exact", False), ("loose", True)):
        p = _pattern(quote, loose)
        ms = list(p.finditer(t))
        if ms:
            return mode, ms
    return "none", []


def _heading_path(heads, off):
    path = []
    for o, lvl, txt, hid in heads:
        if o > off:
            break
        path = [h for h in path if h[0] < lvl] + [(lvl, txt, hid)]
    return path


def locate(url: str, quote: str) -> dict:
    meta = fetch(url)
    res = {k: meta.get(k) for k in ("url", "final_url", "status", "content_type", "fetched_at", "sha256", "bytes")}
    res["quote"] = quote
    body = meta["body"]
    if meta.get("status") != "200":
        res.update(match="fetch_failed", error=meta.get("curl_error"))
        return res
    ct = (meta.get("content_type") or "").lower()
    if "pdf" in ct or body[:5] == b"%PDF-":
        try:
            import io

            from pypdf import PdfReader  # type: ignore
            pages = [p.extract_text() or "" for p in PdfReader(io.BytesIO(body)).pages]
        except Exception as e:  # noqa: BLE001
            res.update(match="unsupported_pdf", error=str(e)[:200])
            return res
        hits = []
        mode = "none"
        for i, pt in enumerate(pages, 1):
            m, ms = _search(pt, quote)
            if ms:
                mode = m if mode in ("none", "loose") else mode
                hits.append({"page": i, "context": _ctx(_norm_chars(pt), ms[0])})
        res.update(match=mode if hits else "none", count=len(hits), hits=hits[:5], kind="pdf")
        return res
    text = body.decode("utf-8", errors="replace")
    is_html = "html" in ct or re.match(r"\s*(<!doctype html|<html)", text[:500], re.I)
    if is_html:
        p = _Text()
        p.feed(text)
        raw = "".join(p.out)
        page, idx = _norm_map(raw, collapse_hspace=True)
        mode, ms = _search(page, quote, normalized=True)
        if not ms:
            m2, ms2 = _search(html.unescape("\n".join(p.script)).replace("\\n", "\n").replace('\\"', '"'), quote)
            res.update(match="script_only" if ms2 else "none", count=len(ms2), kind="html")
            return res
        # 見出しの位置（p.heads）は元の文字列 raw の位置なので、一致した位置も raw の位置に戻して比べる
        heads = p.heads
        hits = []
        for m in ms[:5]:
            path = _heading_path(heads, idx[m.start()])
            last_id = next((h[2] for h in reversed(path) if h[2]), "")
            base = meta.get("final_url") or url
            hits.append({"heading_path": " > ".join(h[1] for h in path),
                         "heading_id": last_id,
                         "anchored_url": (base.split("#")[0] + "#" + last_id) if last_id else "",
                         "context": _ctx(page, m)})
        res.update(match=mode, count=len(ms), hits=hits, kind="html")
        return res
    lines = text.split("\n")
    norm, idx = _norm_map(text)
    mode, ms = _search(norm, quote, normalized=True)
    hits = []
    for m in ms[:5]:
        a, b = idx[m.start()], idx[max(m.start(), m.end() - 1)] + 1
        l0 = text.count("\n", 0, a) + 1
        l1 = text.count("\n", 0, b) + 1
        head = ""
        for i in range(l0 - 1, -1, -1):
            if re.match(r"#{1,6}\s", lines[i]):
                head = lines[i].strip()
                break
        hits.append({"lines": f"{l0}-{l1}" if l1 != l0 else str(l0), "md_heading": head,
                     "context": _ctx(norm, m)})
    res.update(match=mode, count=len(ms), hits=hits, kind="text")
    return res


def _ctx(t: str, m, n: int = 160) -> str:
    s = t[max(0, m.start() - n): m.end() + n]
    return re.sub(r"\s+", " ", s).strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url", nargs="?")
    ap.add_argument("quote", nargs="?")
    ap.add_argument("--batch")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.batch:
        items = json.load(open(a.batch))
        out = []
        for it in items:
            try:
                r = locate(it["url"], it["quote"])
            except Exception as e:  # noqa: BLE001
                r = {"url": it.get("url"), "quote": it.get("quote"), "match": "error", "error": str(e)[:200]}
            r["id"] = it.get("id")
            out.append(r)
        s = json.dumps(out, ensure_ascii=False, indent=1)
        if a.out:
            open(a.out, "w").write(s)
        else:
            print(s)
        return 0
    if not (a.url and a.quote):
        ap.error("URL と引用の文、または --batch を渡す")
    print(json.dumps(locate(a.url, a.quote), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
