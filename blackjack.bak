import pygame
from settings import *
import time
import random

class BlackjackRL:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blackjack")
        pygame.key.set_repeat(500, 100)
        self.__cols = 10
        self.__rows = 32
        self.__width = (self.__cols + 1) * 64
        self.__height = (self.__rows + 1) * 15
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__font = pygame.font.SysFont("monospace", 12) 
        self.bet_amount = 10.0
        self.__init_grid()
        self.__deck = Deck()
        self.current_hand = []
        self.dealer_hand = []
       

    def __init_grid(self):
        self.__hand_states = [(0, "5", 5, 0),(1, "6", 6, 0),(2, "7", 7, 0),(3, "8", 8, 0),(4, "9", 9, 0),(5, "10", 10, 0),(6, "11", 11, 0),(7, "12", 12, 0),(8, "13", 13, 0),(9, "14", 14, 0),(10, "15", 15, 0),(11, "16", 16, 0),(12, "17", 17, 0),(13, "18+", 18, 0),(14, "Pair 2", 2, 1),(15, "Pair 3", 3, 1),(16, "Pair 4", 4, 1),(17, "Pair 5", 5, 1),(18, "Pair 6", 6, 1),(19, "Pair 7", 7, 1),(20, "Pair 8", 8, 1),(21, "Pair 9", 9, 1),(22, "Pair 10", 10, 1)]
        self.__dealer_hand_states = [i for i in range(2, 12)]
        self.__grid = [[0 for x in range(self.__cols)] for y in range(self.__rows)] 
        self.values = [[0 for x in range(self.__cols)] for y in range(self.__rows)] 
        self.rewards = [[-self.bet_amount for x in range(self.__cols)] for y in range(self.__rows)] 
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
        self.__events()
        for r in range(self.__rows):
            for c in range(self.__cols):
                self.__draw_strategy(self.__screen, r, c, 0 if self.policy[r][c][0] == 1 else 1)
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
    
    def is_legal_action(self, action):
        if(action == DOUBLE or action == SPLIT):
            return False
        if(action == STAND):
            return True
        return self.get_hand_value(self.current_hand) < 21

    def get_value(self, r, c):      return self.values[r][c]
    def get_reward(self, r, c):     return self.rewards[r][c]
    def get_policy(self, r, c):     return self.policy[r][c] 

    def hit(self, hand):
        hand.append(self.__deck.deal())
    
    def play_dealer(self, current_hand, dealer_card):
        while(dealer_card <= current_hand):
            dealer_card += self.__deck.deal().get_value()

        return 0 if dealer_card > 21 else (1 if dealer_card > current_hand else 2)

    def get_hand_value(self, hand):
        return sum(map(lambda c: c.get_value(), hand))

    def get_winner(self):
        current_hand_value = self.get_hand_value(self.current_hand)
        dealer_hand = self.get_hand_value(self.dealer_hand)
        if(current_hand_value > 21):
            return -self.bet_amount
        if(dealer_hand > 21 or current_hand_value > dealer_hand):
            return self.bet_amount
        if(dealer_hand > current_hand_value):
            return -self.bet_amount


    def get_rc(self, hand_value, dealer_card):
        row = -1
        for state in self.__hand_states:
            if(state[2] == hand_value):
                row = state[0]
                break
        if(hand_value >= 18):
            row = 13
        col = dealer_card - 2
        return row, col

    def get_card_prob(self, value):
        if (value < 10 or value > 10):
            return 4.0/52.0
        else:
            return 16.0/52.0

    def get_dealer_probs(self, hand_value, first_card):
        busts = 0
        wins = 0
        draws = 0
        for i in range(100):
            result = self.play_dealer(hand_value, first_card)
            if result == 0:
                busts += 1
            elif result == 1:
                wins += 1
            else:
                draw += 1
        return (busts/100.0 * self.bet_amount) - (wins/100.0 * self.bet_amount)

    def update_value(self):
        self.current_hand = [self.__deck.deal(), self.__deck.deal()]
        self.dealer_hand = [self.__deck.deal()]
        hand_value = self.get_hand_value(self.current_hand)
        dealer_card_value = self.dealer_hand[0].get_value()
        #print("hand val: " + str(hand_value))
        #print("dealer val: " + str(dealer_card_value))

        row, col = self.get_rc(hand_value, self.dealer_hand[0].get_value())
        #print("updating: " + str((row, col)))
        new_values = [[0]*self.__cols for i in range(self.__rows)]
        for i in range(len(LEGAL_ACTIONS)):
            if not self.is_legal_action(LEGAL_ACTIONS[i]):
                continue
            if LEGAL_ACTIONS[i] == HIT:
                ## first part
                ## second part
                second_sum = 0
                for v in range(13):
                    c = Card(0, v if v < 10 and v > 1 else (11 if v == 1 else 10))
                    prob = self.get_card_prob(c.get_value())
                    new_hand_value = hand_value + c.get_value()
                    r, c = self.get_rc(new_hand_value, dealer_card_value)
                    reward = -self.bet_amount
                    if(new_hand_value <= 21):
                        reward = self.get_reward(r, c)
                    value = -self.bet_amount
                    if(new_hand_value <= 21):
                        value = self.get_value(r, c)
                    second_sum += prob * (reward + (GAMMA * value))

                    next_state_value =  value
                    probability      =  self.policy[row][col][i]
                    reward           =  self.get_reward(row, col)
                    new_values[row][col] += probability * (reward + GAMMA * next_state_value)
                new_values[row][col] *= second_sum

            if LEGAL_ACTIONS[i] == STAND:
                new_values[row][col] += self.get_dealer_probs(hand_value, dealer_card_value)

        self.values = new_values

    def update_policy(self):
        value = 0
        hand_value = self.get_hand_value(self.current_hand)
        dealer_card_value = self.dealer_hand[0].get_value()
        row, col = self.get_rc(hand_value, dealer_card_value)
        stand_value = self.get_value(row, col)
        policy = []
        for v in range(13):
            card = Card(0, v if v < 10 and v > 1 else (11 if v == 1 else 10))
            r, c = self.get_rc(hand_value + card.get_value(), dealer_card_value)
            value += self.get_value(r, c) * self.get_card_prob(card.get_value())
        stand_prob = 0
        hit_prob = 0

        if(stand_value > value):
            stand_prob = 1
        elif(stand_value < value):
            hit_prob = 1
        else:
            hit_prob = stand_prob = 0.5

        policy = [stand_prob, hit_prob]
        self.policy[row][col] = policy

    # events and input handling
    def __events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                print("event yo!")
                if event.key == pygame.K_s:      self.update_value(); self.update_policy()
                if event.key == pygame.K_v:      self.update_value()
                if event.key == pygame.K_p:      self.update_policy()


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
    def deal(self): 
        v = random.randint(0, 12)
        return Card(0, v if v < 10 and v > 1 else (11 if v == 1 else 10))

b = BlackjackRL()

while True:
    b.update()
    b.update_value()
    b.update_policy()


