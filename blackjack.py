import pygame
from settings import *
import time
import random
import threading
from prettytable import PrettyTable

class BlackjackRL:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blackjack")
        pygame.key.set_repeat(500, 100)
        self.__cols = 10
        self.__rows = 28
        self.__width = (self.__cols + 1) * 64
        self.__height = (self.__rows + 1) * 15
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__font = pygame.font.SysFont("monospace", 12) 
        self.bet_amount = 10.0
        self.__init_grid()
        self.__deck = Deck()
        self.current_hand = []
        self.dealer_hand = []
        self.states = set()
        self.updates = 0
        self.episode_gen_policy = self.greedy_naive #self.random_state #self.epsilon_greedy #self.greedy_naive
        self.epsilon = 0.20

    def __init_grid(self):
        self.values = {}
        self.__set_inital_policy()

    def __set_inital_policy(self):
        self.policy = {}

    #draw states
    def update(self):
        self.__events()
        state_to_draw = None
        for state in self.policy.keys():
            r = state[0]
            if(state[1] == 1):
                r += 10  
            self.__draw_strategy(self.__screen, r-4, state[2] - 2, self.policy[state].index(max(self.policy[state])))
            self.__draw_tile(self.__screen, r-3, 0, ("Soft " if state[1] == 1 else "") + str(state[0]), (255, 255, 255))
            rect = pygame.Rect((state[2] - 1) * 64, (r-3) * 15, 64, 15)
            if(rect.collidepoint(pygame.mouse.get_pos())):
                state_to_draw = state

        for i in range(2, 12):
            self.__draw_tile(self.__screen, 0, i-1, (str(i) if i < 11 else "A"), (255, 255, 255))
        label = self.__font.render(str(self.updates), 1, (255, 255, 255), (0, 0, 0, 0.5))
        self.__screen.blit(label, (2, 2))
        if(state_to_draw != None):
            self.draw_details(state_to_draw)
        pygame.display.flip()
    
    #draw details menu
    def draw_details(self, state):
        self.draw_bordered_text(self.__screen, str(state), 5, self.__height - 113, CYAN, BLACK)
        best = self.policy[state].index(max(self.policy[state]))
        draw_index = 0
        for i in range(len(LEGAL_ACTIONS)):
            action = LEGAL_ACTIONS[i]
            if not (state, action) in self.values.keys(): 
                continue
            text_color = GREEN if i == best else WHITE
            avg = format(self.values[(state, action)]['sum'] / self.values[(state, action)]['plays'], '.2f')
            self.draw_bordered_text(self.__screen, STRATEGY_TYPE_CAPTION[i] + ": " + str(avg), 5, self.__height - 100 + (draw_index*13), STRATEGY_TYPE_COLOR[i], BLACK)
            draw_index+=1 
        
    def draw_bordered_text(self, surface, text, x, y, fg_color, bg_color):
        label2 = self.__font.render(text, 0, fg_color, bg_color)
        surface.blit(label2, (x, y))

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

    def play_dealer(self, current_count, dealer_hand):
        while dealer_hand.count <= current_count and dealer_hand.count < 17:
            dealer_hand.add_card(self.__deck.deal())

    def get_legal_actions(self, hand):
        actions = [STAND]
        if(hand.count < 21):
            actions.append(HIT)
            if(len(hand.cards) == 2):
                actions.append(DOUBLE)
        return actions

    #random policy
    def random_state(self, state, hand):
        return random.choice(self.get_legal_actions(hand))
    
    #epsilon greedy policy
    def epsilon_greedy(self, state, hand):
        if(not state in self.policy.keys()):
            return self.random_state(state, hand)
        best = self.policy[state].index(max(self.policy[state]))
        if(random.randint(0, 100000) < 100000 * self.epsilon):
            return self.random_state(state, hand)
        return best
    #greedy naive policy
    def greedy_naive(self, state, hand):
        self.epsilon = 0
        return self.epsilon_greedy(state, hand)

    #play a game vs the dealer
    def play_game(self):
        current_hand = Hand()
        current_hand.add_card(self.__deck.deal())
        current_hand.add_card(self.__deck.deal())
        dealer_hand = Hand()
        dealer_hand.add_card(self.__deck.deal())
        playedDouble = False

        while True:
            if(current_hand.count > 21 or playedDouble):
                break
            state = (current_hand.count, 0 if current_hand.aces == 0 else 1, dealer_hand.count)
            action = self.policy[state].index(max(self.policy[state]))
            if action == HIT:
                current_hand.add_card(self.__deck.deal())
            if action == DOUBLE:
                playedDouble = True
                current_hand.add_card(self.__deck.deal())
            if action == STAND:
                break
        if(current_hand.count <= 21):
            self.play_dealer(current_hand.count, dealer_hand)

        returnVal = PUSH

        if(current_hand.count > 21):
            returnVal = PLAYER_BUST
        elif(dealer_hand.count > 21):
            returnVal = DEALER_BUST
        elif(current_hand.count > dealer_hand.count):
            returnVal = PLAYER_WIN
        elif(current_hand.count < dealer_hand.count):
            returnVal = DEALER_WIN

        return returnVal

    def update_value(self):
        self.updates += 1
        dealer_hand = Hand()
        current_hand = Hand()

        #setup hands
        current_hand.add_card(self.__deck.deal())
        current_hand.add_card(self.__deck.deal())
        dealer_hand.add_card(self.__deck.deal())

        episode = []
        playedDouble = False

        #play out an episode
        while True:
            if(current_hand.count > 21 or playedDouble):
                break
            state = (current_hand.count, 0 if current_hand.aces == 0 else 1, dealer_hand.count)
            self.states.add(state)
            action = self.episode_gen_policy(state, current_hand)
            sa = (state, action)
            episode.append(sa)
            if action == HIT:
                current_hand.add_card(self.__deck.deal())
            if action == DOUBLE:
                playedDouble = True
                current_hand.add_card(self.__deck.deal())
            if action == STAND:
                break
        
        #determine winner
        if(current_hand.count <= 21):
            self.play_dealer(current_hand.count, dealer_hand)

        bet_return = 0
        if(current_hand.count > 21):
            bet_return = -self.bet_amount
        elif(dealer_hand.count > 21):
            bet_return = self.bet_amount
        elif(current_hand.count > dealer_hand.count):
            bet_return = self.bet_amount
        elif(current_hand.count < dealer_hand.count):
            bet_return = -self.bet_amount

        if(playedDouble):
            bet_return *= 2

        #update values
        for scene in episode:
            if not scene in self.values.keys():
                self.values[scene] = {}
                self.values[scene]['sum'] = 0
                self.values[scene]['plays'] = 0
                self.values[scene]['value'] = 0
            self.values[scene]['plays'] += 1.0
            self.values[scene]['sum'] += bet_return
            ALPHA = 1.0/self.values[scene]['plays']
            self.values[scene]['value'] += ALPHA * (bet_return - self.values[scene]['value'])

    #update policy
    def update_policy(self):
        policy = {}
        for state in self.states:
            best = -1000000
            best_actions = []
            #loop actions
            for i in range(len(LEGAL_ACTIONS)):
                action = LEGAL_ACTIONS[i]
                if(not (state, action) in self.values.keys()):
                    continue
                value = self.values[(state, action)]['value']# self.values[(state, action)]['sum'] / self.values[(state, action)]['plays']
                #find best action
                if(value > best):
                    best = value
                    best_actions = [i]
                elif(value == best):
                    best_actions.append(i)
            policy[state] = []
            #update policies
            for i in range(len(LEGAL_ACTIONS)):
                if i in best_actions:
                    policy[state].append(1/len(best_actions))
                else:
                    policy[state].append(0)
        self.policy = policy

    # events and input handling
    def __events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:      self.update_value(); self.update_policy()
                if event.key == pygame.K_v:      self.update_value()
                if event.key == pygame.K_p:      self.update_policy()


#hand class
class Hand:
    def __init__(self):
        self.count = 0
        self.cards = []
        self.aces = 0
    
    def add_card(self, card):
        self.count += card.get_value()
        self.cards.append(card)
        if card.get_value() == 11:
            self.aces += 1
        while self.count > 21 and self.aces > 0:
            self.count -= 10
            self.aces -= 1
#card class
class Card:
    def __init__(self, suit, value):
        self.__suit = suit
        self.__value = value
    def get_suit(self): return self.__suit
    def get_value(self): return self.__value

#deck class
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

#seperate updates from rendering so it is faster
def updates(b):
    while True:
        b.update_value()
        b.update_policy()
        if(b.updates == 100000):
            break

    results = {}
    results[PUSH] = 0.0
    results[DEALER_BUST] = 0.0
    results[PLAYER_BUST] = 0.0
    results[DEALER_WIN] = 0.0
    results[PLAYER_WIN] = 0.0

    games_to_play = 100000
    for i in range(games_to_play):
        results[b.play_game()] += 1.0

    win = str(((results[PLAYER_WIN] + results[DEALER_BUST]) / games_to_play) * 100) + "%"
    loss = str(((results[DEALER_WIN] + results[PLAYER_BUST]) / games_to_play) * 100) + "%"
    push = str((results[PUSH] / games_to_play) * 100) + "%"
    table = PrettyTable()
    table.field_names = list(TABLE_CAPTION.values()) + ["Total Plays", "Win %", "Loss %", "Push %"]
    table.add_row(list(results.values()) + [sum(results.values()), win, loss, push])
    print(table)


    

t = threading.Thread(target=updates, args=[b])
t.daemon = True
t.start()

while True:
    b.update()



