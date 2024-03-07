import pygame
from spirit_cards.card_engine.board_constants import BoardConstants
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.scenes.encounter_scenes.board_components.slot_component import SlotComponent


class HandZone(UIComponent):

    player: CardPlayer

    slots_components: list[SlotComponent]

    def __init__(self, player: CardPlayer, rect: pygame.Rect, margin: pygame.Vector2):
        super().__init__(rect, margin)
        self.player = player
        self.slots_components = []

        self._initialize_component()

    def update(self):
        self.slots_components = []

        if(len(self.player.hand) <= 0):
            return

        card_size = pygame.Vector2((185*0.5, 256*0.5))
        margin = pygame.Vector2(24, 4)
        inner_rect = self.get_inner_rect()
        slot_size = pygame.Vector2(inner_rect.width / max(BoardConstants.HAND_SIZE, len(self.player.hand)), inner_rect.height)

        for i, slot in enumerate(self.player.hand):
            self.slots_components.append(SlotComponent(
                slot,
                pygame.Rect(
                    inner_rect.x + slot_size.x * i, inner_rect.y + 0,
                    card_size.x+margin.x*2, card_size.y+margin.y*2
                ), margin)
            )

    def _initialize_component(self):
        self.update()