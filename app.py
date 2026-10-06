from flask import Flask, jsonify, send_from_directory
from pathlib import Path
import json,re,datetime,urllib.request
BASE=Path(__file__).resolve().parent
app=Flask(__name__,static_folder=str(BASE),static_url_path="")
OFFICIAL="https://ff.garena.com/en/news/"
def latest_ob():
    req=urllib.request.Request(OFFICIAL,headers={"User-Agent":"HASAN-SENSI-X/1.0"})
    with urllib.request.urlopen(req,timeout=12) as r: s=r.read().decode("utf-8","ignore")
    m=re.search(r'OB\s*([0-9]+)\s*PATCH\s*NOTES',s,re.I)
    if not m: raise RuntimeError("No OB patch found")
    return "OB"+m.group(1)
@app.get("/")
def home(): return send_from_directory(BASE,"index.html")
@app.get("/api/patch")
def patch():
    p=BASE/"patch_state.json"; d=json.loads(p.read_text())
    try:
        v=latest_ob()
        if v!=d["version"]:
            d["version"]=v; d["updated_at"]=datetime.date.today().isoformat()
            d["rules_version"]="calculated-"+v.lower()+"-pending"
            d["rules"]["note"]="New patch detected; values remain calculated until rules are reviewed."
            p.write_text(json.dumps(d,indent=2))
    except Exception: pass
    return jsonify(d)
if __name__=="__main__": app.run(host="0.0.0.0",port=8080)
