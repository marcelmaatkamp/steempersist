#!/usr/bin/python3
from steempersist import SteemPersist
import mycredentials
from steemutils import must_vote
import steem

class PayBots:
    def __init__(self,persistent):
        self.persistent = persistent
    def transfer(self,time,event):
        urlstart = "https://steemit.com/"
        memo = event["memo"]
        if urlstart in memo:
            bot = event["to"]
            if self.persistent["paybot"][bot] == None:
                self.persistent["paybot"][bot] = 0
            self.persistent["paybot"][bot] = self.persistent["paybot"][bot] + 1
            if self.persistent["paybot"][bot] % 10 == 0 and must_vote(mycredentials.account,9985):
                stm=steem.Steem([],keys=mycredentials.keys)
                postlink = memo[len(urlstart):].split()[0]
                print("Downvoting",postlink)
                try:
                    postlink = postlink.split("/",1)[1]
                    print(postlink)
                    stm.vote(postlink,-10.0,mycredentials.account)
                    print("OK")
                except:
                    print("FAIL")

sp = SteemPersist("paybothater")  
pb = PayBots(sp)
sp.set_handlers(pb)
sp()
