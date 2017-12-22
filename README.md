SteemPersist
===

This repo contains a simple helper class *SteemPersist* that is meant to provide the core loop for blockchain event handling with Python, using steem python.
The *SteemPersist* class is used in conjuction with an event handling client class that implements one or more of the blockchain event type handlers.
Usage *SteemPersist* in a program would look something like this:

```python
#!/usr/bin/python3
from steempersist import SteemPersist

class Demo:
    __init__(self,persistent)L
        self.persistent = persistent
    comment(self,time,event):
        #process 'comment' event here.
        ...
       

sp = SteemPersist("demo")  
demo = Demo(sp)
sp.set_handlers(demo)
sp()
```

The script start by creating a *SteemPersist* object and claiming the name **demo** for this scrip. The script will keep track of persistent meta data in the local file **demo**.json. The meta data kept there will be how far the script is in processing the blockchain events, but also client side meta data. It is important to note that the *SteemPersist* object will sync client data to its json file, eventually, but if the client event handling code results in fatal exceptions at any point, the sync point may be multiple events in the past. Ifr after a crash the script gets invoked again, it will start at the latest synchonisation pont and continue from there. If an event handler has side efects that should not get repeated, then the client is responsible for calling *sync()* on the *SteemPersist* object.

At its basis, *SteemPersist* is an event loop implementation around a coroutine wrapper for the steem python BlockChain::stream\_from method. It is combined with a simple json file that keeps track of blockchain event progress and client side dicts for simple persistent program state. The combination of these two features should make it easy to write simple statistics type bots such as the @croupierbot *Watching The Watchers* script. 

Scripts
===
Next to the core *SteemPersist* andsome misc utils, this repo also contains a number of scripts build on top of this core. The scripts provided are meant to be used from non-script-exclusive accounts as a way to augment the regular usage of your steemit account. Pull requests for adding aditional scripts to the collections or for bug fixes or features for the existing scripts are higly welcomed. 

away-trust-friends-bot.py
===

This script will help to not let your excess voting power go to waste. The script acts on a provided list of *friends*. The idea is that when you are *away* from steemit for a longer time, your voring strength may grow to 100% and stay there for a long time. This means two things:

1) You miss the chance to earn curation rewards
2) Your voting weight will not weigh in in how the reward pool is distributed between different topics.

Now if you have been on steemit for a while, chances are you have met a few people who share your interests, and basically vote like you would have voted. Well, the script uses that fact. When you vote yourself, the script willdo nothing. But when at any time your voting strength grows above 97%, the script will assume that you are *away* and will follow the vote of the next *friend* that votes on anything at the exact same weight as used by your friend.

anti-comment-bot-bot.py
===

While making sure, for example, your voting weight will go to guaranteeing a slice of the reward pool goes to *fiction* instead of *cats* is probably a good way to use your own little bot, the idea that you basically steal curration rewards from your friends (who are doing the currating) may be seen as unethical. Instead of making money from curation you arn't actually doing, an other option is to use your *away* voting power to clean up the steemit eccosystem a bit.

There are a lot of people running bots or using cut-paste strategies in a way of what the ethics are indisputably on the wrong side of good maners. One type of bot is the bot that tries to actually act like a human that interacts with a post author. The bot owner of these bots will use sweeping compliments or other canned fake responses in order to provoke upvotes from the more sociable post creators. 

The *anti-comment-bot-bot* is currently still under construction, so please don't use it yet (pull requests with fixes are highly welcome). Its aim is to detect coment bots like these and monitor for unknowing blog post authors upvoting their automated comments. The script than acts in two ways:

* It mutes the bot for its owner, so if the bot at any time decides to drop by on your own posts, you won't see it.
* It makes a trigger for future comments by this author.

Just like the previous script, this script will only perform triggered actions if the voting weight of it's owner is (very close to) 100%. For this script, 99.85%. If the script detects a new comment by a comment bot, it will downvote to compensate. At this moment in time, using 10% of it's owner total voting weight.

 


