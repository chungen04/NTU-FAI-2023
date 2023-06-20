import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
from agents.agent import setup_ai as mc_ai
import argparse

class cfg:
    def __init__(self) -> None:
        self.baseline = -1
    
parser = argparse.ArgumentParser()
parser.add_argument('--baseline', type=int)

args = parser.parse_args()
cfgs = cfg()
# cfg.preflop_1_prob = args.preflop_1_prob
# cfg.preflop_2_prob = args.preflop_2_prob
# cfg.preflop_3_prob = args.preflop_3_prob
# cfg.flop_1_prob = args.flop_1_prob
# cfg.flop_2_prob = args.flop_2_prob
# cfg.flop_3_prob = args.flop_3_prob
# cfg.turn_1_prob = args.turn_1_prob
# cfg.turn_2_prob = args.turn_2_prob
# cfg.turn_3_prob = args.turn_3_prob
# cfg.river_1_prob = args.river_1_prob
# cfg.river_2_prob = args.river_2_prob
# cfg.river_3_prob = args.river_3_prob
cfgs.baseline = args.baseline
# cfg.preflop_1_prob = 0.4
# cfg.preflop_2_prob = 0.3
# cfg.preflop_3_prob = 0.2
# cfg.flop_1_prob = 0.45
# cfg.flop_2_prob = 0.3
# cfg.flop_3_prob = 0.05
# cfg.turn_1_prob = 0.55
# cfg.turn_2_prob = 0.45
# cfg.turn_3_prob = 0.05
# cfg.river_1_prob = 0.65
# cfg.river_2_prob = 0.55
# cfg.river_3_prob = 0.05

if(cfgs.baseline == 0):
    from baseline0 import setup_ai as baseline0_ai
elif(cfgs.baseline == 1):
    from baseline1 import setup_ai as baseline0_ai
elif(cfgs.baseline == 2):
    from baseline2 import setup_ai as baseline0_ai
elif(cfgs.baseline == 3):
    from baseline3 import setup_ai as baseline0_ai
elif(cfgs.baseline == 4):
    from baseline4 import setup_ai as baseline0_ai
elif(cfgs.baseline == 5):
    from baseline5 import setup_ai as baseline0_ai

config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
config.register_player(name="p1", algorithm=baseline0_ai())
config.register_player(name="p2", algorithm=mc_ai(cfgs))

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