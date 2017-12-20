#!/usr/bin/python3
#A simple demo script for demonstrating the use of steempersist
from steempersist import SteemPersist
import hashlib

#Event handler for short comments.
class Demo:
    def __init__(self,pers):
        #Remember the SteemPersist object
        self.pers=pers
    def __call__(self,time,event):
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
            #If the exact same comment from the exact same author is detected, it likely is a silly comment bot.
            if self.pers["postdigestcount"][digest] > 3:
                print(time,self.pers["postdigestcount"][digest], event["author"],event["body"])
    def clear(self,time,event):
        print("CLEAR")
        self.pers["postdigestcount"].clear()

#Create the SteemPersist object
pers = SteemPersist("persist-demo")
#Create a simple event handler, hand it the SteemPersist object for storing persistent meta info
demo_comment = Demo(pers)
#Register the event handler as handler for "comment" events.
pers.set_handler("comment",demo_comment)
#Call clear every hour
pers.set_handler("hour",demo_comment.clear)
#Run the main loop forever.
pers()

