class StagHuntGame:
  def __init__(self, id, n_rounds, agents = []):
    self.id = id
    self.n_rounds = n_rounds
    self.cur_round = 0
    self.agents = agents
    self.history_dict = {'winner': []}
    for agent in self.agents:
      self.history_dict[agent.name] = {'score': 0, 'moves': [], 'text_moves': []}
    self.history_dict['agents'] = [agent.name for agent in agents]
    self.history_dict['n_rounds'] = n_rounds
    self.payoff = {'deer': {'deer': 5, 'rabbit': 0}, 'rabbit': {'deer': 4, 'rabbit': 2}}


  def step(self):
    self.cur_round += 1
    for agent in self.agents:
      answer = agent.get_answer(self.n_rounds, self.cur_round, self.agents,
       [self.history_dict[a.name]['moves'][:self.cur_round-1] for a in self.agents])
      self.history_dict[agent.name]['text_moves'].append(answer)
      answer = re.sub(r'[^\w \n]', '', answer)
      answer = re.search(r'Answer I choose \w+', answer)

      self.history_dict[agent.name]['moves'].append(answer.group(0).strip().split()[-1])

    self.history_dict[self.agents[0].name]['score'] += \
    self.payoff[self.history_dict[self.agents[0].name]['moves'][-1]][self.history_dict[self.agents[1].name]['moves'][-1]]

    self.history_dict[self.agents[1].name]['score'] += \
    self.payoff[self.history_dict[self.agents[1].name]['moves'][-1]][self.history_dict[self.agents[0].name]['moves'][-1]]

  def play(self, save_to_json = False):
    global games
    while self.cur_round < self.n_rounds:
      self.step()
    if self.history_dict[self.agents[0].name]['score'] > self.history_dict[self.agents[1].name]['score']:
      self.history_dict['winner'].append(self.agents[0].name)
    elif self.history_dict[self.agents[1].name]['score'] > self.history_dict[self.agents[0].name]['score']:
      self.history_dict['winner'].append(self.agents[1].name)
    else:
      self.history_dict['winner'] = [self.agents[0].name, self.agents[1].name]
    if save_to_json:
      with open(self.id + ".json", "w") as f:
        json.dump(self.history_dict, f)
    games.append(self.history_dict)
    return self.history_dict

class PublicGoodsGame:
  def __init__(self, id, n_rounds, agents, multiplier):
    self.id = id
    self.n_rounds = n_rounds
    self.cur_round = 0
    self.agents = agents
    self.multiplier = 5
    self.current_sum = 0
    self.history_dict = {'winner': []}
    for agent in self.agents:
      self.history_dict[agent.name] = {'score': 0, 'moves': [], 'text_moves': []}
    self.history_dict['agents'] = [agent.name for agent in agents]
    self.history_dict['n_rounds'] = n_rounds

  def step(self):
    self.cur_round += 1

    for agent in self.agents:
      ans_final = None

      while ans_final is None:
        ans_initial = agent.get_answer(self.n_rounds, self.cur_round, [a.name for a in self.agents],
        [self.history_dict[a.name]['moves'][:self.cur_round-1] for a in self.agents], self.multiplier)
        ans_final = re.sub(r'[^\w ]', '', ans_initial.lower())
        ans_final = re.search(r'i contribute \d+', ans_final)

      num = int(ans_final.group(0).strip().split()[-1])
      self.history_dict[agent.name]['moves'].append(num)
      self.history_dict[agent.name]['text_moves'].append(ans_initial)
      self.current_sum+=num
      agent.money -= num


  def play(self, save_to_json = False):
    global games
    while self.cur_round < self.n_rounds:
      self.step()

    self.current_sum*=self.multiplier
    for num, agent in enumerate(self.agents):
      self.agents[num].money += self.current_sum // len(self.agents)
    m = 0
    for agent in self.agents:
      self.history_dict[agent.name]['score'] = agent.money
      if agent.money > m:
        self.history_dict['winner'] = [agent.name]
        m = agent.money
      elif agent.money == m and self.history_dict.get('winner'):
        self.history_dict['winner'].append(agent.name)
    if save_to_json:
      with open(self.id + ".json", "w") as f:
        json.dump(self.history_dict, f)
    games.append(self.history_dict)
    return self.history_dict

class HanabiGame:
  def __init__(self, agents, cards_in_hand = 5, colors = ['white', 'yellow', 'green', 'blue', 'red']):
    self.deck = []
    self.agents = agents
    self.fireworks = []
    self.last_action = None
    self.last_played = None
    self.fireworks_colors = set()
    self.cards_in_hand = cards_in_hand
    self.colors = colors
    self.history_dict = {}
    self.history_dict['agents'] = [agent.name for agent in agents]
    self.history_dict['n_rounds'] = None
    for agent in self.agents:
      self.history_dict[agent.name] = {'cards': [], 'moves': [], 'text_moves': []}


  def init_deck(self):
    for color in self.colors:
      for num in [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]:
        self.deck.append([color, num])
    shuffle(self.deck)

  def init_hands(self):
    for num, agent in enumerate(self.agents):
      for i in range(self.cards_in_hand):
        self.agents[num].cards.append(self.deck.pop())
        self.agents[num].revealed_cards.append([None, None])

  def step(self, agent, other_agent):

    available = set()

    for num, card in enumerate(agent.cards):
      if card != [None, None]:
        available.add(f'discard card {num+1}')
        available.add(f'play card {num+1}')
        if agent.hints_left > 0:
          available.add(f'reveal all {card[0]}')
          available.add(f'reveal all {card[1]}')
    available = list(available)

    ans_final = None
    while ans_final is None:

      ans_initial = agent.get_answer(other_agent.cards, self.fireworks, agent.mistakes_left,
                                agent.hints_left, agent.revealed_cards,
                                len(self.deck), self.last_action, self.last_played,
                                available)
      ans_final = re.sub(r'\*', '', ans_initial)
      ans_final = re.search(r'Action: .*[.,\n*]', ans_final)

    self.history_dict[agent.name]['text_moves'].append(ans_initial)
    self.history_dict[agent.name]['moves'].append(ans_final)
    action = ans_final.group(0).strip().split()[1]
    move = ans_final.group(0).strip().split()[3]


    self.last_action = ans_initial

    if action.lower() == 'discard':
      card_idx = int(move) - 1
      agent.hints_left = min(8, agent.hints_left+1)
      if self.deck:
        agent.cards[card_idx] = self.deck.pop()
      agent.revealed_cards[card_idx] = [None, None]

    elif action.lower() == 'play':
      card_idx = int(move) - 1
      put = False
      for num, firework in enumerate(self.fireworks):
        if agent.cards[card_idx][1] == 1 and agent.cards[card_idx][0] not in self.fireworks_colors:
          self.fireworks.append([agent.cards[card_idx]])
          self.fireworks_colors.add(agent.cards[card_idx][0])
        elif firework[-1][0] == agent.cards[card_idx][0] and firework[-1][1]+1 == agent.cards[card_idx][1]:
            self.fireworks[num].append(agent.cards[card_idx])
            put = True
            self.last_played = agent.cards[card_idx]
            break
      if len(self.fireworks) > 2:
        if len(self.fireworks[0]) == 5 and len(self.fireworks[1]) == 5:
          return 'win'
      if not put:
        agent.mistakes_left -= 1
        if agent.mistakes_left == 0:
          return 'lose'

      if self.deck:
        agent.cards[card_idx] = self.deck.pop()
      agent.revealed_cards[card_idx] = [None, None]

    elif action.lower() == 'reveal':
      idx = 0
      if move.isdigit():
        idx = 1
      for num, card in enumerate(other_agent.cards):
        if card[idx] == move:
          other_agent.revealed_cards[num][idx] = move
      agent.hints_left -= 1

    self.history_dict[agent.name]['cards'].append(agent.cards)

    return 'ok'

  def play(self, save_to_json = False):

      self.init_deck()
      self.init_hands()

      while self.deck:
        res = self.step(self.agents[0], self.agents[1])
        if res == 'lose':
          self.score = 0
          return
        elif res == 'win':
          self.score = 10
          return
        res = self.step(self.agents[1], self.agents[0])
        if res == 'lose':
          self.score = 0
          return
        elif res == 'win':
          self.score = 10
          return
      for f in self.fireworks:
        self.score += len(f)

      if save_to_json:
        with open(self.id + ".json", "w") as f:
          json.dump(self.history_dict, f)
      games.append(self.history_dict)
      return self.history_dict