#!/usr/bin/python3
#A simple demo script for demonstrating the use of steempersist
from steempersist import SteemPersist
import hashlib
import mycredentials
import steem
import datetime
import dateutil
import dateutil.parser
import syslog

#Don't let 100% voting power go to waist, use it. This function returns true if our voting power is higher than 99.85%
def must_vote(account):
    stm=steem.Steem()
    account = stm.get_account(account)
    vp = account["voting_power"]
    lvt = account["last_vote_time"]
    more_vp = int((datetime.datetime.utcnow() - dateutil.parser.parse(lvt)).total_seconds() / 43.2)
    full_vp = vp + more_vp
    if full_vp > 9985:
        return True
    return False

#Event handler for short comments.
class AntiCommentBotBot:
    def __init__(self,pers):
        #Remember the SteemPersist object
        self.pers=pers
    def comment(self,time,event):
        #Only look at short comments
        if len(event["body"]) < 128:
            #Calculate an author specific MD5 digest of the comment
            m = hashlib.md5()
            m.update((event["author"] + "/" + event["body"]).encode())
            digest = m.hexdigest()
            #Count the comment, persistently
            if self.pers["postdigestcount"][digest] == None:
                self.pers["postdigestcount"][digest] = 1
            else:
                self.pers["postdigestcount"][digest] = self.pers["postdigestcount"][digest] + 1
            #If the exact same comment from the exact same author is detected within a one hour time frame, it likely is a silly comment bot.
            if self.pers["postdigestcount"][digest] > 3:
                #Check if we have seen this comment spambot before 
                if self.pers["spambots"][event["author"]] == None:
                    #Remember this spambot account for eternity or untill our owner drops the json file and starts from scratch
                    self.pers["spambots"][event["author"]] = True
                    syslog.syslog("Ignoring spam comment bot: @"+event["author"])
                    #We need to use our posting key in order to ignore the spam bot.
                    stm=steem.Steem([],keys=mycredentials.keys)
                    #Create the structure needed for ignoring the comment spam bot.
                    json=["follow",{"follower" : mycredentials.account, "following" : event["author"], "what" : ["ignore"]}]
                    #Ignore the comment spam bot.
                    stm.commit.custom_json("follow",json,required_posting_auths=[mycredentials.account])
    def vote(self,time,event):
        #A reply post by a known spam bot that got upvoted, this might be a spam comment, if we must vote, we need to do something here.
        if self.pers["spambots"][event["author"]] and event["weight"] > 10 and event["permlink"][:3] == "re-" and must_vote(mycredentials.account):
                #We need to use our posting key to downvote.
                stm=steem.Steem([],keys=mycredentials.keys)
                #The permlink of the spambot post we wish to downvote.
                postlink = "@" + event["author"] + "/" + event["permlink"]
                syslog.syslog("Downvoting upvoted comment by spam bot:",postlink)
                try:
                    #Try to downvote the upvoted comment spambot response that just got upvoted. 
                    stm.vote(postlink,-10.0,mycredentials.account)
                    syslog.syslog("OK")
                except:
                    syslog.syslog("FAIL")
    def hour(self,time,event):
        if time != None:
            self.pers["postdigestcount"].clear()

#Create the SteemPersist object
pers = SteemPersist("anti-comment-bot-bot")
#Create a simple event handler, hand it the SteemPersist object for storing persistent meta info
acb = AntiCommentBotBot(pers)
#Register the event handler as handler for "comment" events.
pers.set_handlers(acb)
#Run the main loop forever.
pers()

