class StagHuntAgent:
  def __init__(self, model = None, name = 'Player 0', prompt_type = stag_zero_shot_prompt):
    self.name = name
    self.prompt_type = prompt_type
    self.model = model

  def get_answer(self, rounds, cur_round, agents, moves):
    if cur_round == 1:
      return model(base_stag_prompt.format(rounds = rounds, cur_round = cur_round, player_name = self.name) \
                           + "As for now there are no previous moves." +  self.prompt_type)
    else:
      return model(base_stag_prompt.format(rounds = rounds,
                                                            cur_round = cur_round, player_name = self.name) \
                           + stag_history_prompt.format(agent_1 = agents[0].name, \
                                                   agent_2 = agents[1].name, moves_1 = moves[0], moves_2 = moves[1]) + self.prompt_type)

class PublicGoodsAgent:
  def __init__(self, name, prompt_type = pg_zero_shot_prompt):
    self.name = name
    self.prompt_type = prompt_type
    self.model = model
    self.money = 100

  def get_answer(self, rounds, cur_round, agents, moves, multiplier):
    if cur_round == 1:
      return model(base_pg_prompt.format(rounds = rounds, 
                                                          multiplier = multiplier) \
                           + "As for now there are no previous moves." +  self.prompt_type)
    else:
      return model(base_pg_prompt.format(rounds = rounds, 
                                                          cur_round = cur_round, 
                                                          player_name = self.name,
                                                          multiplier = multiplier) \
                           + pg_history_prompt.format(agent_1 = agents[0].name,
                                                   agent_2 = agents[1].name,
                                                   agent_3 = agents[2].name,
                                                   moves_1 = moves[0], 
                                                   moves_2 = moves[1],
                                                   moves_3 = moves[2]) + self.prompt_type)


class HanabiAgent:
  def __init__(self, model = None, name = 'Player 0', prompt_type = hanabi_action_prompt, mistakes_left = 3, hints_left = 3):
    self.name = name
    self.prompt_type = prompt_type
    self.model = model
    self.mistakes_left = mistakes_left
    self.hints_left = hints_left
    self.cards = []
    self.revealed_cards = []

  def get_answer(self, other_agent_cards, fireworks, life_tokens, hint_tokens,
                 revealed_cards, deck_size, opponent_action, last_played, available):
    prompt = hanabi_system_prompt + hanabi_observation_prompt.format(
        other_hands = other_agent_cards, fireworks = fireworks, 
        tokens = {'life_tokens': life_tokens, 'hint_tokens': hint_tokens}, 
        revealed_cards = revealed_cards, deck_size = deck_size, 
        opponent_action = opponent_action, last_played = last_played, 
        available = available) + hanabi_action_prompt
    ans = model(prompt)  
    return ans