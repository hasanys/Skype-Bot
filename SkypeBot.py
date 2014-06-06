import Skype4Py
import time
import logging as Logging
from chatterbotapi import ChatterBotFactory, ChatterBotType
import datetime
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

    chat_coup = None
    playing_coup = False
    doing_amb_exchange = ""
    CoupGame = None
    Skype_Coup_title = "Coup 2" ## This is the title of your chat for playing Coup
    
    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()

        factory = ChatterBotFactory()

        for elem in self.skype.Chats:
            if len(elem.Members) > 3 and len(elem.Members )< 7:
                self.chat = elem
                print self.chat.Topic
                break
                
        for elem in self.skype.Chats:
            if elem.Topic.find(self.Skype_Coup_title) != -1:
            ##if elem.FriendlyName == "Yasir Hasan":
                self.chat_coup = elem
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


##        while True:
##            i = 0
##            stack_messages = ""
##
##            instance = self.chat.Messages[:10]
##            if self.chat.Topic != "Yasir is not Indian":
##                self.chat.Topic = "Yasir is not Indian"
##            for m in instance:
##                ## Check if the saved message and current messages are by the same person, sent at the same time.
##                if m.Timestamp == self.previousConvo[i][1] and m.Sender.Handle == self.previousConvo[i][2]:
##                    print "checking message2"
##                    ## Check if the message content is the same and the message has been edited
##                    if m.EditedBy != "" and m.Body != self.previousConvo[i][0]:
##                        if m.Body == "":
##                            self.stack_messages = m.Sender.FullName + " has deleted the following message at " + self.previousConvo[i][1] + ":\n" + self.previousConvo[i][0] 
##                        else:
##                            ## Check if the edited message is "similar" to the original (eg: just a typo fix...)
##                            x = [ord(c) for c in m.Body]
##                            y = [ord(c) for c in self.previousConvo[i][0]]
##
##                            if abs(sum(x) - sum(y)) < 250:
##                                continue
##                            self.stack_messages = m.EditedBy + " has edited a message from:\n\"" + self.previousConvo[i][0] + " \"\nto:\n\"" + m.Body + "\""
##                        print self.stack_messages
##                        ## Print the deleted or edited message to shell, and if edit mode enabled, send the message
##                        if self.edit_mode_enabled == True:
##                            self.chat.SendMessage(self.stack_messages)
##                i = i + 1
##                
##            
##            i = 0 ## Store the next previous 10 messages
##            for k in self.chat.Messages[:10]:
##                self.previousConvo[i][0] = k.Body
##                self.previousConvo[i][1] = datetime.datetime.fromtimestamp(k.Timestamp).strftime('%Y-%m-%d %H:%M:%S')
##                self.previousConvo[i][2] = k.Sender.Handle
##                i = i + 1
##
        time.sleep(0.2)

    def Listen(self):
        """ Forever loop I wanna be forever loop """
        while True:
            time.sleep(1)
    def CheckValidCard(self, card):

        if card not in ['Contessa', 'Assassin', 'Duke', 'Ambassador', 'Captain']:
            self.chat_coup.SendMessage('Invalid card type given')
            return False
        return True

    def DisplayStat(self, name, message):
        if name == "ALL":
            self.chat_coup.SendMessage(message)
        else:
            self.skype.SendMessage(name, message)
            
    def MessageStatus(self, Message, Status):
        """ Event handler for Skype chats """
        if Status == Skype4Py.cmsReceived and Message.Sender.Handle != "skype.edit.bot":
            Message.MarkAsSeen()
            if Message.Chat.Topic.find(self.Skype_Coup_title) != -1:
                if Message.Body.find("!") == -1:
                    return
                if Message.Body.find('!help') != -1:
                    self.DisplayStat("ALL", "\nWelcome to Coup The Game on Skype! Here are the commands you can use: \n !newgame for newgame \n !stopgame to end game \n !turn for next turn \n !losecard with card name to discard card \n!coin with a number (plus or minus) to gain or lose the coins \n !exchange with card name to exchange card with another in deck \n !ambexchange with the index of the card you want to exchange. The bot will message you your 3 card choices. In the main chat use !keep with the index of the card you want to keep \n !verify followed by the player name and the card name to check if player x has card y \nGood luck! ")
                if Message.Body.find("!newgame") != -1:
                    if len(Message.Body.split(" ")) < 2:
                        turn = Message.Sender.FullName.split(" ")[0]
                    else:
                        turn = Message.Body.split(" ")[1]
                    self.playing_coup = True
                    self.CoupGame = Coup(self.chat_coup.Members, turn)
                    self.CoupGame.display_stats()
                if self.playing_coup == True:
                    if Message.Body.find("!keep") == -1 and self.doing_amb_exchange != "":
                        self.DisplayStat("ALL", "Waiting for " + self.doing_amb_exchange + " to finish ambassador exchange")  
                        return   
                    if Message.Body.find("!stopgame") != -1:
                        self.playing_coup = False
                    elif Message.Body.find("!exchange") != -1:
                        if len(Message.Body.split(" ")) < 2:
                            self.DisplayStat("ALL", "Need to enter card name to exchange")
                            return
                        card = Message.Body.split(" ")[1]
                        if self.CheckValidCard(card):
                           self.CoupGame.exchange(Message.Sender.FullName, card)
                    elif Message.Body.find("!ambexchange") != -1:
                        if len(Message.Body.split(" ")) < 2:
                            self.DisplayStat("ALL", "Need to enter index of card to exchange")
                            return
                        if int(Message.Body.split(" ")[1]) >= 2:
                            self.DisplayStat("ALL", "Index has to be 0 or 1")
                            return
                        self.doing_amb_exchange = Message.Sender.FullName
                        self.CoupGame.amb_exchange(Message.Sender.FullName, Message.Body.split(" ")[1])
                    elif Message.Body.find("!keep") != -1:
                        if len(Message.Body.split(" ")) < 2:
                            self.DisplayStat("ALL", "Need to enter index of card to exchange")
                            return
                        self.doing_amb_exchange = ""
                        self.CoupGame.complete_amb_exchange(Message.Sender.FullName, Message.Body.split(" ")[1])
                    elif Message.Body.find("!losecard") != -1:
                        if len(Message.Body.split(" ")) < 2:
                            return
                        card = Message.Body.split(" ")[1]
                        if self.CheckValidCard(card):
                            self.CoupGame.push(Message.Sender.FullName, card, True)
                    elif Message.Body.find("!coin") != -1:
                        if len(Message.Body.split(" ")) < 2:
                            return
                        coins = Message.Body.split(" ")[1]
                        self.CoupGame.coin_transaction(Message.Sender.FullName, coins)
                    elif Message.Body.find('!turn') != -1:
                        self.CoupGame.next_turn(Message.Sender.FullName)
                    elif Message.Body.find('!verify') != -1:
                        self.CoupGame.verify_card(Message.Body.split(" ")[1], Message.Body.split(" ")[2])
                    else:
                        return
                    self.CoupGame.display_stats()
                    return
                return
            
            if len(Message.Chat.Members) == 2:
                self.ProcessMessage(Message)
            elif Message.Body.find("!edit") != -1:
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
                Message.Chat.SendMessage(self.magic_ball_responses[random.randint(0,len(self.magic_ball_responses) - 1)])
            elif Message.Body.find("!clear") != -1:
                Message.Chat.SendMessage(". \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n .")
        
            elif Message.Body.find("!switch") != -1:
                self.current_bot = (self.current_bot + 1) % 5
                self.skype.Profile('FULLNAME', self.bots[self.current_bot])
                self.restartProcess(self.current_bot)
                Message.Chat.SendMessage("Switching to a new bot..." + self.bots[self.current_bot])
##            elif Message.Body.find("!conversation") != -1:
##                if self.in_autonomous_mode == False:
##                    Message.Chat.SendMessage("Cleverbot will now be talking to Chomsky")
##                    self.in_autonomous_mode = True
##
##                    factory = ChatterBotFactory()
##                    bot = factory.create(ChatterBotType.CLEVERBOT)
##                    self.botsession = bot.create_session()
##                    
##                    factory2 = ChatterBotFactory()
##                    bot2 = factory2.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
##                    self.other_bot_session = bot2.create_session()
##
##                    self.conversation(Message, 0)
##                else:
##                    self.in_autonomous_mode = False
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

class Coup:

    deck_of_cards = []
    current_turn = "None"
    ded_cards = []
    players = {}
    first_to_full_name = {}
    
    def __init__(self, chat_members, start):
        self.deck_of_cards = ["Contessa", "Contessa", "Contessa",
                     "Assassin", "Assassin", "Assassin",
                     "Ambassador","Ambassador","Ambassador",
                     "Captain", "Captain", "Captain",
                     "Duke", "Duke", "Duke"]
        self.ded_cards = []
        self.players = {}
        self.first_to_full_name = {}
        self.shuffle()
        global current_turn
        for elem in chat_members:
            if elem.Handle != "skype.edit.bot":
                self.first_to_full_name[elem.FullName.split(" ")[0]] = elem.FullName
                self.players[elem.FullName] = {}
                self.players[elem.FullName]['cards'] = []
                self.players[elem.FullName]['coins'] = 2
                self.players[elem.FullName]['handle'] = elem.Handle
                self.deal_cards(elem.FullName)

        self.current_turn = self.first_to_full_name[start]
        if self.current_turn not in self.players.keys():
            self.current_turn = self.players.keys()[0]


    def check_player(self,player):
        return player in self.first_to_full_name.keys()

    def exchange(self, player, card):
        self.push(player, card)
        self.pop(player)

    def amb_exchange(self, player, idx):
        self.shuffle()
        str = "\n"+idx+": " + self.players[player]['cards'][int(idx)]
        str += "\n2: " + self.deck_of_cards[len(self.deck_of_cards)-2]
        str += "\n3: " + self.deck_of_cards[len(self.deck_of_cards)-1]
        _object.DisplayStat(self.players[player]['handle'], "Please reply in the main chat with (!keep) the index of these three cards you'd like to keep" + str)

    def complete_amb_exchange(self, player, idx):
        if int(idx) == 2:
            self.players[player]['cards'].append(self.deck_of_cards.pop(len(self.deck_of_cards)-2))
            self.push(player, self.players[player]['cards'][0])
        elif int(idx) == 3:
            self.players[player]['cards'].append(self.deck_of_cards.pop())
            self.push(player, self.players[player]['cards'][0])

    def pop(self, player):
        self.shuffle()
        self.players[player]['cards'].append(self.deck_of_cards.pop())

    def shuffle(self):
        random.shuffle(self.deck_of_cards)

    def push(self, player, card, ded=False):
        self.players[player]['cards'].remove(card)
        if ded:
            self.ded_cards.append(card)
        else:
            self.deck_of_cards.append(card)
         
    def coin_transaction(self, player, amount):
        self.players[player]['coins'] = int(self.players[player]['coins']) + int(amount)
        
    def display_stats(self):
        _object.DisplayStat("ALL", '\nDead cards: ' + `self.ded_cards`)
        
        for pl in self.players: 
            str = '' 
            str = str + '\nYour cards:' + `self.players[pl]['cards']` + "\n"
            str = str + 'Your coins: ' + `self.players[pl]['coins']` + "\n"
            _object.DisplayStat(self.players[pl]['handle'], str)
            _object.DisplayStat("ALL", pl + ' has ' + `self.players[pl]['coins']` + ' coins and has ' + `len(self.players[pl]['cards'])` + ' cards.')

        _object.DisplayStat("ALL", 'It is ' + self.current_turn + '\'s turn \n')

    def next_turn(self, player):
        if player != self.current_turn and player != "None":
            _object.DisplayStat("ALL", 'Only ' + self.current_turn + ' can advance the turn')
            return
        idx = self.players.keys().index(self.current_turn)+1
        if idx == len(self.players.keys()):
            self.current_turn = self.players.keys()[0]
        else:
            self.current_turn = self.players.keys()[idx]
        if len(self.players[self.current_turn]['cards']) == 0:
            next_turn(self, self.current_turn)


    def verify_card(self, player, card):
        if not self.check_player(player):
            _object.DisplayStat("ALL", 'Please enter a valid player name')
            return
        else:
            pl = self.first_to_full_name.get(player)
        if card in self.players[pl]['cards']:
            _object.DisplayStat("ALL", player + ' does have the ' + card + ' card')
        else:
            _object.DisplayStat("ALL", player + 'does NOT have the ' + card + ' card')
  
    
    def deal_cards(self, player):
        self.pop(player)
        self.pop(player)

        
_object = SkypeBot()
_object.Listen()
