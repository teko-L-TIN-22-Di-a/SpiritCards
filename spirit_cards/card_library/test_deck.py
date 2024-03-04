
from spirit_cards.card_engine.card import Card
from spirit_cards.card_library.test_card import get_test_card, get_test_card2, get_test_card3, get_test_card4


def get_test_deck() -> list[Card]:
    return [
        *[get_test_card() for x in range(0, 10)],
        *[get_test_card2() for x in range(0, 10)],
        *[get_test_card3() for x in range(0, 10)],
        *[get_test_card4() for x in range(0, 10)]
    ]
        
    