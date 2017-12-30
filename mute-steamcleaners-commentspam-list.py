#!/usr/bin/python3
import steem
import json
import mycredentials
import sys
muted = set()
s = steem.Steem([],keys=mycredentials.keys)
try:
    with open("muted.json") as pjson:
        obj = json.loads(pjson.read())
        for account in obj["spambots"]:
            muted.add(account)
    print("Already muted:",len(muted),"spam bots")
except:
    print("Can't process muted.json")
count = 0
try:
    with open("steemcleaners.json") as pjson:
        obj = json.loads(pjson.read())
        for account in obj["spambots"]:
            if not account in muted:
                print("muting",account)
                ojson=["follow",{"follower" : mycredentials.account, "following" : account, "what" : ["ignore"]}]
                s.commit.custom_json("follow",ojson,required_posting_auths=[mycredentials.account])
                muted.add(account)
                count = count + 1
    if count > 0:
        print("Muted",count,"spam bots")
    else:
        print("No new spam bots to mute.")
except:
    print("Something went wrong!")
if count > 0:
    print("Saving muted.")
    obj = dict()
    obj["spambots"] = []
    for account in muted:
        obj["spambots"].append(account)
    js = json.dumps(obj)
    print(js)
    with open("muted.json", "w") as pjson:
        pjson.write(js)
print("Done")
