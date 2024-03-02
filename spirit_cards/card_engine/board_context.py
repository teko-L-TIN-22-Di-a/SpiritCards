from spirit_cards.card_engine.slot import Slot

class BoardContext:
    BATTLE_SLOT_COUNT = 4
    SUPPORT_SLOT_COUNT = 2
    HAND_SIZE = 5

    battle_slots: list[Slot]
    support_slots: list[Slot]
    hand_slots: list[Slot]
    grave_slots: list[Slot]
    