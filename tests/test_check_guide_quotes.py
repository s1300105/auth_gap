"""scripts/check_guide_quotes.py: 付録 H の原文の引用が下書きの行と一字一句同じかを確かめる道具。"""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("cgq", os.path.join(ROOT, "scripts", "check_guide_quotes.py"))
cgq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cgq)


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_exact_quote_with_blank_line_passes(tmp_path, capsys):
    draft = _write(tmp_path, "d.md", "# 題\n\n本文 1\n本文 2\n")
    doc = _write(tmp_path, "h.md", "> 【原文 L1-3】\n> # 題\n>\n> 本文 1\n\n> 【原文 L4】\n> 本文 2\n")
    assert cgq.check([doc], draft) == 0
    out = capsys.readouterr().out
    assert "一致 2 / 不一致 0" in out
    assert "すべてどれかの引用に入っている" in out


def test_changed_quote_fails(tmp_path, capsys):
    draft = _write(tmp_path, "d.md", "本文 1\n本文 2\n")
    doc = _write(tmp_path, "h.md", "> 【原文 L1-2】\n> 本文 1\n> 本文 二\n")
    assert cgq.check([doc], draft) == 1
    assert "原文と一致しない" in capsys.readouterr().out


def test_short_quote_fails_and_uncovered_lines_reported(tmp_path, capsys):
    draft = _write(tmp_path, "d.md", "a\nb\nc\n")
    doc = _write(tmp_path, "h.md", "> 【原文 L1-2】\n> a\n")
    assert cgq.check([doc], draft) == 1
    out = capsys.readouterr().out
    assert "L1-3" in out  # 一致しなかった引用は網羅に数えない


def test_out_of_range_fails(tmp_path, capsys):
    draft = _write(tmp_path, "d.md", "a\n")
    doc = _write(tmp_path, "h.md", "> 【原文 L2-3】\n> x\n")
    assert cgq.check([doc], draft) == 1
    assert "範囲外" in capsys.readouterr().out
