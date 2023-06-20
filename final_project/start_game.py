import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
from agents.agent import setup_ai as mc_ai

from baseline4 import setup_ai as baseline0_ai

config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
config.register_player(name="p1", algorithm=baseline0_ai())
config.register_player(name="p2", algorithm=mc_ai())

## Play in interactive mode if uncomment
#config.register_player(name="me", algorithm=console_ai())
ai_win = 0
for i in range(10):
    game_result = start_poker(config, verbose=1)
    print(json.dumps(game_result, indent=4))
    print(game_result)
    if game_result['players'][1]['stack']>game_result['players'][0]['stack'] :
        ai_win += 1
game_result = start_poker(config, verbose=1)
print(f"me win ratio: {ai_win/10}")