#!/usr/bin/python3
import steem
import json
spambots = set()
s=steem.steemd.Steemd()
entries = s.get_blog_entries("steemcleaners",-1,4)
for entry in entries:
    content = s.get_content("steemcleaners",entry["permlink"])["body"]
    parts = content.split("# Report\n")
    if len(parts) > 1:
        body = parts[1]
        lines = body.split("\n")
        for line in lines:
            parts = line.split("|")
            if len(parts) >5:
                link = parts[1]
                abuse_type = parts[2]
                if "Comment Spam" in abuse_type:
                    p2 = link.split("@")
                    if len(p2) > 1:
                        p3 = p2[1].split("/")
                        if len(p3) > 1:
                            spambots.add(p3[0])
sb_obj = dict()
sb_obj["spambots"] = []
for bot in sorted(spambots):
    sb_obj["spambots"].append(bot)
with open("steemcleaners.json", "w") as pjson:
    pjson.write(json.dumps(sb_obj))
print("Done")

