#!/usr/bin/python3
import steem
import datetime
import dateutil
import dateutil.parser
import time
import syslog

def must_vote(account,minvp):
    stm=steem.steemd.Steemd()
    acc = stm.get_account(account)
    vp = acc["voting_power"]
    lvt = acc["last_vote_time"]
    more_vp = int((datetime.datetime.utcnow() - dateutil.parser.parse(lvt)).total_seconds() / 43.2)
    if more_vp > 4: #Attempt to fight the stuck at one value issue with the steemit API
        full_vp = vp + more_vp
        if full_vp > minvp:
            return True
    return False

def is_blogpost(nodes,author,permlink):
   stm=steem.steemd.Steemd(nodes)
   c = stm.get_content(author,permlink)
   if c != None and (c["parent_author"] == None or c["parent_author"] == ""):
       return True
   return False

class AwayVote:
    def __init__(self,account,keys,demo_mode=False,nodes=[]):
        self.account = account
        self.nodes=nodes
        self.keys = keys
        self.demo_mode = demo_mode
        self.queue = []
        syslog.syslog("AwayVote using nodes " + str(self.nodes))
        self.stm = steem.steemd.Steemd(self.nodes)
        acc = self.stm.get_account(account)
        self.lvt = dateutil.parser.parse(acc["last_vote_time"])
        self.lvp = acc["voting_power"]
        self.newer_own_vote = False
    def must_vote(self,treshold):
        cur_max_vp = int((datetime.datetime.utcnow() - self.lvt).total_seconds() / 43.2) + self.lvp
        #If the VP cant have gone up enough even without votes, simply return false
        if cur_max_vp < treshold:
            return False
        #self.stm = steem.steemd.Steemd(self.nodes)
        acc = self.stm.get_account(self.account)
        lvt = dateutil.parser.parse(acc["last_vote_time"])
        if lvt == self.lvt and self.newer_own_vote:
            #We can't trust the current lvt yet, need to return false for now.
            return False
        self.lvt = lvt
        self.lvp = acc["voting_power"]
        self.newer_own_vote = False
        max_vp = int((datetime.datetime.utcnow() - self.lvt).total_seconds() / 43.2) + self.lvp
        if cur_max_vp < treshold:
            return False
        return True
    def vote(self,permlink,percentage):
        syslog.syslog("Voting using nodes " + str(self.nodes))
        stm=steem.Steem(self.nodes,keys=self.keys)
        try:
            stm.vote(permlink,percentage,self.account)
            self.newer_own_vote = True
            return True
        except:
            print("Error: Failed to vote. Possibly too low percentage set for voting or too low current voting power.")
            return False
    def upvote(self,permlink,percentage):
        return self.vote(permlink,abs(percentage))
    def downvote(self,permlink,percentage):
        if self.demo_mode:
            syslog.syslog("NOTE: Downvote of "+permlink+" in demo mode:  changing to an upvote instead.")
            #In demo mode, downvotes are turned to upvotes.
            return self.vote(permlink,abs(percentage))
        return self.vote(permlink,0.0 - abs(percentage))

