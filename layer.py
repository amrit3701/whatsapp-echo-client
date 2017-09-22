# -*- coding: utf-8 -*-
import os, subprocess, time
#import RPi.GPIO as GPIO

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(14, GPIO.OUT)

from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause

#Log, but only creates the file and writes only if you kill by hand from the console (CTRL + C)
#import sys
#class Logger(object):
#    def __init__(self, filename="Default.log"):
#        self.terminal = sys.stdout
#        self.log = open(filename, "a")
#
#    def write(self, message):
#        self.terminal.write(message)
#        self.log.write(message)
#sys.stdout = Logger("/1.txt")
#print "Hello world !" # this is should be saved in yourlogfilename.txt
#------------#------------#------------#------------#------------#------------

allowedPersons=['91xxxxxxxxxx', '91xxxxxxxxxx'] #Filter the senders numbers
ap = set(allowedPersons)

name = "NAMEPRESENCE"
filelog = "/root/.yowsup/Not allowed.log"

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            self.onTextMessage(messageProtocolEntity) #Send the answer
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = messageProtocolEntity.getBody().lower()
        recipient  = messageProtocolEntity.getFrom()
	#print "recipient: ", recipient
	#print "type recipient: ", type(recipient)
        #print "message: ", message
        textmsg    = TextMessageProtocolEntity

        #For a break to use the character \n
        #The sleep you write so #time.sleep(1)

        if messageProtocolEntity.getFrom(False) in ap:
            if message == 'hi':
                answer = "Hi "+namemitt+" "
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'sends the list':
                answer = "Hi "+namemitt+"\n\nYou can ask me these things:\n\nTemperature\nRestart\nOn GPIO14\nOff GPIO14"
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'firefox':
                os.system('firefox')
                self.toLower(textmsg("Done", to = recipient ))

            else:
                answer = "Sorry "+namemitt+", I can not understand what you're asking me.."
                self.toLower(textmsg(answer, to = recipient))
                print answer

        else:
            answer = "Hi "+namemitt+", I'm sorry, I do not want to be rude, but I can not chat with you.."
            time.sleep(20)
            self.toLower(textmsg(answer, to = recipient))
            print answer
            out_file = open(filelog,"a")
            out_file.write("------------------------"+"\n"+"Sender:"+"\n"+namemitt+"\n"+"Number sender:"+"\n"+recipient+"\n"+"Message text:"+"\n"+message+"\n"+"------------------------"+"\n"+"\n")
            out_file.close()
