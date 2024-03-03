
from dataclasses import dataclass
import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.slot import Slot
from spirit_cards.core.context import Context
from spirit_cards.pygame_extension.event_buffer import EventBuffer
from spirit_cards.pygame_extension.gui.msg_box import MsgBox, MsgBoxConfiguration
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.encounter_scenes.board_components.battle_zone import BattleZone
from spirit_cards.scenes.encounter_scenes.board_components.hand_zone import HandZone
from spirit_cards.scenes.encounter_scenes.board_components.slot_component import SlotComponent
from spirit_cards.scenes.encounter_scenes.board_components.support_zone import SupportZone
from spirit_cards.scenes.encounter_scenes.encounter_services import EncounterServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices
    
class BoardSide(UIComponent):

    _context: Context
    _msg_box: MsgBox
    _event_buffer: EventBuffer

    _card_texture: pygame.Surface

    battle_zone: BattleZone
    support_zone: SupportZone
    hand_zone: HandZone

    battle_slots: list[Slot]
    support_slots: list[Slot]
    hand_slots: list[Slot]

    def __init__(self, rect: pygame.Rect, context: Context):
        super().__init__(rect)

        self._context = context
        self._msg_box = self._context.get_service(EncounterServices.MESSAGE_BOX)
        self._event_buffer = context.get_service(PygameServices.EVENT_BUFFER)
        asset_manager: AssetManager = self._context.get_service(GlobalServices.ASSET_MANAGER)
        self._card_texture = asset_manager.get_image(AssetMap.TEST_CARD)

        self.battle_slots = [Slot() for x in range(0, BoardContext.BATTLE_SLOT_COUNT)]
        self.support_slots = [Slot() for x in range(0, BoardContext.SUPPORT_SLOT_COUNT)]
        self.hand_slots = []

        self._initialize_component()

    def draw_to_surface(self, mouse_pos: pygame.Vector2, flipped: bool = False) -> pygame.Surface:

        if(flipped):
            board_center = self.get_rect().center
            mouse_pos = (mouse_pos - board_center).rotate(180) + board_center

        size = pygame.Vector2(self.get_rect().size)
        board_surface = pygame.Surface(size)
        
        pygame.draw.rect(board_surface, "#092B40", pygame.Rect(0,0,size.x, size.y))
        pygame.draw.rect(board_surface, "#405F73", self.battle_zone.get_inner_rect(), 2, 4)
        pygame.draw.rect(board_surface, "#405F73", self.support_zone.get_inner_rect(), 2, 4)
        pygame.draw.rect(board_surface, "#405F73", self.hand_zone.get_inner_rect(), border_radius=4)

        slots = (
            self.battle_zone.slots_components + 
            self.support_zone.slots_components
        )

        click = False

        for event in self._event_buffer.get_events():
            if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # 1 == Left mouse button
                click = True

        for slot in slots:
            if(slot.get_inner_rect().collidepoint(mouse_pos.x, mouse_pos.y)):
                pygame.draw.rect(board_surface, "Green", slot.get_inner_rect(), border_radius=4)

                if(click):
                    self._show_msg_box(slot, flipped)

            pygame.draw.rect(board_surface, "#5A798C", slot.get_inner_rect(), 2, 4)
            board_surface.blit(pygame.transform.scale(self._card_texture, slot.get_inner_rect().size), slot.get_inner_rect())

        for slot in self.hand_zone.slots_components:
            if(slot.get_inner_rect().collidepoint(mouse_pos.x, mouse_pos.y)):
                pygame.draw.rect(board_surface, "Green", slot.get_inner_rect(), border_radius=4)

                if(click):
                    self._show_msg_box(slot, flipped)

            board_surface.blit(pygame.transform.scale(self._card_texture, slot.get_inner_rect().size), slot.get_inner_rect())

        pygame.draw.circle(board_surface, "red", mouse_pos, 8, 2)

        return pygame.transform.rotate(board_surface, 180) if flipped else board_surface

    def _show_msg_box(self, slot: SlotComponent, flipped: bool) -> None:

        position = pygame.Vector2(slot.get_rect().center) + pygame.Vector2(self.get_rect().topleft)

        if(flipped):
            board_center = self.get_rect().center
            position = (position - board_center).rotate(180) + board_center

        self._msg_box.show(MsgBoxConfiguration(
            UIComponent(pygame.Rect(0,0,64,64)),
            position = position
        ))

    def _initialize_component(self):
        margin = pygame.Vector2(6, 6)
        card_size = pygame.Vector2((185, 256))
        board_space_between = 32

        #TODO add Grave add Deck

        self.battle_zone = BattleZone(pygame.Rect(
            0,0,
            pygame.Vector2(self.get_rect().size).x * 0.64,
            pygame.Vector2(self.get_rect().size).y * 0.55
        ), margin)

        self.support_zone = SupportZone(pygame.Rect(
            0, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.get_rect().size).x * 0.28,
            pygame.Vector2(self.get_rect().size).y * 0.45,
        ), margin)
        self.hand_zone = HandZone(pygame.Rect(
            self.support_zone.get_rect().right, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.get_rect().size).x * 0.72,
            pygame.Vector2(self.get_rect().size).y * 0.45
        ), margin)