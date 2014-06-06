import Skype4Py
import time
import logging as Logging
from chatterbotapi import ChatterBotFactory, ChatterBotType
import datetime
import random

class SkypeBot:
    skype = None
    botsession = None
    chat = None
    playing_coup = False
    doing_amb_exchange = ""
    CoupGame = None
    
    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()

        factory = ChatterBotFactory()
        for elem in self.skype.Chats:
            if elem.Topic.find("Coup 2") != -1:
            ##if elem.FriendlyName == "Yasir Hasan":
                self.chat = elem
                break
             
        self.skype.OnMessageStatus = self.MessageStatus

    def Listen(self):
        """ Forever loop I wanna be forever loop """
        while True:
            time.sleep(1)

    def CheckValidCard(self, card):

        if card not in ['Contessa', 'Assassin', 'Duke', 'Ambassador', 'Captain']:
            self.chat.SendMessage('Invalid card type given')
            return False
        return True

    def DisplayStat(self, name, message):
        if name == "ALL":
            self.chat.SendMessage(message)
        else:
            self.skype.SendMessage(name, message)
            
    def MessageStatus(self, Message, Status):
        """ Event handler for Skype chats """
        if Message.ChatName.find("Coup") != -1:
            return
        if Status == Skype4Py.cmsReceived and Message.Sender.Handle != "skype.edit.bot":
            Message.MarkAsSeen()
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
                self.CoupGame = Coup(self.chat.Members, turn)
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
