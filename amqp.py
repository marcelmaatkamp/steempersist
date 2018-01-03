#!/usr/bin/python3
from steempersist import SteemPersist
from steemutils import must_vote
import mycredentials
import steem
import syslog

import pika
import json

class AMQP:
    def __init__(self,pers,channel):
        self.pers=pers
        self.channel=channel
    def other(self,time,event):	
        print(time, event)
        message = json.dumps(event)
        channel.basic_publish(exchange='steemit', routing_key='', body=json.dumps(event))

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.20.0.5'))
channel = connection.channel()

pers = SteemPersist("amqp")
atf = AMQP(pers, channel)
pers.set_handlers(atf)
pers()
