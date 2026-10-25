import json,sys
def solve(d):
 return sorted({r["warehouse"] for r in d["shown"] if r["warehouse"] not in d["allowed"] and r.get("visible",False)})
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin))))
