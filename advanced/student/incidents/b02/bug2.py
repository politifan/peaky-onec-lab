import json, sys
def solve(d):
 return sorted(set(d['ack'])-set(d['sent']))
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
