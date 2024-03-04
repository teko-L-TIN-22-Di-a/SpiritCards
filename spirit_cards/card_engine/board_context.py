from spirit_cards.card_engine.card_player import CardPlayer

class BoardContext:
    round_count: int = 1

    # Round independent player views
    player1: CardPlayer
    player2: CardPlayer

    # Player depending on who is playing this round
    player: CardPlayer
    opponent: CardPlayer

    def __init__(self, player, opponent):
        self.player = self.player1 = player
        self.opponent = self.player2= opponent
    