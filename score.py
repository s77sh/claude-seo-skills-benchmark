"""Tally grader JSON for every graded run. python3 score.py"""
import json, re, os, glob, sys
LAB = sys.argv[1] if len(sys.argv) > 1 else "work/v1"
P = set() if "v2" in LAB else {1, 2, 3, 5, 6, 12, 13, 14, 16, 17, 18, 20}
names = dict(l.split() for l in open(LAB + "/grading/map.txt"))
def load(f):
    try:
        t = open(f).read()
        return json.loads(t[t.index("{"):t.rindex("}") + 1])
    except Exception:
        return None
rows = []
for gid, name in sorted(names.items(), key=lambda x: x[1]):
    g = LAB + "/grading/" + gid
    s = json.load(open(f"{LAB}/runs/{name}/summary.json"))
    out = {"run": name, "cost": round(s["cost_usd"] or 0, 2), "min": round(s["duration_s"] / 60, 1)}
    per = {}
    for who in ("opus", "codex"):
        d = load(f"{g}/{who}.txt")
        if not d: out[who] = None; continue
        sc = {i["n"]: i["score"] for i in d["issues"]}
        per[who] = sc
        out[who] = {"recall": sum(sc.values()), "P": sum(v for k, v in sc.items() if k in P),
                    "S": sum(v for k, v in sc.items() if k not in P), "wrong": len(d["wrong_findings"]),
                    "geo": len(d["geo_advice"]), "unreq": len(d["unrequested"]), "total": d.get("total_findings")}
    if len(per) == 2:
        out["disagree"] = [n for n in range(1, 21) if per["opus"].get(n) != per["codex"].get(n)]
    rows.append(out)
    print(json.dumps(out))
json.dump(rows, open(LAB + "/grading/scores.json", "w"), indent=1)
