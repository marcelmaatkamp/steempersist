#!/usr/bin/python3
from steempersist import SteemPersist
import mycredentials
from steemutils import AwayVote
import syslog
#import fakesyslog as syslog

class PayBots:
    def __init__(self,persistent):
        self.line = 0
        self.persistent = persistent
        self.flag_weight = 0.0 - self.persistent.get_config("min_vote",10.0)
        self.away_treshold = self.persistent.get_config("away_treshold",9800)
        self.aw_vote = AwayVote(mycredentials.account,mycredentials.keys,demo_mode=self.persistent.get_config("test_mode",False))
    def transfer(self,time,event):
        urlstart = "https://steemit.com/"
        memo = event["memo"]
        if urlstart in memo:
            self.line = self.line + 1
            bot = event["to"]
            if self.persistent["candidates"][bot] == None:
                syslog.syslog("Potential new upvote bot: " + bot)
                self.persistent["candidates"][bot] = 0
            self.persistent["candidates"][bot] = self.persistent["candidates"][bot] + 1
            if (self.persistent["candidates"][bot] == 20):
                syslog.syslog("20 seperate upvote bot alike transactions seen for " + bot + ", adding bot to the watchlist")
                self.persistent["likely_bots"][bot] = True
            if self.persistent["likely_bots"][bot] == None:
                user = event["from"]
                self.persistent["bot_users"][user] = True
    def vote(self,time,event):
        author = event["author"]
        voter = event["voter"]
        if self.persistent["likely_bots"][voter]!= None and self.persistent["bot_users"][author] != None:
            postlink = "@" + author + "/" + event["permlink"]
            if self.aw_vote.must_vote(self.away_treshold):
                syslog.syslog("Downvoting "+postlink+ " because of "+ voter + " paybot usage")
                self.aw_vote.downvote(postlink,self.flag_weight)
            else:
                syslog.syslog("NOT flagging '"+ postlink + "' for '"+ voter + "' paybot usage, vote power treshold not reached.")
        
sp = SteemPersist("paybothater")  
pb = PayBots(sp)
sp.set_handlers(pb)
sp()
