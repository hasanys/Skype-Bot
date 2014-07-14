import Skype4Py
import time
import logging as Logging
from chatterbotapi import ChatterBotFactory, ChatterBotType
import datetime
import random
import thread

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
    call_out_move = False
    block_move = False
    Skype_Coup_title = "Yasir Hasan" ## This is the title of your chat for playing Coup
    
    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()

        factory = ChatterBotFactory()

        for elem in self.skype.Chats:
            if len(elem.Members) > 3 and len(elem.Members )< 7:
                self.chat = elem
                print self.chat.Topic
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

        thread.start_new_thread( self.edit_bot, () )

    def edit_bot(self):
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
##            if self.chat.Topic != "Yasir is not Indian":
##                self.chat.Topic = "Yasir is not Indian"
            for m in instance:
                ## Check if the saved message and current messages are by the same person, sent at the same time.
                if m.Timestamp == self.previousConvo[i][1] and m.Sender.Handle == self.previousConvo[i][2]:
                    ## Check if the message content is the same and the message has been edited

                    if m.EditedBy != "" and m.Body != self.previousConvo[i][0]:
                        if m.Body == "":
                            self.stack_messages = m.Sender.FullName + " has deleted the following message:\n" + self.previousConvo[i][0] 
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

            time.sleep(0.1)
            
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
            show_stats = True
            if Message.Body.find("!newgame") != -1:    
                if self.playing_coup == True:
                    Message.Chat.SendMessage("Complete the other game first before the starting a new one (or end it with !stopgame command).")
                    return
                bot_playing = False
                if len(Message.Body.split(" ")) >= 2:
                    turn = Message.Body.split(" ")[1]
                    if len(Message.Body.split(" ")) == 3:
                        if Message.Body.split(" ")[2] == "1":
                            bot_playing = True
                else:
                    turn = Message.Sender.FullName.split(" ")[0]
                self.chat_coup = Message.Chat
                self.playing_coup = True
                self.CoupGame = Coup(self.chat_coup.Members, turn, bot_playing)
                self.CoupGame.display_stats()
                return
            if self.chat_coup != None and Message.Chat.Topic == self.chat_coup.Topic:
                if Message.Body.find("!") == -1:
                    return
                if Message.Body.find('!help') != -1:
                    self.DisplayStat("ALL", "\nWelcome to Coup The Game on Skype! Here are the commands you can use: \n !newgame for newgame \n !stopgame to end game \n !turn for next turn \n !losecard with card name to discard card \n!coin with a number (plus or minus) to gain or lose the coins \n !exchange with card name to exchange card with another in deck \n !ambexchange with the index of the card you want to exchange. The bot will message you your 3 card choices. In the main chat use !keep with the index of the card you want to keep \n !verify followed by the player name and the card name to check if player x has card y \nGood luck! ")
                
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
                           _object.CoupGame.exchange(Message.Sender.FullName, card)
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
                        if self.CoupGame.bot_playing and self.CoupGame.current_turn == "Cleverbot":
                            show_stats = False
                            Message.Chat.SendMessage("It is my turn...")
                            thread.start_new_thread( self.CoupGame.ai_session.take_turn, () )
                    elif Message.Body.find('!verify') != -1:
                        self.CoupGame.verify_card(Message.Body.split(" ")[1], Message.Body.split(" ")[2])

                    elif Message.Body.find('!tax') != -1:
                        if self.CoupGame.bot_playing:
                            show_stats = False
                            self.CoupGame.ai_session.player_taxes(Message.Sender.FullName.split(" ")[0])
                            
                    elif Message.Body.find('!foreignaid') != -1:
                        if self.CoupGame.bot_playing:
                            show_stats = False
                            thread.start_new_thread( self.CoupGame.ai_session.player_foreign_aids, (Message.Sender.FullName.split(" ")[0],) )
                            
                    elif Message.Body.find('!steal') != -1:
                        if self.CoupGame.bot_playing:
                            if len(Message.Body.split(" ")) == 2 and Message.Body.split(" ")[1] == "bot":
                                show_stats = False
                                thread.start_new_thread( self.CoupGame.ai_session.player_steals, (Message.Sender.FullName.split(" ")[0],) )

                    elif Message.Body.find('!assassinate') != -1:
                        if self.CoupGame.bot_playing:
                            if len(Message.Body.split(" ")) == 2 and Message.Body.split(" ")[1] == "bot":
                                show_stats = False
                                thread.start_new_thread( self.CoupGame.ai_session.player_assassinates, (Message.Sender.FullName.split(" ")[0],) )

                    elif Message.Body.find('!coup') != -1:
                        if self.CoupGame.bot_playing:
                            if len(Message.Body.split(" ")) == 2 and Message.Body.split(" ")[1] == "bot":
                                show_stats = False
                                self.CoupGame.ai_session.player_coups()

                    elif Message.Body.find('!block') != -1:
                        if self.CoupGame.bot_playing:
                            if len( Message.Body.split(" ")) == 2 and Message.Body.split(" ")[1] == "bot":
                                show_stats = False
                                self.block_move = False

                    elif Message.Body.find('!call') != -1:
                        if self.CoupGame.bot_playing:
                            if len( Message.Body.split(" ")) == 2 and Message.Body.split(" ")[1] == "bot":
                                show_stats = False
                                self.call_out_move = False
                            
                    else:
                        return
                    if show_stats == True:
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
##            elif Message.Body.find("!countdown") != -1:
##                if len (Message.Body.split(" ")) > 1:
##                    
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
    bot_playing = False
    ai_session = None

    def __init__(self, chat_members, start, bot_game):
        self.deck_of_cards = ["Contessa", "Contessa", "Contessa",
                     "Assassin", "Assassin", "Assassin",
                     "Ambassador","Ambassador","Ambassador",
                     "Captain", "Captain", "Captain",
                     "Duke", "Duke", "Duke"]
        self.ded_cards = []
        self.players = {}
        self.first_to_full_name = {}
        self.bot_playing = bot_game
        self.shuffle()

        global current_turn
        for elem in chat_members:
            if elem.Handle == "skype.edit.bot" and bot_game == False:
                continue
            self.first_to_full_name[elem.FullName.split(" ")[0]] = elem.FullName
            self.players[elem.FullName] = {}
            self.players[elem.FullName]['cards'] = []
            self.players[elem.FullName]['coins'] = 2
            self.players[elem.FullName]['handle'] = elem.Handle
            self.deal_cards(elem.FullName)

        if bot_game:
            self.ai_session = ArtificialIntelligence(len(self.players))
        
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
            if self.players[pl]['handle'] == "skype.edit.bot" and self.bot_playing == True:
                self.ai_session.set_cards(self.players[pl]['cards'])
                self.ai_session._my_coins = self.players[pl]['coins']
            else:
                _object.DisplayStat(self.players[pl]['handle'], str)
            if self.bot_playing == True:
                self.ai_session.set_other_players_stats(pl, self.players[pl]['coins'], len(self.players[pl]['cards']))
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
        if self.bot_playing == True:
            self.ai_session._current_turn = self.current_turn
        if len(self.players[self.current_turn]['cards']) == 0:
            self.next_turn(self.current_turn)


    def verify_card(self, player, card):
        if not self.check_player(player):
            _object.DisplayStat("ALL", 'Please enter a valid player name')
            return
        else:
            pl = self.first_to_full_name.get(player)
        if card in self.players[pl]['cards']:
            _object.DisplayStat("ALL", player + ' does have the ' + card + ' card')
            return True
        else:
            _object.DisplayStat("ALL", player + ' does NOT have the ' + card + ' card')
            return False
    
    def deal_cards(self, player):
        self.pop(player)
        self.pop(player)

class ArtificialIntelligence:
    

    ## The state I am in, dictates my call-outs, bluffs, and all my moves.
    ## Moving between states is a rather diffcult and more or less random
    ## decision based on the game's standing, at least from what I know.
    _states = ["Start", "Aggressive", "Late", "Coup"]
    _state = 0

    ## These are my cards and coins. They are updated from Coup Bot automatically.
    _my_cards = []
    _my_coins = 0

    ## This is the info I have about other players and the game in general.
    ## The number of players, the number of coins and cards other players have,
    ## and the current turn. I use these in weighing my decisions and moves too.
    _num_players = 0
    _stats = {}
    _current_turn = ""

    ## In a future version, this will be my set of predictions for other players
    ## based on what I have seen in the game. They may or may not be right, but I
    ## will create these during the game, and will use these as a base for decisions.
    _predictions = {}
    _dead_cards = []
    _turns = 0
    
    def __init__(self, players ):
        self._my_coins = 2
        self._state = 0
        self._num_players = players

    def set_cards(self, cards):
        self._my_cards = cards

    def set_other_players_stats(self, player, coins, num_cards):
        self._stats[player] = {}
        self._stats[player]['coins'] = coins
        self._stats[player]['cards'] = num_cards

    def take_turn(self):
        import random
        self._turns = self._turns + 1
        if len(self._my_cards) == 2:
            cardA = self._my_cards[0]
            cardB = self._my_cards[1]
        elif len(self._my_cards) == 1:
            cardA = self._my_cards[0]
            cardB = ""
        else:
            cardA = ""
            cardB = ""
            
        if self._state == 0:
            if cardA == "Duke" or cardB == "Duke":
                self.make_move("Tax")
            elif cardA == "Ambassador" and cardB == "Ambassador" :
                self.make_move("Exchange")
            elif cardA == "Contessa" and cardB == "Contessa" :
                self.make_move("Exchange")
            else:
                x = random.randint(0,100)
                coins = 0
                for i in self._stats:
                    if self._stats[i]['coins'] == 5:
                        coins = coins + 1
                if coins > len(self._stats)/2:
                    self.make_move("Tax")
                else:
                    if x > 75:
                        self.make_move("Income")
                    else:
                        self.make_move("Tax")
            self.change_state()
        elif self._state == 1:
            if cardA == "Assassin" or cardB == "Assassin":
                if self._my_coins > 2:
                    self.make_move("Assassinate")
                else:
                    self.make_move("Tax")
            elif self._my_coins > 6:
                self.make_move("Coup")
            elif cardA == "Captain" or cardB == "Captain":
                self.make_move("Steal")
            else:
                #Gotta bluff assassinating or stealing
                random = random.randint(0,100)
                if random < 50:
                    self.make_move("Assassinate")
                else:
                    self.make_move("Steal")
            self.change_state()
        elif self._state == 2:
            if self._my_coins < 7:
                if cardA == "Duke" or cardB == "Duke":
                    self.make_move("Tax")
                elif cardA == "Captain" or cardB == "Captain":
                    self.make_move("Steal")
                elif cardA == "Assassin" or cardB == "Assassin":
                    self.make_move("Assassin")
                else:
                    self.make_move("Income")
            else:
                self.make_move("Coup")
        elif self._state == 3:
            self.make_move("Coup")
            self.change_state()
        else: ##Shouldn't get here
            print "Shouldn't get here" + str(self._state)
            self.make_move("Income") 
        _object.DisplayStat("ALL", '!turn')
        _object.CoupGame.next_turn("Cleverbot")

    def change_state(self):
        import random
        if self._my_coins > 10:
            self._state = 3 ## Need to Coup someone
            return
        cards = 0
        for i in self._stats:
            cards = cards + self._stats[i]['cards']
        cards = cards / len(self._stats)
        if cards < 1.3:
            self._state = 2
        elif self._my_coins > 7 or self._turns > 3:
            self._state = 1
        else:
            self._state = 1

    def player_taxes(self, player):
        if len(self._my_cards) == 2:
            cardA = self._my_cards[0]
            cardB = self._my_cards[1]
        elif len(self._my_cards) == 1:
            cardA = self._my_cards[0]
            cardB = ""
        else:
            cardA = ""
            cardB = ""        
        x = random.randint(0,100)
        if cardA == "Duke" and cardB == "Duke" or (self._turns > 7 and x > 75) or (self._turns == 1 and x < 6):
            _object.DisplayStat("ALL", 'I am going to call you out on not having a Duke! !verify ' + player + ' Duke')
            if _object.CoupGame.verify_card("Cleverbot", "Duke"): ## They had a Duke, I lose a card
                _object.DisplayStat("ALL", 'You did have a Duke. I lose a card... !losecard ' + self.lose_card())
                _object.CoupGame.push("Cleverbot", self.lose_card(), True)
            else:
                _object.DisplayStat("ALL", 'You did not have a Duke, ' + player + '! Please lose a card (and return the 3 coins from taxing).')
        else:
            _object.DisplayStat("ALL", 'Okay, go ahead...') 

    def player_foreign_aids(self, player):
        if len(self._my_cards) == 2:
            cardA = self._my_cards[0]
            cardB = self._my_cards[1]
        elif len(self._my_cards) == 1:
            cardA = self._my_cards[0]
            cardB = ""
        else:
            cardA = ""
            cardB = ""
            
        if cardA == "Duke" or cardB == "Duke":
            _object.DisplayStat("ALL", 'I am going to block with my Duke. You have 10 seconds to call me out (with !call bot)...')
            _object.call_out_move = True
            time.sleep(10)

            if _object.call_out_move == True:
                _object.DisplayStat("ALL", 'No call out')
            else:
                _object.DisplayStat("ALL", 'I DO have a Duke... Please lose a card !verify Clever bot Duke')
                _object.CoupGame.verify_card("Cleverbot", "Duke")
                _object.DisplayStat("ALL", 'Exchanging Card... !exchange Duke')
                _object.CoupGame.exchange("Cleverbot", "Duke")
            _object.call_out_move = False
        else:
            _object.DisplayStat("ALL", 'Go ahead ...')    
    
    def player_steals(self, player):
        if len(self._my_cards) == 2:
            cardA = self._my_cards[0]
            cardB = self._my_cards[1]
        elif len(self._my_cards) == 1:
            cardA = self._my_cards[0]
            cardB = ""
        else:
            cardA = ""
            cardB = ""
            
        if cardA == "Captain" or cardB == "Captain":
            _object.DisplayStat("ALL", 'I am going to block with my Captain. You have 10 seconds to call me out (with !call bot)...')
            _object.call_out_move = True
            time.sleep(10)

            if _object.call_out_move == True:
                _object.DisplayStat("ALL", 'No call out. I block the steal with my Captain')
            else:
                _object.DisplayStat("ALL", 'I DO have a Captain... Please lose a card !verify Clever bot Captain')
                _object.CoupGame.verify_card("Cleverbot", "Captain")
                _object.DisplayStat("ALL", 'Exchanging Card... !exchange Captain')
                _object.CoupGame.exchange("Cleverbot", "Captain")
        elif cardA == "Ambassador" or cardB == "Ambassador":
            _object.DisplayStat("ALL", 'I am going to block with my Ambassador. You have 10 seconds to call me out (with !call bot)...')
            _object.call_out_move = True
            time.sleep(10)

            if _object.call_out_move == True:
                _object.DisplayStat("ALL", 'No call out. I block the steal with my Ambassador')
            else:
                _object.DisplayStat("ALL", 'I DO have an Ambassador... Please lose a card !verify Clever bot Ambassador')
                _object.CoupGame.verify_card("Cleverbot", "Ambassador")
                _object.DisplayStat("ALL", 'Exchanging Card... !exchange Ambassador')
                _object.CoupGame.exchange("Cleverbot", "Ambassador")                
                _object.call_out_move = False
        elif self._turns < 5 or (len(self._my_cards) == 2 and random.randint(0,100) > 50):
            _object.DisplayStat("ALL", 'I am going to block with my Ambassador. You have 10 seconds to call me out (with !call bot)...')
            _object.call_out_move = True
            time.sleep(10)

            if _object.call_out_move == True:
                _object.DisplayStat("ALL", 'No call out. I block the steal with my Ambassador')
            else:
                _object.DisplayStat("ALL", 'I DONT have an Ambassador... !verify Clever bot Ambassador')
                _object.CoupGame.verify_card("Cleverbot", "Ambassador")
                _object.DisplayStat("ALL", 'I lose a card... !losecard ' + self.lose_card())
                _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                _object.call_out_move = False
        else:
            _object.DisplayStat("ALL", 'Go ahead, I lose two coins, you gain two... !coin -2')  
            _object.CoupGame.coin_transaction("Cleverbot", -2)

    def player_assassinates(self, player):
        import random
        if len(self._my_cards) == 2:
            cardA = self._my_cards[0]
            cardB = self._my_cards[1]
        elif len(self._my_cards) == 1:
            cardA = self._my_cards[0]
            cardB = ""
        else:
            cardA = ""
            cardB = ""        
        if cardA == "Contessa" or cardB == "Contessa":
            _object.DisplayStat("ALL", 'I am going to block with my Contessa. You have 10 seconds to call me out (with !call bot)...')
            _object.call_out_move = True
            time.sleep(10)

            if _object.call_out_move == True:
                _object.DisplayStat("ALL", 'No call out. I block with my Contessa. Lose 3 coins.')
            else:
                _object.DisplayStat("ALL", 'I DO have a Contessa... Please lose a card and 3 coins !verify Clever Contessa')
                _object.CoupGame.verify_card("Cleverbot", "Contessa")
                _object.DisplayStat("ALL", 'Exchanging Card... !exchange Contessa')
                _object.CoupGame.exchange("Cleverbot", "Contessa")                
                _object.call_out_move = False
        else:
            random = random.randint(0,100)
            if len(self._my_cards) == 1: ## Need to block/call out or I lose
                if random > 50:
                    ##call out
                    _object.DisplayStat("ALL", 'I am calling you out on not having an Assassin... !verify ' + player + ' Assassin')
                    if _object.CoupGame.verify_card(player, "Assassin") == True:
                        _object.CoupGame.verify_card("Cleverbot", "Ambassador")
                        _object.DisplayStat("ALL", 'You do have an Assassin. I lose a card ...  !losecard ' + self.lose_card())
                        _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                    else:
                        _object.DisplayStat("ALL", 'You did not have an Assassin. Please lose a card and 3 coins ...')                        
                else: ##block
                    _object.DisplayStat("ALL", 'I am going to block with my Contessa. You have 10 seconds to call me out (with !call bot)...')
                    _object.call_out_move = True
                    time.sleep(10)
                    if _object.call_out_move == True:
                        _object.DisplayStat("ALL", 'I block with my contessa. Please lose 3 coins')
                    else:
                        _object.DisplayStat("ALL", 'I DONT have a Contessa... I lose the game! !verify Clever Contessa')
                        _object.CoupGame.verify_card("Cleverbot", "Contessa")
                        _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                        _object.call_out_move = False
            else:
                if "Contessa" not in _object.Coupgame.ded_cards:
                    if random < 35:
                        ##block
                        _object.DisplayStat("ALL", 'I am going to block with my Contessa. You have 10 seconds to call me out (with !call bot)...')
                        _object.call_out_move = True
                        time.sleep(10)
                        
                        if _object.call_out_move == True:
                            _object.DisplayStat("ALL", 'I block with my contessa. Please lose 3 coins')
                        else:
                            _object.DisplayStat("ALL", 'I DONT have a Contessa... I lose 2 cards and lose the game! !verify Clever Contessa')
                            _object.CoupGame.verify_card("Cleverbot", "Contessa")
                            _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                            _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                            _object.call_out_move = True
                else:
                    if random > 80:
                        ##call out
                        _object.DisplayStat("ALL", 'I am calling you out on not having an Assassin... !verify ' + player + ' Assassin')
                        if _object.CoupGame.verify_card(player, "Assassin") == True:
                            _object.CoupGame.verify_card("Cleverbot", "Ambassador")
                            _object.DisplayStat("ALL", 'You do have an Assassin. I lose a card ...  !losecard ' + self.lose_card())
                            _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                        else:
                            _object.DisplayStat("ALL", 'You did not have an Assassin. Please lose a card and 3 coins ...')                        
                    else:
                            _object.DisplayStat("ALL", 'Okay go ahead, I lose a card ... !losecard ' + self.lose_card())                        
                            _object.CoupGame.push("Cleverbot", self.lose_card(), True)                
                

    def player_coups(self):
        _object.DisplayStat("ALL", 'I have been couped! I lose a card... !losecard ' + self.lose_card())
        _object.CoupGame.push("Cleverbot", self.lose_card(), True)

    def make_move(self, move):
        import random
        if len(self._my_cards) == 2:
            cardA = self._my_cards[0]
            cardB = self._my_cards[1]
        elif len(self._my_cards) == 1:
            cardA = self._my_cards[0]
            cardB = ""
            
        if move == "Tax":
            _object.DisplayStat("ALL", 'I am going to tax... You have 10 seconds to make a counter-action (!call bot)...')
            _object.call_out_move = True

            time.sleep(10)
            
            if _object.call_out_move == True: ##Nobody called me out :)
                _object.DisplayStat("ALL", 'Taxing... !coin 3')
                _object.CoupGame.coin_transaction("Cleverbot", 3)
            else: ## Someone called me out on not having a Duke :(
                if cardA == "Duke" or cardB == "Duke": ## I DID have a duke! :)
                    _object.DisplayStat("ALL", 'I DO have a Duke... You lose a card !verify Cleverbot Duke')
                    _object.CoupGame.verify_card("Cleverbot", "Duke")
                    _object.DisplayStat("ALL", 'Exchanging Card... !exchange Duke')
                    _object.CoupGame.exchange("Cleverbot", "Duke")                      
                else: ## I didn't have a Duke :(
                    _object.DisplayStat("ALL", 'I DONT have a Duke... !verify Cleverbot Duke')
                    _object.CoupGame.verify_card("Cleverbot", "Duke")
                    _object.DisplayStat("ALL", '!losecard ' + self.lose_card())
                    _object.CoupGame.push("Cleverbot", self.lose_card(), True)
            _object.call_out_move = True
            _object.CoupGame.display_stats()
        elif move == "Income":
            _object.DisplayStat("ALL", 'I am going to income...')
            _object.DisplayStat("ALL", 'Income... !coin 1')
            _object.CoupGame.coin_transaction("Cleverbot", 1)
            _object.CoupGame.display_stats()
        elif move == "Foreign Aid":
            _object.DisplayStat("ALL", 'I am going to foreign aid... You have 10 seconds to make a counter-action (!block bot or !call bot)...')
            _object.block_move = True
            time.sleep(10)

            if _object.block_move == True: ##Nobody blocked me :)
                _object.DisplayStat("ALL", 'Foreign Aid... !coin 2')
                _object.CoupGame.coin_transaction("Cleverbot", 2)
            else: # I was blocked...
                _object.DisplayStat("ALL", 'Okay I will take the block...')
                ## Here, I'll want to store who blocks me into prediction list
                ## So I don't make the same move again and look stupid.
            _object.block_move = False
            _object.CoupGame.display_stats()
        elif move == "Assassinate":
            # Figure out who to assassinate...
            target = ""
            cards = 0
            for key,value in self._stats.iteritems():
                if key == "Cleverbot":
                    continue
                cards = cards + self._stats[key]['cards']
                if cards == 2:
                    target = key
                    break
            if target == "":
                for i in self._stats:
                    if i == "Cleverbot":
                        continue
                    if self._stats[i]['cards'] > 0:
                        target = i
                    break
            _object.DisplayStat("ALL", 'I will assassinate ' + target + '... !coin -3 You have 10 seconds to make a counter-action (!block bot or !call bot)... \n !assassinate ' + target )
            _object.call_out_move = True
            _object.block_move = True
            time.sleep(10)

            _object.CoupGame.coin_transaction("Cleverbot", -3)

            if _object.call_out_move == False: ## I was called out for not having an assasssin
                if cardA == "Assassin" or cardB == "Assassin": ## I DID have a Assassin! :)
                    _object.DisplayStat("ALL", 'I DO have an Assassin... You lose a card, and I assassinate you so lose another card ... !verify Clever Assassin')
                    _object.CoupGame.verify_card("Cleverbot", "Assassin")
                    _object.DisplayStat("ALL", 'Exchanging Card... !exchange Assassin')
                    _object.CoupGame.exchange("Cleverbot", "Assassin")                      
                else: ## I didn't have a Assassin :(
                    _object.DisplayStat("ALL", 'I DONT have an Assassin... I lose a card ... !verify Clever Assassin')
                    _object.CoupGame.verify_card("Cleverbot", "Assassin")
                    _object.DisplayStat("ALL", '!losecard ' + self.lose_card())
                    _object.CoupGame.push("Cleverbot", self.lose_card(), True)
            elif _object.block_move == False: ## I was blocked with a Contessa
                import random
                random = random.randint(0,100)
                call_out = False
                if self._stats[target]['cards'] == 1:
                    if random < 60:
                        call_out = True
                else:
                    if random < 20:
                        call_out = True
                if call_out == True:
                    _object.DisplayStat("ALL", 'I am calling you out on not having a Contessa ... !verify ' + target.split(" ")[0] + ' Contessa')
                    if _object.CoupGame.verify_card(target.split(" ")[0], "Contessa") == True:
                        _object.DisplayStat("ALL", 'I lose a card... !losecard ' + self.lose_card())
                    else:
                        _object.DisplayStat("ALL", 'I assassinated you AND you lose a card for not having a Contessa, so you lose 2 cards')
                else:
                    _object.DisplayStat("ALL", 'Okay I accept the block...')
            else: ## No one called out or blocked me.
                _object.DisplayStat("ALL", 'No call or block ... I assassinated you, ' + target + ' so please lose a card...')
            _object.CoupGame.display_stats()
        elif move == "Coup":
            target = ""
            cards = 0
            for key,value in self._stats.iteritems():
                if key == "Cleverbot":
                    continue
                cards = cards + self._stats[key]['cards']
                if cards == 1:
                    target = key
                    break
            if target == "":
                for i in self._stats:
                    if i == "Cleverbot":
                        continue
                    target = i
                    break
            _object.DisplayStat("ALL", 'I will Coup ' + target + 'Please lose a card now ... !coup ' + target )
        elif move == "Steal":
            # Figure out who to steal from...
            target = ""
            coins = 15
            for key,value in self._stats.iteritems():
                if self._stats[key]['coins'] <= coins: 
                    coins = coins + self._stats[key]['coins']
                    target = key
            _object.DisplayStat("ALL", 'I steal from ' + target + '. You have 10 seconds to make a counter-action (!block bot or !call bot)... \n !steal ' + target)
            _object.call_out_move = True
            _object.block_move = True
            time.sleep(10)

            if _object.call_out_move == False: ## I was called out for not having a Captain
                if cardA == "Captain" or cardB == "Captain": ## I DID have a Captain! :)
                    _object.DisplayStat("ALL", 'I DO have a Captain... You lose a card ... !verify Clever Captain')
                    _object.CoupGame.verify_card("Cleverbot", "Captain")
                    _object.DisplayStat("ALL", 'Exchanging Card... !exchange Captain')
                    _object.DisplayStat("ALL", 'Stealing 2 coins from ' + target + '. Please lose 2 coins. !coin 2')
                    _object.CoupGame.coin_transaction("Cleverbot", 2)
                    _object.CoupGame.exchange("Cleverbot", "Captain")                      
                else: ## I didn't have a Captain :(
                    _object.DisplayStat("ALL", 'I DONT have a Captain... I lose a card ... !verify Clever Captain')
                    _object.CoupGame.verify_card("Cleverbot", "Captain")
                    _object.DisplayStat("ALL", '!losecard ' + self.lose_card())
                    _object.CoupGame.push("Cleverbot", self.lose_card(), True)
            elif _object.block_move == False: ## I was blocked with an Ambassador or Captain
                random = random.randint(0,100)
                call_out = False
                if self._stats[target]['cards'] == 1:
                    if random < 20 or (cardA == "Captain" and cardB == "Captain") or (cardA == "Ambassador" and cardB == "Ambassador"):
                        call_out = True
                    elif self._state == 3:
                        if random < 50:
                            call_out = True
                else:
                    if random < 15:
                        call_out = True
                if call_out == True:
                    _object.DisplayStat("ALL", 'I am calling you out on not having a... blocker.. person? !verify ' + target.split(" ")[0] + ' Blocker')
                    if _object.CoupGame.verify_card(target.split(" ")[0], "Ambassador") == True or _object.CoupGame.verify_card(target.split(" ")[0], "Captain") == True :
                        _object.DisplayStat("ALL", 'I lose a card, you did have a blocker... !losecard ' + self.lose_card())
                        _object.CoupGame.push("Cleverbot", self.lose_card(), True)
                    else:
                        _object.DisplayStat("ALL", 'You did not have a blocker. And I stole two from you, please lose 2 coins and 1 card')
                        _object.DisplayStat("ALL", '!coin 2')
                        _object.CoupGame.coin_transaction("Cleverbot", 2)
                else:
                    _object.DisplayStat("ALL", 'Okay I accept the block...')
            else: ## I wasn't called out!
                _object.DisplayStat("ALL", 'Stealing 2 coins from ' + target + '. Please lose 2 coins. !coin 2')
                _object.CoupGame.coin_transaction("Cleverbot", 2)
            _object.CoupGame.display_stats()
        elif move == "Exchange":
            ## Not yet implemented fully (Need to rework how exchanges work anyway)
            _object.DisplayStat("ALL", 'I am going to Exchange... You have 10 seconds to make a counter-action (!call bot)...')
            _object.call_out_move = True

            time.sleep(10)

            if _object.call_out_move == True: ##Nobody called me out :)
                _object.DisplayStat("ALL", 'Exchanging... !ambexchange 3')
                if cardA == "Contessa":
                    _object.CoupGame.exchange("Cleverbot", "Contessa")
                elif cardA == "Ambassador":
                    _object.CoupGame.exchange("Cleverbot", "Ambassador")
            else: ## Someone called me out on not having an Ambassador :(
                if cardA == "Ambassador" or cardB == "Ambassador": ## I DID have an Ambassador! :)
                    _object.DisplayStat("ALL", 'I DO have an Ambassador... You lose a card !verify Cleverbot Ambassador')
                    _object.CoupGame.verify_card("Cleverbot", "Ambassador")
                    _object.DisplayStat("ALL", 'Exchanging Card... !exchange Ambassador')
                    _object.CoupGame.exchange("Cleverbot", "Ambassador")
                    _object.CoupGame.exchange("Cleverbot", "Ambassador")
                else: ## I didn't have an Ambassador :(
                    _object.DisplayStat("ALL", 'I DONT have an Ambassador... !verify Cleverbot Ambassador')
                    _object.CoupGame.verify_card("Cleverbot", "Ambassador")
                    _object.DisplayStat("ALL", '!losecard ' + self.lose_card())
                    _object.CoupGame.push("Cleverbot", self.lose_card(), True)
            _object.call_out_move = True
            _object.CoupGame.display_stats()
            return

    ## I need to lose a card, so pick which one to lose                                    
    def lose_card(self):
        import random
        if len(self._my_cards) == 1: ## I lost the game!
            _object.DisplayStat("ALL", 'I am out of the game. Good game!')
            return self._my_cards[0]
        else:
            if len(self._my_cards) == 2:
                cardA = self._my_cards[0]
                cardB = self._my_cards[1]
            elif len(self._my_cards) == 1:
                cardA = self._my_cards[0]
                cardB = ""
            else:
                cardA = ""
                cardB = ""
                
            if self._turns < 5: ##Early game
                if cardA == "Duke":
                    return cardB
                if cardB == "Duke":
                    return cardA
            if cardA == "Contessa":
                return cardA
            if cardB == "Contessa":
                return cardB
            if cardA == "Ambassador":
                return cardA
            if cardB == "Ambassador":
                return cardB
            ## Late game
            random = random.randint(0,100)
            if random > 50:
                return cardA
            else:
                return cardB


    
_object = SkypeBot()
_object.Listen()
