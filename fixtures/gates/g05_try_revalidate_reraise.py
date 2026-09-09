"""G5: try/except でパス検証が再送出する。

期待: DOM(strong-path -> OP)。前身は NODOM で誤 FN。
拒否側（例外辺）は handler で `raise` に終わるので効果へ到達しない。
"""

from _prelude import validate_path

ROOT = "/srv/data"


def read_file(path):
    try:
        safe = validate_path(path, ROOT)  # WITNESS
    except ValueError:
        raise PermissionError(path) from None
    with open(safe) as fh:  # EFFECT
        return fh.read()
