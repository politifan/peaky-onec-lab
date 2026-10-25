import json,sys
def solve(d):
 return [{"id":x["id"],"cost":x["qty"]*p["price"]} for x in d["lines"] for p in d["prices"] if x["item"]==p["item"]]
if __name__=="__main__":
 print(json.dumps(solve(json.load(sys.stdin)),ensure_ascii=False))
