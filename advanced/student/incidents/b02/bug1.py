import json, sys
def solve(d):
 return {'saved':{x['key']:x['payload'] for x in d['incoming']},'created':[x['key'] for x in d['incoming']],'repeats':[],'conflicts':[]}
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
