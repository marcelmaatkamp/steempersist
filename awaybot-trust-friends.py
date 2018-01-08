#!/usr/bin/python3
#A simple demo script for demonstrating the use of steempersist
from steempersist import SteemPersist
from steemutils import must_vote
import mycredentials
import steem
import syslog

#Event handler for short comments.
class AwayTrustFriendsBot:
    def __init__(self,pers):
        #Remember the SteemPersist object
        self.pers=pers
    def vote(self,time,event):
        #Positive vote by a friend for a non comment while we are away and we don't want our voting strenth to go to waste.
        if event["voter"] in mycredentials.friends and event["weight"] > 10 and event["permlink"][:3] != "re-" and must_vote(mycredentials.account,9700):
                #We need to use our posting key to upvote.
                stm=steem.Steem([],keys=mycredentials.keys)
                #The permlink of the spambot post we wish to downvote.
                postlink = "@" + event["author"] + "/" + event["permlink"]
                syslog.syslog("Upvoting upvoted comment by friend:" + event["voter"] + "  :  " + postlink)
                try:
                    #Try to downvote the upvoted comment spambot response that just got upvoted. 
                    stm.vote(postlink,event["weight"]*1.0/100,mycredentials.account)
                    syslog.syslog("OK")
                except:
                    syslog.syslog("FAIL")

#Create the SteemPersist object
pers = SteemPersist("awaybot-trust-friends")
#Create a simple event handler, hand it the SteemPersist object for storing persistent meta info
atf = AwayTrustFriendsBot(pers)
#Register the event handler as handler for "comment" events.
pers.set_handlers(atf)
#Run the main loop forever.
pers()

