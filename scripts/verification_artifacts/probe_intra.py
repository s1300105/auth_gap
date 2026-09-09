import ast, sys, os
sys.path.insert(0, "/home/yudai/Project/research/Master_Project/dispatch-taint-system/dispatch-taint/taintp2x_extension")
import selection_guard as sg

CASES = {}

CASES["M1 log-before-return early exit"] = ('''
def dispatch(name, args):
    if not is_allowed(name):
        logger.warning("denied %s", name)
        return None
    return TOOLS[name](args)          # DISPATCH
''', "TOOLS[name](args)")

CASES["M2 or-disjunction of failures"] = ('''
def dispatch(name, args):
    if not is_allowed(name) or not confirm(name):
        raise PermissionError(name)
    return TOOLS[name](args)          # DISPATCH
''', "TOOLS[name](args)")

CASES["M3 bare await approval"] = ('''
async def dispatch(name, args):
    await confirm(name)
    return TOOLS[name](args)          # DISPATCH
''', "TOOLS[name](args)")

CASES["M4 walrus in test"] = ('''
def dispatch(name, args):
    if (ok := confirm(name)):
        return TOOLS[name](args)      # DISPATCH
    return None
''', "TOOLS[name](args)")

CASES["M5 try/except validator re-raise"] = ('''
def write_file(root, rel, data):
    p = Path(root, rel).resolve()
    try:
        p.relative_to(Path(root).resolve())
    except ValueError:
        raise PermissionError(rel)
    p.write_text(data)                # SINK
''', "p.write_text(data)")

CASES["M6 approval raise swallowed"] = ('''
def dispatch(name, args):
    try:
        require_approval(name)
    except ApprovalDenied:
        logger.warning("proceeding anyway")
    return TOOLS[name](args)          # DISPATCH
''', "TOOLS[name](args)")

CASES["M7 comprehension filter"] = ('''
def dispatch(calls):
    return [TOOLS[c.name](c.args) for c in calls if is_allowed(c.name)]
''', "TOOLS[c.name](c.args)")

CASES["M8 with-CM approval gate"] = ('''
def dispatch(self, name, args):
    with self.require_approval(name):
        return TOOLS[name](args)      # DISPATCH
''', "TOOLS[name](args)")

CASES["M9 suppress swallows approval"] = ('''
def dispatch(name, args):
    with contextlib.suppress(ApprovalDenied):
        require_approval(name)
    return TOOLS[name](args)          # DISPATCH
''', "TOOLS[name](args)")

CASES["M10 for/continue allowlist"] = ('''
def dispatch(calls):
    for c in calls:
        if c.name not in ALLOWED_TOOLS:
            continue
        TOOLS[c.name](c.args)         # DISPATCH
''', "TOOLS[c.name](c.args)")

CASES["M11 subject mismatch"] = ('''
def dispatch(self, name, args):
    if self.is_allowed(self.default_tool):
        return TOOLS[name](args)      # DISPATCH
    return None
''', "TOOLS[name](args)")

CASES["M12 dispatch in finally"] = ('''
def dispatch(name, args):
    try:
        require_approval(name)
    finally:
        TOOLS[name](args)             # DISPATCH
''', "TOOLS[name](args)")

for label, (src, needle) in CASES.items():
    mod = ast.parse(src)
    line = None
    for i, l in enumerate(src.splitlines(), 1):
        if needle in l:
            line = i
            break
    fn = sg.enclosing_function(mod, line)
    gd = sg.guard_dominance(fn, line, mod)
    print(f"{label:38s} line={line} dominates={gd.dominates}")
    for ln, w in gd.dominating:
        print(f"     DOM  L{ln}: {w}")
    for ln, w in gd.non_dominating[:2]:
        print(f"     seen L{ln}: {w}")
