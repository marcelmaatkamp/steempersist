#!/usr/bin/python3
from steempersist import SteemPersist
import mycredentials
from steemutils import AwayVote,is_blogpost
import hashlib
import syslog
#import fakesyslog as syslog

class PayBots:
    def __init__(self,persistent):
        self.persistent = persistent
    def comment(self,time,event):
        if event["parent_author"] != None and event["parent_author"] != "":
            body = event["body"]
            body.replace("@"+event["parent_author"],"BLOG_AUTHOR")
            m = hashlib.md5()
            m.update(body.encode())
            digest = m.hexdigest()
            if self.persistent["hourly_hashes"][digest] == None:
                self.persistent["hourly_hashes"][digest] = 0
            self.persistent["hourly_hashes"][digest] = self.persistent["hourly_hashes"][digest] + 1
            if self.persistent["hourly_hashes"][digest] == 6: #Six times in one hour, might be bot stuff.
                self.persistent["candidate_hashes"][digest] = True
            if self.persistent["candidate_hashes"][digest]:
                if is_blogpost(self.persistent.get_config("nodes",[]),event["parent_author"],(event["parent_permlink"])):
                    if self.persistent["candidate_bots"][event["author"]] == None:
                        self.persistent["candidate_bots"][event["author"]] = 0
                    self.persistent["candidate_bots"][event["author"]] = self.persistent["candidate_bots"][event["author"]] + 1
                    if self.persistent["candidate_bots"][event["author"]] == 20:
                        if self.persistent["bots"][event["author"]] == None:
                            self.persistent["bots"][event["author"]] = True
            if self.persistent["bots"][event["author"]] and self.persistent["candidate_hashes"][digest]:
                if self.persistent["bot_text"]["@" + event["author"] + " : " + body ] == None:
                    syslog.syslog("@" + event["author"] + " : " + body)
                    self.persistent["bot_text"]["@" + event["author"] + " : " + body ] = True
    def vote(self,time,event):
        pass
    def hour(self,time,event):
        self.persistent["hourly_hashes"].clear()

        
sp = SteemPersist("awaybot-commentbot")  
pb = PayBots(sp)
sp.set_handlers(pb)
sp()
