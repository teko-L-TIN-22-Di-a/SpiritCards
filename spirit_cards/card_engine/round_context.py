from dataclasses import dataclass
from spirit_cards.card_engine.card_player import CardPlayer

class RoundContext:

    round_count: int = 1

    player: CardPlayer
    opponent: CardPlayer

    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent