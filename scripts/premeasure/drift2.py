import subprocess, os, sys, json
sys.path.insert(0,'an')
import scan
base='corpus_mcp'
out={}
for line in open('drift_list.txt'):
    name,url=line.split()
    d=os.path.join(base,name)
    def has(ref):
        return subprocess.run(['git','-C',d,'rev-parse','--verify','-q',ref],capture_output=True).returncode==0
    if not (has('refs/tags/authgap_old') and has('refs/tags/authgap_new')): continue
    res={}
    ok=True
    for ref in ('authgap_old','authgap_new'):
        r=subprocess.run(['git','-C',d,'checkout','-q','--force',ref],capture_output=True,timeout=300)
        if r.returncode!=0: print("CHECKOUTFAIL",name,ref,r.stderr[-200:]); ok=False; break
        res[ref]=scan.run(d,name)
    if ok: out[name]=res
    subprocess.run(['git','-C',d,'checkout','-q','--force','-'],capture_output=True)
json.dump(out, open('drift_raw.json','w'))
print("repos scanned:", len(out))
