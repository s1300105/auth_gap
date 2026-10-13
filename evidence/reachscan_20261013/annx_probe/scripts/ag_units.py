import os, sys
sys.path.insert(0, "/home/user/auth_gap")
from authgap.srcindex import SourceIndex
from authgap.entries import find_units, find_tool_literals, join_annotations, mcp_version_class
from authgap.dparse import parse_d_kind, parse_d_kind_by_tool
base = sys.argv[1]
for case in sorted(os.listdir(base)):
    root = os.path.join(base, case)
    idx = SourceIndex(root)
    units = find_units(idx)
    lits = find_tool_literals(idx)
    j, uj = join_annotations(units, lits)
    print(f"== {case}: version={mcp_version_class(idx)[0]} parse_failures={idx.parse_failures} units={len(units)} literals={[(l.name, l.annotations, l.form) for l in lits]} joined={j} unjoined={uj}")
    for u in units:
        dk = parse_d_kind(u)
        print(f"   unit {u.framework}:{u.qualname} tool={u.tool_name} ann={u.annotations} form={u.annotation_form} dispatch={getattr(u,'dispatch_names',None)} dispatch_ann={u.dispatch_annotations} | explicit={dk.explicit} unknown={dk.unknown} malformed={dk.malformed} bottom={dk.is_bottom}")
