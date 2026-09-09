import ast, sys
sys.path.insert(0, "/home/yudai/Project/research/Master_Project/dispatch-taint-system/dispatch-taint/taintp2x_extension")
import selection_guard as sg
C = {}
C["G1"] = ('''
def dispatch(name, args):
    if not is_allowed(name):
        logger.warning("denied %s", name)
        return ""
    return TOOLS[name](args)
''', "return TOOLS[name](args)")
C["G3-require_approval"] = ('''
async def dispatch(name, args):
    await require_approval(name)
    return TOOLS[name](args)
''', "return TOOLS[name](args)")
C["G13-plugins"] = ('''
def dispatch(self, name, args):
    handler = self.plugins.get(name)
    return handler(args)
''', "return handler(args)")
for k,(src,needle) in C.items():
    mod = ast.parse(src)
    line = next(i for i,l in enumerate(src.splitlines(),1) if needle in l)
    fn = sg.enclosing_function(mod, line)
    gd = sg.guard_dominance(fn, line, mod)
    print(f"{k}: line={line} dominates={gd.dominates} dom={gd.dominating} seen={gd.non_dominating}")
