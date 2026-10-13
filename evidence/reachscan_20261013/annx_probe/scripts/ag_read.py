import ast, sys
sys.path.insert(0, "/home/user/auth_gap")
from authgap.entries import _read_annotations
from authgap.dparse import d_kind_from
cases = [
    "ToolAnnotations(readOnlyHint=True)",
    "ToolAnnotations(readOnlyHint=settings.ro, destructiveHint=False)",
    "ToolAnnotations(readOnlyHint=RO)",
    "ToolAnnotations(readOnlyHint=1)",
    "ToolAnnotations(readOnlyHint='true')",
    "ToolAnnotations(readOnlyHint=True, **extra)",
    "ToolAnnotations(**{'readOnlyHint': True})",
    "{**BASE, 'openWorldHint': False}",
    "{'openWorldHint': False, **BASE}",
    "{'readOnlyHint': True, 'readOnlyHint': False}",
    "{KEY: True, 'openWorldHint': False}",
    "READ_ONLY",
    "make_ann()",
    "ToolAnnotations(read_only_hint=True)",
    "{'title': 'x'}",
    "ToolAnnotations(idempotentHint=True)",
]
for c in cases:
    node = ast.parse(c, mode="eval").body
    for snake in ("lt2", "ge2", "unknown"):
        if snake != "lt2" and "hint" not in c:
            continue
        ann, form, mal, und = _read_annotations(node, snake)
        dk = d_kind_from(ann, form)
        print(f"{c!s:70} snake={snake:7} -> ann={ann} form={form} mal={mal} und={und} | explicit={dk.explicit} closed={dk.closed_world} idem={dk.idempotent} unknown={dk.unknown} bottom={dk.is_bottom}")
