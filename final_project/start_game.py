import json
from game.game import setup_config, start_poker
from agents.agent import setup_ai as mc_ai

from baseline0 import setup_ai as baseline0_ai

config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
config.register_player(name="p1", algorithm=baseline0_ai())
config.register_player(name="p2", algorithm=mc_ai())

## Play in interactive mode if uncomment
#config.register_player(name="me", algorithm=console_ai())
game_result = start_poker(config, verbose=1)