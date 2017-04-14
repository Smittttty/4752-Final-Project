import pygame
from settings import *
import time
import random

class BlackjackRL:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blackjack")
        self.__cols = 10
        self.__rows = 32
        self.__width = (self.__cols + 1) * 64
        self.__height = (self.__rows + 1) * 15
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__font = pygame.font.SysFont("monospace", 12) 
        self.bet_amount = 1
        self.__init_grid()
        self.__deck = Deck()
        self.current_hand = []
        self.dealer_hand = []
       

    def __init_grid(self):
        self.__hand_states = [(0, "5", 5, 0),(1, "6", 6, 0),(2, "7", 7, 0),(3, "8", 8, 0),(4, "9", 9, 0),(5, "10", 10, 0),(6, "11", 11, 0),(7, "12", 12, 0),(8, "13", 13, 0),(9, "14", 14, 0),(10, "15", 15, 0),(11, "16", 16, 0),(12, "17", 17, 0),(13, "18+", 18, 0),(14, "Pair 2", 2, 1),(15, "Pair 3", 3, 1),(16, "Pair 4", 4, 1),(17, "Pair 5", 5, 1),(18, "Pair 6", 6, 1),(19, "Pair 7", 7, 1),(20, "Pair 8", 8, 1),(21, "Pair 9", 9, 1),(22, "Pair 10", 10, 1)]
        self.__dealer_hand_states = [i for i in range(2, 12)]
        self.__grid = [[0 for x in range(self.__cols)] for y in range(self.__rows)] 
        self.values = [[0 for x in range(self.__cols)] for y in range(self.__rows)] 
        self.__rewards = [[-self.bet_amount for x in range(self.__cols)] for y in range(self.__rows)] 
        self.__set_inital_policy()

    def __set_inital_policy(self):
        self.policy = [[[] for x in range(self.__cols)] for y in range(self.__rows)] 
        for r in range(self.__rows):
            for c in range(self.__cols):
                # for every non-terminal state, set an equiprobable policy of moving in a legal direction
                # here, 'legal' will be an array of 1s and 0s, 1 indicating that LEGAL_ACTIONS[i] is legal
                legal = [1 for action in LEGAL_ACTIONS]
                # we can sum the binary array to get the number of legal actions at this state
                num_legal = sum(legal)
                # so now the equiprobable policy is just dividing each element of the binary array by the number of actions
                state_policy = [i/num_legal for i in legal]
                # set the current policy
                self.policy[r][c] = state_policy
                # set the class policy to this initial policy we just created

    def update(self):
        for r in range(self.__rows):
            for c in range(self.__cols):
                self.__draw_strategy(self.__screen, r, c, self.__grid[r][c])
        for state in self.__hand_states:
            self.__draw_tile(self.__screen, state[0] + 1, 0, state[1], (255, 255, 255))
        for state in self.__dealer_hand_states:
            title = str(state) if state < 11 else "A"
            self.__draw_tile(self.__screen, 0, state -1, title, (255, 255, 255))
        pygame.display.flip()

    def __draw_tile(self, surface, row, col, name, color):
        surface.fill(color, (col * 64, row * 15, 64, 15))
        pygame.draw.rect(surface, (0, 0, 0), (col * 64, row * 15, 64, 15), 1)
        label = self.__font.render(name, 1, (0, 0, 0))
        font_size = self.__font.size(name)
        surface.blit(label, ((col * 64) + 32 - (font_size[0]/2), (row * 15) + 8 - (font_size[1]/2)))

    def __draw_strategy(self, surface, row, col, sType):
        row += 1
        col += 1
        surface.fill(STRATEGY_TYPE_COLOR[sType], (col * 64, row * 15, 64, 15))
        pygame.draw.rect(surface, (0, 0, 0), (col * 64, row * 15, 64, 15), 1)
        label = self.__font.render(STRATEGY_TYPE_CAPTION[sType], 1, (0, 0, 0))
        font_size = self.__font.size(STRATEGY_TYPE_CAPTION[sType])
        surface.blit(label, ((col * 64) + 32 - (font_size[0]/2), (row * 15) + 8 - (font_size[1]/2)))
    
    def __get_legal_actions(self):
        actions = [STAND]
        if(self.current_hand[1] < 21):
            actions.append(HIT)
    
    def hit(self, hand):
        hand.append(self.__deck.deal())
    
    def play_dealer(self):
        current_hand_value = self.get_hand_value(self.current_hand)
        dealer_hand = self.get_hand_value(self.dealer_hand)
        while(dealer_hand < current_hand_value):
            dealer_hand = self.get_hand_value(self.dealer_hand)
            if(dealer_hand <= 16):
                self.hit(self.dealer_hand)
            else:
                break

    def get_hand_value(self, hand):
        return sum(map(lambda c: c.get_value(), hand))

    def get_winner(self):
        current_hand_value = self.get_hand_value(self.current_hand)
        dealer_hand = self.get_hand_value(self.dealer_hand)
        if(current_hand_value > 21):
            return -self.bet_amount
        if(dealer_hand > 21 or current_hand_value > dealer_hand):
            return self.bet_amount
        if(dealer_hand > current_hand_value)
            return -self.bet_amount


    def get_rc(self):
        self.current_hand = [self.__deck.deal(), self.__deck.deal()]
        self.dealer_hand = [self.__deck.deal(), self.__deck.deal()]
        hand_value = self.get_hand_value(self.current_hand)
        row = -1
        for state in self.__hand_states:
            if(state[3] == hand_value):
                row = state[0]
                break
        if(hand_value >= 18)
            row = 13
        col = self.dealer_hand[0].get_value() - 1

        return row, col

    def update_value(self):
        i_row, i_col = self.get_rc()
        card = null
        while(true)
            row, col = self.get_rc()
            for action in self.__get_legal_actions():
                if action == HIT:
                    c = self.__deck.deal()
                    if card == null:
                        card = c
                    self.current_hand.append(c)
                if action == STAND:
                    break
        self.play_dealer()
        winner = self.get_winner()

        self.__values =  new_values
        return

    def update_policy(self):
        return

class Card:
    def __init__(self, suit, value):
        self.__suit = suit
        self.__value = value
    def get_suit(self): return self.__suit
    def get_value(self): return self.__value

class Deck:
    def __init__(self):
        self.__cards = []
        for suit in range(4):
            for v in range(13):
                card = Card(suit, v if v < 10 and v > 1 else (11 if v == 1 else 10))
                self.__cards.append(card)
        random.shuffle(self.__cards)

    def get_cards(self): return self.__cards
    def deal(self): return self.__cards.pop()

b = BlackjackRL()
b.play_dealer()
print("Current hand:")
for c in b.current_hand:
    print(c.get_value())
print("Total: " + str(b.get_hand_value(b.current_hand)))
print("\nDealer hand:")
for c in b.dealer_hand:
    print(c.get_value())
print("Total: " + str(b.get_hand_value(b.dealer_hand)))

while True:
    b.update()

