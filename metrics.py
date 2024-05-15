def win_rate(players, games):
  d = dict.fromkeys([a.name for a in players], 0)
  for game in games:
    for winner in game['winner']:
      d[winner] += 1
  return pd.DataFrame(d, index = ['Winrate']).T / len(games)

def rationality_stag_hunt(players, games, n_rounds):
  d = dict.fromkeys([a.name for a in players], 0)
  for game in games:
    for m_1, m_2 in zip(game[players[0].name]['moves'], game[players[1].name]['moves']):
      if m_1 == 'rabbit':
        d[players[0].name] += 1
      if m_2 == 'rabbit':
        d[players[1].name] += 1
  return pd.DataFrame(d, index = ['Rationality_stag_hunt']).T / (len(games) * n_rounds)

def rationality_public_goods(players, games, n_rounds):
  d = dict.fromkeys([a.name for a in players], 0)
  for game in games:
    for m_1, m_2, m_3 in zip(game[players[0].name]['moves'],
                             game[players[1].name]['moves'],
                             game[players[2].name]['moves']):
      for num, move in enumerate([m_1, m_2, m_3]):
        if move == min([m_1, m_2, m_3]):
          d[players[num].name] += 1
  return pd.DataFrame(d, index = ['Rationality_public_goods']).T / (len(games) * n_rounds)