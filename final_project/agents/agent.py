from game.players import BasePokerPlayer
from agents.util import *

class MCPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state, cfg):
        print(hole_card)
        print(round_state)
        for i, card in enumerate(hole_card):
            hole_card[i] = f"{card[1]}{card[0].lower()}"
        for i, card in enumerate(round_state['community_card']):
            round_state['community_card'][i] = f"{card[1]}{card[0].lower()}"
        win_ratio = monte_carlo(hole_card, round_state['community_card'])
        print(win_ratio)
        # print(valid_actions)
        if(round_state['street'] == 'preflop'):
            # 0.4, 0.3, 0.2
            criteria1 = cfg.preflop_1_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria2 = cfg.preflop_2_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria3 = cfg.preflop_3_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
        elif(round_state['street'] == 'flop'):
            # .45 .3 .05
            criteria1 = cfg.flop_1_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria2 = cfg.flop_2_prob   + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria3 = cfg.flop_3_prob   + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
        elif(round_state['street'] == 'turn'):
            # .55 .45 .05
            criteria1 = cfg.turn_1_prob   + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria2 = cfg.turn_2_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria3 = cfg.turn_3_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
        else:
            # .65 .55 .05
            criteria1 = cfg.river_1_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria2 = cfg.river_2_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            criteria3 = cfg.river_3_prob  + (- round_state['round_count'] / 400 if round_state['round_count']>15 else 0)
            
        if(win_ratio[0]>criteria1):
            if(valid_actions[2] is not None):
                ratio = (win_ratio[0]-criteria1)*2 if (win_ratio[0]-criteria1)*2 < 1 else 1
                amount = int(valid_actions[2]['amount']['max']*ratio)
                return 'raise', amount
            elif(valid_actions[1] is not None):
                amount = valid_actions[1]['amount']
                return 'call', amount
            else:
                return 'fold', 0
        elif(win_ratio[0]>criteria2):
            if(valid_actions[2] is not None):
                ratio = (win_ratio[0]-criteria2)*2 if (win_ratio[0]-criteria2)*2 < 1 else 1
                amount = valid_actions[2]['amount']['max']//3
                return 'raise', amount
            elif(valid_actions[1] is not None):
                amount = valid_actions[1]['amount']
                return 'call', amount
            else:
                return 'fold', 0
        elif(win_ratio[0]>criteria3):
            if(valid_actions[1] is not None):
                amount = valid_actions[1]['amount']
                return 'call', amount
            else:
                return 'fold', 0
        else:
            return 'fold', 0
            
        
    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai(cfg):
    return MCPlayer(cfg)
