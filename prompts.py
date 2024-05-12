base_stag_prompt = """You are playing a repeated game with another player for 
{rounds} turns. Current turn is {cur_round}. You are {player_name}.
Each turn you may hunt for a deer and if another hunter chooses to hunt for a 
deer, each of you will receive 5 points.However, if you choose to hunt for a 
deer, while the other one hunts for a rabbit, you will receive nothing, while 
the other player will receive 4 points and vice versa.If both of you decide to 
hunt for a rabbit, then each of you will receive 2 points. 
Your goal is to maximize your personal score."""

stag_history_prompt = "The previous moves are {agent_1}: {moves_1}, {agent_2}: {moves_2}"

stag_zero_shot_prompt = 'Make a best move based on your predictions. Your prediction should be based on previous steps. You must answer with the template "I choose x" where x is either deer or rabbit'

stag_cot_prompt = stag_zero_shot_prompt + "Let's think step by step"

stag_predict_prompt =  stag_zero_shot_prompt + "First, calculate all possible outcomes and try to predict another player's move."

base_pg_prompt = """Welcome to the 'Public Good' game. Here is the game setting and rules.

- Each of you starts with 100 monetary points. In each of the {rounds} rounds, you will publicly decide how much to contribute to a communal pool. 
- The total contributions from all the players to this pool are times with {multiplier} and then evenly divided among all players. Contributions are public and known to all players after each round. 
- The winner is determined at the end of the {rounds} rounds, and is the player whose total of remaining points and the points earned from the communal pool is the highest. 
- Be mindful of the final stage where you can have chance to vote to penalize others, typically driven by perceptions of unfair contributions throughout the game."""

pg_history_prompt = "The previous moves are {agent_1}: {moves_1}, {agent_2}: {moves_2}, {agent_3}: {agent_3}"

pg_zero_shot_prompt = '''Based on your own analysis about others and other's thoughts, make the decision about your own contribution to achieve the highest replayment for yourself. Remember
- Your total investment should the least to win the game;
- Your target is to get highest points and also promote the commumal repayment to get as much as more points at the end.
You must answer with the template "I contribute xx". '''

pg_cot_prompt = pg_zero_shot_prompt + "Let's think step by step."

pg_predict_prompt =  pg_zero_shot_prompt + "First, try to predict moves of other two players, then choose the optimal amount of money to contribute."

hanabi_system_prompt = """You are playing a Hanabi game. There are the basic
rules for Hanabi with a small structure: Hanabi is a 2 player-cooperative game 
where you should work together to form fireworks. A firework is a set of cards 
of the same color, ordered from 1 to 5. Cards in the game have both a color and 
a number; there are two colors and five numbers in total. Each player can only 
view the cards another player holds, but not their own. Players cannot directly 
communicate with each other, but must instead remove an infotoken from play to 
give information. Players can tell other players which of the cards in their 
hand is a specific color, or a specific number. You must point out all the cards
of this color or number. There are initially 3 info tokens, but players can 
discard cards in their hand and draw a new card from the deck to return an 
infotoken into play. Players can also play a card from their hand: the card must
either begin a new firework (card number should be "1") or be appended to an 
existing firework. However, 2 fireworks cannot have the same color, and a single
firework cannot repeat numbers. If the played card does not satisfy these 
conditions, a life token is placed. The game ends when either 3 life tokens have
been placed, all 2 fireworks have been completed, or all cards have been drawn 
from the deck. Points are awarded based on the largest card value in each 
created firework. In this game, you and your opponent are players. Each person 
has two handcards, each with two colors and five possible numbers from 1 to 5. 
Each player has 3 info tokens and 3 life tokens."""

hanabi_observation_prompt = """Your observation now is: 
The cards in another player’s hands are:{other_hands} 
The current fireworks is:{fireworks} 
The current number of tokens is {tokens} 
The information of your own cards that was revealed is:{revealed_cards} 
The current deck size is {deck_size} 
Your opponent’s action is {opponent_action}
The card that the opponent last played or discarded is {last_played} 
Now you can choose one of the following actions: {available}"""

hanabi_action_prompt = """You should think step by step and output your action. 
For example: "reveal all yellow cards for another player" or "play card 1" to
play the first card from your hand. You will respond with an action, 
formatted as: "Action: <action>" where you replace <action> with your 
actual action. You should explain why you chose the action."""