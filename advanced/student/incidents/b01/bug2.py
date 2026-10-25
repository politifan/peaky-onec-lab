import json, sys
def solve(d):
 return sorted({x['line'] for x in d})
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
