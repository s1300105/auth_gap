import ast, os, sys, json, hashlib
from collections import Counter, defaultdict

TOOL_DECOS = {"tool","tool_plain","function_tool","kernel_function","mcp_tool","toolcall"}
ENUM_BASES = {"Enum","StrEnum","IntEnum","str","IntFlag"}
FORMAT_TYPES = {"HttpUrl","AnyUrl","AnyHttpUrl","EmailStr","IPvAnyAddress","IPv4Address","IPv6Address","FileUrl","PostgresDsn","UUID","datetime","date"}
PATH_TYPES = {"Path","PurePath","FilePath","DirectoryPath","NewPath","PosixPath"}
SCALAR_TYPES = {"int","float","bool"}
OPAQUE_TYPES = {"str","Any","object","dict","Dict","list","List","Optional","Union","JSON"}
CONSTRAINT_KW = {"pattern":"pattern","regex":"pattern","ge":"numeric","gt":"numeric","le":"numeric","lt":"numeric",
                 "max_length":"length","min_length":"length","max_items":"length","min_items":"length",
                 "multiple_of":"numeric","const":"enum","choices":"enum","allow_inf_nan":"numeric"}
APPROVAL_KW = {"requires_confirmation","requires_user_input","external_execution","needs_approval","human_input","confirm"}
DANGER = {
 "EXEC": [("eval",),("exec",),("compile",),("literal_eval",)],
}


def ann_field_list(node):
    """extract explicitly written annotation field names from ToolAnnotations(...)/dict literal"""
    out=[]
    if isinstance(node, ast.Call):
        for k in node.keywords:
            if k.arg: out.append(k.arg)
            elif isinstance(k.value, ast.Dict):
                for kk in k.value.keys:
                    if isinstance(kk, ast.Constant): out.append(str(kk.value))
        for a in node.args:
            if isinstance(a, ast.Dict):
                for kk in a.keys:
                    if isinstance(kk, ast.Constant): out.append(str(kk.value))
    elif isinstance(node, ast.Dict):
        for kk in node.keys:
            if isinstance(kk, ast.Constant): out.append(str(kk.value))
    return out

def dotted(n):
    parts=[]
    while isinstance(n, ast.Attribute):
        parts.append(n.attr); n=n.value
    if isinstance(n, ast.Name): parts.append(n.id)
    elif isinstance(n, ast.Call): parts.append("()")
    return ".".join(reversed(parts))

def danger_kind(func):
    d = dotted(func)
    last = d.split(".")[-1] if d else ""
    if d.startswith("subprocess.") or last in ("Popen","check_output","check_call") or d in ("subprocess.run","subprocess.call"):
        return "SPAWN"
    if d in ("os.system","os.popen","os.execv","os.execve","os.spawnv","pty.spawn"): return "SPAWN"
    if last in ("exec_command","run_command","execute_command"): return "SPAWN"
    if last in ("eval","exec","compile") and not d.startswith("ast."): return "EXEC"
    if last in ("literal_eval",): return None
    if d.startswith("os.remove") or d.startswith("os.unlink") or d.startswith("shutil.rmtree") or last in ("write_text","write_bytes","unlink","rmtree","mkdir","makedirs","rename","copyfile","move"): return "FS_WRITE"
    if last=="open": return "FS_RW"
    if last in ("read_text","read_bytes"): return "FS_READ"
    if d.split(".")[0] in ("requests","httpx","urllib","aiohttp") or last in ("urlopen","urlretrieve"): return "NET"
    if last in ("get","post","put","delete","request") and d.split(".")[0] in ("requests","httpx","session","client","self"): return "NET"
    if last in ("execute","executemany","exec_driver_sql","execute_query"): return "DB"
    return None

def names_in(node):
    out=set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name): out.add(n.id)
        elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name): out.add(n.value.id)
    return out

class FileInfo:
    def __init__(self, tree):
        self.enums=set(); self.models={}
        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef):
                bnames={dotted(b).split(".")[-1] for b in n.bases}
                if bnames & {"Enum","StrEnum","IntEnum","IntFlag","Flag"}: self.enums.add(n.name)
                if bnames & {"BaseModel","BaseModelV1","TypedDict"}: self.models[n.name]=n

def field_constraints(call):
    """constraints declared in Field(...)/constr(...) call"""
    kinds=set(); desc=False
    fn = dotted(call.func).split(".")[-1]
    if fn in ("constr","conint","confloat","conlist","condecimal"):
        for kw in call.keywords:
            k=CONSTRAINT_KW.get(kw.arg)
            if k: kinds.add(k)
        kinds.add("contype")
    if fn in ("Field","FieldInfo"):
        for kw in call.keywords:
            if kw.arg=="description": desc=True
            k=CONSTRAINT_KW.get(kw.arg)
            if k: kinds.add(k)
            if kw.arg in ("json_schema_extra",) and isinstance(kw.value, ast.Dict):
                for kk in kw.value.keys:
                    if isinstance(kk, ast.Constant) and kk.value in ("enum","pattern","format"): kinds.add(str(kk.value))
    return kinds, desc

def classify_annotation(ann, fi):
    """returns (set_of_constraint_kinds, type_label)"""
    if ann is None: return set(), "none"
    kinds=set()
    # unwrap Annotated
    label=None
    def walk_ann(a):
        nonlocal label
        if isinstance(a, ast.Subscript):
            base=dotted(a.value).split(".")[-1]
            sl=a.slice
            if base=="Annotated":
                elts = sl.elts if isinstance(sl, ast.Tuple) else [sl]
                if elts: walk_ann(elts[0])
                for e in elts[1:]:
                    if isinstance(e, ast.Call):
                        k,_=field_constraints(e); kinds.update(k)
            elif base=="Literal":
                kinds.add("enum"); label=label or "Literal"
            elif base in ("Optional","Union","List","list","Sequence","Iterable"):
                elts = sl.elts if isinstance(sl, ast.Tuple) else [sl]
                for e in elts: walk_ann(e)
            else:
                label=label or base
        elif isinstance(a, ast.Constant) and isinstance(a.value,str):
            # string annotation
            s=a.value
            if "Literal[" in s: kinds.add("enum")
            if any(t in s for t in PATH_TYPES): kinds.add("path_type")
            if any(t in s for t in FORMAT_TYPES): kinds.add("format")
            label=label or s.split("[")[0]
        else:
            base=dotted(a).split(".")[-1]
            if base in fi.enums: kinds.add("enum"); label=label or "EnumClass"
            elif base in PATH_TYPES: kinds.add("path_type"); label=label or base
            elif base in FORMAT_TYPES: kinds.add("format"); label=label or base
            elif base in SCALAR_TYPES: label=label or base
            else: label=label or base
    walk_ann(ann)
    return kinds, (label or "?")

def params_from_func(fn, fi):
    out=[]
    a=fn.args
    allargs=list(a.posonlyargs)+list(a.args)+list(a.kwonlyargs)
    defaults={}
    d=a.defaults; pos=list(a.posonlyargs)+list(a.args)
    for i,dv in enumerate(d): defaults[pos[len(pos)-len(d)+i].arg]=dv
    for i,kw in enumerate(a.kwonlyargs):
        if a.kw_defaults[i] is not None: defaults[kw.arg]=a.kw_defaults[i]
    for arg in allargs:
        if arg.arg in ("self","cls"): continue
        kinds,label = classify_annotation(arg.annotation, fi)
        desc=False
        dv=defaults.get(arg.arg)
        if isinstance(dv, ast.Call):
            k,ds=field_constraints(dv); kinds.update(k); desc = desc or ds
        # context params
        if label in ("Context","ToolContext","RunContext","Annotated") or arg.arg in ("ctx","context","run_context","callbacks","config","tool_call_id","state"):
            continue
        out.append({"name":arg.arg,"kinds":sorted(kinds),"type":label,"desc":desc})
    return out

def params_from_model(cls, fi):
    out=[]
    for st in cls.body:
        if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name):
            nm=st.target.id
            if nm.startswith("_") or nm in ("model_config","Config"): continue
            kinds,label = classify_annotation(st.annotation, fi)
            desc=False
            if isinstance(st.value, ast.Call):
                k,ds=field_constraints(st.value); kinds.update(k); desc=desc or ds
            out.append({"name":nm,"kinds":sorted(kinds),"type":label,"desc":desc})
    return out

def schema_props(dnode):
    """parse a JSON-schema dict literal -> list of param dicts"""
    out=[]
    if not isinstance(dnode, ast.Dict): return out
    props=None
    for k,v in zip(dnode.keys,dnode.values):
        if isinstance(k,ast.Constant) and k.value=="properties": props=v
    if not isinstance(props, ast.Dict): return out
    for k,v in zip(props.keys, props.values):
        if not isinstance(k, ast.Constant): continue
        kinds=set(); label="?"; desc=False
        if isinstance(v, ast.Dict):
            for kk,vv in zip(v.keys,v.values):
                if not isinstance(kk, ast.Constant): continue
                key=kk.value
                if key=="enum": kinds.add("enum")
                elif key=="pattern": kinds.add("pattern")
                elif key=="format": kinds.add("format")
                elif key in ("minimum","maximum","exclusiveMinimum","exclusiveMaximum","multipleOf"): kinds.add("numeric")
                elif key in ("minLength","maxLength","minItems","maxItems"): kinds.add("length")
                elif key=="const": kinds.add("enum")
                elif key=="type" and isinstance(vv,ast.Constant): label=str(vv.value)
                elif key=="description": desc=True
        out.append({"name":str(k.value),"kinds":sorted(kinds),"type":label,"desc":desc})
    return out

def body_effects(fn, param_names):
    kinds=set(); ctrl=set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Call):
            k=danger_kind(n.func)
            if k:
                kinds.add(k)
                used=set()
                for a in list(n.args)+[kw.value for kw in n.keywords]:
                    used|=names_in(a)
                ctrl |= (used & set(param_names))
    return kinds, ctrl

def analyze_file(path, repo, rel):
    try:
        src=open(path,encoding="utf-8",errors="replace").read()
    except Exception: return []
    if len(src)>2_000_000: return []
    quick = ("@tool" in src or ".tool(" in src or "@mcp" in src or "function_tool" in src or "kernel_function" in src
             or "BaseTool" in src or "inputSchema" in src or "args_schema" in src or "@app.tool" in src or "@agent.tool" in src or "StructuredTool" in src
             or "ToolSpec" in src or "(Action)" in src or "ToolDefinition" in src)
    if not quick: return []
    try: tree=ast.parse(src)
    except Exception: return []
    fi=FileInfo(tree)
    tools=[]
    # 1. decorated functions
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
            for deco in n.decorator_list:
                call = deco if isinstance(deco, ast.Call) else None
                target = deco.func if call else deco
                dn = dotted(target); last = dn.split(".")[-1]
                if last not in TOOL_DECOS: continue
                if last=="tool" and "." not in dn and dn!="tool": continue
                tl={"repo":repo,"file":rel,"name":n.name,"form":"decorator","deco":dn,
                    "params":params_from_func(n, fi),"annotations":False,"ann_fields":[],
                    "return_direct":False,"approval":[],"schema_source":"signature"}
                if call:
                    for kw in call.keywords:
                        if kw.arg=="annotations":
                            tl["annotations"]=True
                            tl["ann_fields"]=ann_field_list(kw.value)
                        if kw.arg=="return_direct": tl["return_direct"]=True
                        if kw.arg in APPROVAL_KW: tl["approval"].append(kw.arg)
                tools.append(tl); break
    # 2. BaseTool subclasses
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            bn={dotted(b).split(".")[-1] for b in n.bases}
            if not (bn & {"BaseTool","Tool","StructuredTool","BaseAction","Toolkit"}): continue
            if bn & {"Toolkit"}: continue
            args_schema=None; approval=[]; retdirect=False
            for st in n.body:
                tgt=None
                if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name): tgt=st.target.id; val=st.value
                elif isinstance(st, ast.Assign) and len(st.targets)==1 and isinstance(st.targets[0],ast.Name): tgt=st.targets[0].id; val=st.value
                else: continue
                if tgt=="args_schema": args_schema=val
                if tgt=="return_direct": retdirect=True
                if tgt in APPROVAL_KW: approval.append(tgt)
            params=[]; src_kind="none"
            if args_schema is not None:
                mn=dotted(args_schema).split(".")[-1]
                # Type[X] form
                if isinstance(args_schema, ast.Subscript): mn=dotted(args_schema.slice).split(".")[-1]
                if mn in fi.models:
                    params=params_from_model(fi.models[mn], fi); src_kind="args_schema"
            if not params:
                for st in n.body:
                    if isinstance(st,(ast.FunctionDef,ast.AsyncFunctionDef)) and st.name in ("_run","run","_arun"):
                        params=params_from_func(st, fi); src_kind="run_signature"; break
            tools.append({"repo":repo,"file":rel,"name":n.name,"form":"basetool","deco":"","params":params,
                          "annotations":False,"ann_fields":[],"return_direct":retdirect,"approval":approval,
                          "schema_source":src_kind})
    # 2b. llama_index BaseToolSpec / openhands Action schemas
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            bn={dotted(b).split(".")[-1] for b in n.bases}
            if any(b.endswith("ToolSpec") for b in bn):
                for st in n.body:
                    if isinstance(st,(ast.FunctionDef,ast.AsyncFunctionDef)) and not st.name.startswith("_"):
                        ps=params_from_func(st, fi)
                        k,c=body_effects(st,[x["name"] for x in ps])
                        tools.append({"repo":repo,"file":rel,"name":n.name+"."+st.name,"form":"toolspec","deco":"",
                            "params":ps,"annotations":False,"ann_fields":[],"return_direct":False,"approval":[],
                            "schema_source":"signature","effects":sorted(k),"ctrl_params":sorted(c)})
            elif "Action" in bn:
                ps=params_from_model(n, fi)
                tools.append({"repo":repo,"file":rel,"name":n.name,"form":"action_schema","deco":"",
                    "params":ps,"annotations":False,"ann_fields":[],"return_direct":False,"approval":[],
                    "schema_source":"pydantic_action","effects":[],"ctrl_params":[]})
    # 3. Tool(...) literals with inputSchema
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and dotted(n.func).split(".")[-1] in ("Tool","ToolDef"):
            kws={kw.arg:kw.value for kw in n.keywords if kw.arg}
            if "inputSchema" not in kws and "input_schema" not in kws: continue
            sch=kws.get("inputSchema") or kws.get("input_schema")
            nm=kws.get("name")
            nmv=nm.value if isinstance(nm,ast.Constant) else "?"
            annv = "annotations" in kws
            afl=[]
            if annv:
                afl=ann_field_list(kws["annotations"])
            tools.append({"repo":repo,"file":rel,"name":str(nmv),"form":"tool_literal","deco":"",
                          "params":schema_props(sch),"annotations":annv,"ann_fields":afl,
                          "return_direct":False,"approval":[],"schema_source":"inputSchema"})
    # attach effects
    funcs={}
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)): funcs.setdefault(n.name,n)
        if isinstance(n, ast.ClassDef): funcs.setdefault("class:"+n.name,n)
    for t in tools:
        if "effects" in t: continue
        node=None
        if t["form"]=="decorator": node=funcs.get(t["name"])
        elif t["form"]=="basetool": node=funcs.get("class:"+t["name"])
        pn=[p["name"] for p in t["params"]]
        if node is not None:
            k,c=body_effects(node,pn); t["effects"]=sorted(k); t["ctrl_params"]=sorted(c)
        else:
            t["effects"]=[]; t["ctrl_params"]=[]
    return tools

def run(root, label):
    out=[]
    for dp,dns,fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git","node_modules","__pycache__",".venv","venv","site-packages","tests","test","__tests__","testing","docs")]
        for f in fns:
            if not f.endswith(".py"): continue
            if f.startswith("test_") or f.endswith("_test.py"): continue
            p=os.path.join(dp,f)
            rel=os.path.relpath(p, root)
            out.extend(analyze_file(p, label, rel))
    return out

if __name__=="__main__":
    base=sys.argv[1]; outp=sys.argv[2]
    all_tools=[]
    for d in sorted(os.listdir(base)):
        full=os.path.join(base,d)
        if not os.path.isdir(full): continue
        ts=run(full,d)
        all_tools.extend(ts)
        print(f"{d}\t{len(ts)}", file=sys.stderr)
    json.dump(all_tools, open(outp,"w"))
    print("TOTAL", len(all_tools), file=sys.stderr)
