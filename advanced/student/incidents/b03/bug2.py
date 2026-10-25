import json, sys
def solve(d):
 return dict(d['saved'],version=d['target_version'])
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
