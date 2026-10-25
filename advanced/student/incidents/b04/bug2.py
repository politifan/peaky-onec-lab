import json, sys
def solve(d):
 return [dict(x,code='T-'+str(x['id'])) for x in sorted(d['rows'],key=lambda x:x['id'])]
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
