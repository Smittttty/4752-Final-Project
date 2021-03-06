HIT     = 0
STAND   = 1
DOUBLE  = 2
SPLIT   = 3

STRATEGY_TYPE_COLOR = {}
STRATEGY_TYPE_COLOR[HIT]    = (255, 0, 0)
STRATEGY_TYPE_COLOR[STAND]  = (255, 255, 0)
STRATEGY_TYPE_COLOR[DOUBLE] = (0, 0, 255)
STRATEGY_TYPE_COLOR[SPLIT]  = (0, 255, 0)

STRATEGY_TYPE_CAPTION = {}
STRATEGY_TYPE_CAPTION[HIT]    = "HIT"
STRATEGY_TYPE_CAPTION[STAND]  = "STAND"
STRATEGY_TYPE_CAPTION[DOUBLE] = "DOUBLE"
STRATEGY_TYPE_CAPTION[SPLIT]  = "SPLIT"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

PUSH = 0
DEALER_BUST = 1
PLAYER_BUST = 2
DEALER_WIN = 3
PLAYER_WIN = 4

TABLE_CAPTION = {}
TABLE_CAPTION[PUSH] = "Pushes"
TABLE_CAPTION[DEALER_BUST] = "Dealer Busts"
TABLE_CAPTION[PLAYER_BUST] = "Player Busts"
TABLE_CAPTION[DEALER_WIN] = "Dealer Wins"
TABLE_CAPTION[PLAYER_WIN] = "Player Wins"

LEGAL_ACTIONS = [HIT, STAND, DOUBLE]
ALPHA = 0.1