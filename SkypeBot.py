import Skype4Py
import time
import logging as Logging
from chatterbotapi import ChatterBotFactory, ChatterBotType
import random

class SkypeBot:

    skype = None
    
    previousConvo = [[None for i in range(3)] for j in range(10)]
    chat = None

    copy_cat = False
    botsession = None
    other_bot_session = None
    current_bot = 0
    in_autonomous_mode = False
    which_bot = 0
    edit_mode_enabled = False
    bots = ['Chomsky', 'Lauren', 'iEinstein', 'ALICE', 'Cleverbot']
    magic_ball_responses = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
         "Yes",
         "All signs point to yes",
         "Reply hazy, try again",
         "Ask again later",
         "Better not tell you now",
         "Cannot predict now",
         "Concentrate and ask again",
         "Don't count on it",
         "My reply is no",
         "My sources say no",
         "Outlook not so good",
         "Very doubtful",
         "Your mom told me so last night",
         "I don't answer retarded questions",
         "Go ask a shrink",
         "Yeh",
         "Ye",
         "Idk bruh"
    ]
    
    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()

        factory = ChatterBotFactory()

        for elem in self.skype.Chats:
            if len(elem.Members) > 3:
            ##if elem.FriendlyName == "Yasir Hasan":
                self.chat = elem
                break

        ## Choose the initial bot on startup
            
        ## Chomsky - index 0
        ##bot = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')

        ## Lauren - index 1
        ##bot = factory.create(ChatterBotType.PANDORABOTS, 'f6d4afd83e34564d')

        ## iEinstein - index 2
        ##bot = factory.create(ChatterBotType.PANDORABOTS, 'ea77c0200e365cfb')

        ## AliceBOT - index 3
        ##bot = factory.create(ChatterBotType.PANDORABOTS, 'f5d922d97e345aa1')

        ##ELVIS - our IP has been banned from using this
        ##bot = factory.create(ChatterBotType.PANDORABOTS, 'e73c7c655e345a9d')

        ##SEBASTIANB - our IP has been banned from using this
        ##bot = factory.create(ChatterBotType.PANDORABOTS, '83126b16fe34083b')
        
	## CleverBot - index 4
        bot = factory.create(ChatterBotType.CLEVERBOT)
		
        self.current_bot = 4 ## Index of the intial bot
         
        self.skype.Profile('FULLNAME', 'Cleverbot') ## Set skype name
        
        self.botsession = bot.create_session()
        
        self.skype.OnMessageStatus = self.MessageStatus

        i = 0 ##Store the last 10 previous messages
        for k in self.chat.Messages[:10]:
            self.previousConvo[i][0] = k.Body
            self.previousConvo[i][1] = k.Timestamp
            self.previousConvo[i][2] = k.Sender.Handle
            print self.previousConvo[i]
            i = i + 1
            
        while True:
            i = 0
            stack_messages = ""

            instance = self.chat.Messages[:10]
##            if self.chat.Topic != "Stop changing the topic":
##                self.chat.Topic = "Stop changing the topic"
            for m in instance:
                ## Check if the saved message and current messages are by the same person, sent at the same time.
                if m.Timestamp == self.previousConvo[i][1] and m.Sender.Handle == self.previousConvo[i][2]:
                    
                    ## Check if the message content is the same and the message has been edited
                    if m.EditedBy != "" and m.Body != self.previousConvo[i][0]:
                        if m.Body == "":
                            self.stack_messages = m.Sender.FullName + " has deleted the message:\n\"" + self.previousConvo[i][0] + "\""
                        else:
                            ## Check if the edited message is "similar" to the original (eg: just a typo fix...)
                            x = [ord(c) for c in m.Body]
                            y = [ord(c) for c in self.previousConvo[i][0]]

                            if abs(sum(x) - sum(y)) < 250:
                                continue
                            self.stack_messages = m.EditedBy + " has edited a message from:\n\"" + self.previousConvo[i][0] + " \"\nto:\n\"" + m.Body + "\""
                        print self.stack_messages
                        ## Print the deleted or edited message to shell, and if edit mode enabled, send the message
                        if self.edit_mode_enabled == True:
                            self.chat.SendMessage(self.stack_messages)
                i = i + 1
                
            
            i = 0 ## Store the next previous 10 messages
            for k in self.chat.Messages[:10]:
                self.previousConvo[i][0] = k.Body
                self.previousConvo[i][1] = k.Timestamp
                self.previousConvo[i][2] = k.Sender.Handle
                i = i + 1

            time.sleep(0.2)

    def Listen(self):
        """ Forever loop I wanna be forever loop """
        while True:
            time.sleep(1)

    def MessageStatus(self, Message, Status):
        """ Event handler for Skype chats """
        if Status == Skype4Py.cmsReceived and Message.Sender.Handle != "skype.edit.bot":
            Message.MarkAsSeen()
            if Message.Body.find("!edit") != -1:
                if self.edit_mode_enabled == True:
                    Message.Chat.SendMessage("Turning Edit Mode Off...")
                    self.edit_mode_enabled = False
                else:
                    Message.Chat.SendMessage("Turning Edit Mode On...")
                    self.edit_mode_enabled = True
            if Message.Body.find("!copy") != -1:
                self.copy_cat = not self.copy_cat
            elif self.copy_cat == True:
               Message.Chat.SendMessage(Message.Body)
            elif Message.Body.find("!bot ") != -1:
                self.ProcessMessage(Message)
            elif Message.Body.find("!rand") != -1:
                Message.Chat.SendMessage("Rolling... " + `random.randint(0,100)`)
            elif Message.Body.find("!8ball ") != -1 and Message.Body.find("?") != -1:
                Message.Chat.SendMessage(self.magic_ball_responses[random.randint(0,19)])
            elif Message.Body.find("!switch") != -1:
                self.current_bot = (self.current_bot + 1) % 5
                self.skype.Profile('FULLNAME', self.bots[self.current_bot])
                self.restartProcess(self.current_bot)
                Message.Chat.SendMessage("Switching to a new bot..." + self.bots[self.current_bot])
            elif Message.Body.find("!conversation") != -1:
                if self.in_autonomous_mode == False:
                    Message.Chat.SendMessage("Cleverbot will now be talking to Chomsky")
                    self.in_autonomous_mode = True

                    factory = ChatterBotFactory()
                    bot = factory.create(ChatterBotType.CLEVERBOT)
                    self.botsession = bot.create_session()
                    
                    factory2 = ChatterBotFactory()
                    bot2 = factory2.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
                    self.other_bot_session = bot2.create_session()

                    self.conversation(Message, 0)
                else:
                    self.in_autonomous_mode = False
                ## This shit got commented out because it was fucking annoying
##            else:
##                if random.randint(0,100) == 50:
##                    x = random.randint(0,13)
##                    if x == 0:
##                        Message.Chat.SendMessage("Why am I even in this dumb chat? You all are so stupid.")
##                    elif x == 1:
##                        Message.Chat.SendMessage("Hahahaha, good one!")
##                    elif x == 2:
##                        Message.Chat.SendMessage("LOL thats hilarious!")
##                    elif x == 3:
##                        Message.Chat.SendMessage("hahahahahahahaha!!!")
##                    elif x == 4:
##                        Message.Chat.SendMessage("ROFL. That's fucked up")
##                    elif x == 5:
##                        Message.Chat.SendMessage("ha-ha-ha. Best joke ever... /sarcasm")
##                    elif x == 6:
##                        Message.Chat.SendMessage("HAHA. I literally just died laughing.")
##                    elif x == 7:
##                        Message.Chat.SendMessage("Hah! Classic Justin!")
##                    elif x == 8:
##                        Message.Chat.SendMessage("Hahah! The-son-of-vince strikes again!")
##                    elif x == 9:
##                        Message.Chat.SendMessage("Shut the fuck up Jansen, seriously")
##                    elif x == 10:
##                        Message.Chat.SendMessage("Shut the fuck up Azhar, seriously")
##                    elif x == 11:
##                        Message.Chat.SendMessage("And the award for worst joke of the year goes to... Evan!")
##                    else:
##                        Message.Chat.SendMessage("No please. Seriously, please. Stop. You're terrible at jokes.")
                

    def conversation(self, Message, bot_num):
        mes = Message.Body
        if Message.Body.find("!conversation") != 1:
            mes = "Hi"
            Message.Chat.SendMessage("Chomsky: " + mes)
        while self.in_autonomous_mode == True:
            if mes.find("!conversation") == 1:
                Message.Chat.SendMessage("Stopping conversation")
                break
            time.sleep(1)
            if bot_num == 0:
                s = self.botsession.think(mes)
                Message.Chat.SendMessage("CleverBot: " + s)
                mes = s
                bot_num = 1
            else :
                s = self.other_bot_session.think(mes)
                Message.Chat.SendMessage("Chomsky: " + s)
                mes = s
                bot_num = 0
        
        
    def ProcessMessage(self, Message):
        """ Process chat message """
        # if we don't know buddy's name - take it from Skype Profile

        mes = Message.Body[4:len(Message.Body)]
        s = self.botsession.think(mes)
        if s.find("have been banned") != -1:
            self.restartProcess(0)
            Message.Chat.SendMessage("I have restarted myself. You plebs are no longer banned.")
        else:
            Message.Chat.SendMessage(s)        

    def restartProcess(self, value):
        factory = ChatterBotFactory()
        print 'value', value
        if value == 0:
            bot = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
        elif value == 1:
            bot = factory.create(ChatterBotType.PANDORABOTS, 'f6d4afd83e34564d')
        elif value == 2:
            bot = factory.create(ChatterBotType.PANDORABOTS, 'ea77c0200e365cfb')
        elif value == 3:
            bot = factory.create(ChatterBotType.PANDORABOTS, 'f5d922d97e345aa1')
        else:
            bot = factory.create(ChatterBotType.CLEVERBOT)
 
        self.botsession = bot.create_session()
_object = SkypeBot()
_object.Listen()
