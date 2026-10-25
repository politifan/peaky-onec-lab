import json, sys
def solve(d):
 return sorted(x['id'] for x in d['old'] if not any(y['id']==x['id'] for y in d['new']))
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
