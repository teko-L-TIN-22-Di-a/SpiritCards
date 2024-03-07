
from dataclasses import dataclass
from typing import Callable
import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.action_instance import ActionInstance
from spirit_cards.card_engine.board_constants import BoardConstants
from spirit_cards.card_engine.card_engine import CardEngine
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.card_engine.slot import Slot
from spirit_cards.core.context import Context
from spirit_cards.pygame_extension.event_buffer import EventBuffer
from spirit_cards.pygame_extension.gui.button import Button, ButtonConfig
from spirit_cards.pygame_extension.gui.button_container import ButtonContainer
from spirit_cards.pygame_extension.gui.msg_box import MsgBox, MsgBoxConfiguration
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.encounter_scenes.board_components.battle_zone import BattleZone
from spirit_cards.scenes.encounter_scenes.board_components.card_viewer import CardViewer
from spirit_cards.scenes.encounter_scenes.board_components.hand_zone import HandZone
from spirit_cards.scenes.encounter_scenes.board_components.slot_component import SlotComponent
from spirit_cards.scenes.encounter_scenes.board_components.support_zone import SupportZone
from spirit_cards.scenes.encounter_scenes.encounter_services import EncounterServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices
    
class BoardSide(UIComponent):

    _context: Context
    _card_engine: CardEngine
    _msg_box: MsgBox
    _event_buffer: EventBuffer

    _card_textures: dict[str, pygame.Surface]
    _font: pygame.font.Font

    player: CardPlayer
    following_player: CardPlayer

    score_component: UIComponent

    battle_zone: BattleZone
    support_zone: SupportZone
    hand_zone: HandZone

    on_slot_click: Callable[[tuple[Action, Slot]], None]

    def __init__(self, rect: pygame.Rect, player: CardPlayer, following_player: CardPlayer, context: Context):
        super().__init__(rect)

        self.following_player = following_player
        self.player = player
        self._context = context
        self._card_engine = context.get_service(EncounterServices.CARD_ENGINE)
        self._msg_box = self._context.get_service(EncounterServices.MESSAGE_BOX)
        self._event_buffer = context.get_service(PygameServices.EVENT_BUFFER)

        asset_manager: AssetManager = self._context.get_service(GlobalServices.ASSET_MANAGER)

        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)

        # TODO clean this up
        self._card_textures = {
            AssetMap.TEST_CARD: asset_manager.get_image(AssetMap.TEST_CARD),
            AssetMap.TEST_CARD2: asset_manager.get_image(AssetMap.TEST_CARD2),
            AssetMap.TEST_CARD3: asset_manager.get_image(AssetMap.TEST_CARD3),
            AssetMap.TEST_CARD4: asset_manager.get_image(AssetMap.TEST_CARD4)
        }

        self._initialize_component()

    def update(self) -> pygame.Surface:
        self.hand_zone.update()

    def draw_to_surface(self, mouse_pos: pygame.Vector2, flipped: bool = False, hide_hand: bool = False) -> pygame.Surface:

        if(flipped):
            board_center = self.get_rect().center
            mouse_pos = (mouse_pos - board_center).rotate(180) + board_center

        size = pygame.Vector2(self.get_rect().size)
        board_surface = pygame.Surface(size)
        
        pygame.draw.rect(board_surface, "#092B40", pygame.Rect(0,0,size.x, size.y))
        pygame.draw.rect(board_surface, "#405F73", self.battle_zone.get_inner_rect(), 2, 4)
        pygame.draw.rect(board_surface, "#405F73", self.support_zone.get_inner_rect(), 2, 4)
        pygame.draw.rect(board_surface, "#405F73", self.hand_zone.get_inner_rect(), border_radius=4)

        self._draw_slots(board_surface, mouse_pos, flipped, hide_hand)        
        self._draw_player_info(board_surface)

        pygame.draw.circle(board_surface, "red", mouse_pos, 8, 2)

        return pygame.transform.rotate(board_surface, 180) if flipped else board_surface

    def _draw_player_info(self, board_surface: pygame.Surface):
        text = self._font.render(f"HP: {self.player.health} MANA: {self.player.resources}", True, "White")
        board_surface.blit(text, self.score_component.get_inner_rect())

    def _draw_slots(self, board_surface: pygame.Surface, mouse_pos: pygame.Vector2, flipped: bool, hide_hand: bool = False):

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
                    if(slot.slot.active):
                        self._card_engine.round_state.select_slot(slot.slot)
                    else:
                        self._show_actions(slot, flipped)
                else:
                    self._show_card(slot, flipped)

            pygame.draw.rect(board_surface, "#5A798C", slot.get_inner_rect(), 2, 4)
            if(slot.slot.card is not None):
                texture = self._card_textures[slot.slot.card.asset_key]
                board_surface.blit(pygame.transform.scale(texture, slot.get_inner_rect().size), slot.get_inner_rect())

            if(slot.slot.active):
                pygame.draw.rect(board_surface, "yellow", slot.get_inner_rect(), 2, 4)

        for slot in self.hand_zone.slots_components:
            if(slot.get_inner_rect().collidepoint(mouse_pos.x, mouse_pos.y)):
                pygame.draw.rect(board_surface, "Green", slot.get_inner_rect(), border_radius=4)

                if(click):
                    self._show_actions(slot, flipped)
                else:
                    self._show_card(slot, flipped)

            if(slot.slot.card is not None):

                if(hide_hand):
                    pygame.draw.rect(board_surface, "Black", slot.get_inner_rect(), border_radius=4)
                    continue

                texture = self._card_textures[slot.slot.card.asset_key]
                board_surface.blit(pygame.transform.scale(texture, slot.get_inner_rect().size), slot.get_inner_rect())


    def _show_actions(self, slot: SlotComponent, flipped: bool) -> None:

        position = pygame.Vector2(slot.get_rect().center) + pygame.Vector2(self.get_rect().topleft)

        if(flipped):
            board_center = self.get_rect().center
            position = (position - board_center).rotate(180) + board_center

        buttons: list[Button] = []
        for action in self._card_engine.round_state.get_legal_actions(slot.slot, self.following_player):
            buttons.append(Button(self._context, ButtonConfig((action, slot.slot), action.key, pygame.Vector2(224, 32), self.on_slot_click)))

        if(len(buttons) <= 0):
            return

        self._msg_box.show(MsgBoxConfiguration(
            ButtonContainer(buttons),
            position = position
        ))

    def _show_card(self, slot: SlotComponent, flipped: bool) -> None:
        if(slot.slot.card is None or not pygame.key.get_pressed()[pygame.K_LALT]):
            return

        texture = self._card_textures[slot.slot.card.asset_key]

        self._msg_box.show(MsgBoxConfiguration(
            CardViewer(texture)
        ))

    def _initialize_component(self):
        margin = pygame.Vector2(6, 6)

        #TODO add Grave add Deck

        self.battle_zone = BattleZone(self.player, pygame.Rect(
            0,0,
            pygame.Vector2(self.get_rect().size).x * 0.64,
            pygame.Vector2(self.get_rect().size).y * 0.55
        ), margin)

        self.support_zone = SupportZone(self.player, pygame.Rect(
            0, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.get_rect().size).x * 0.28,
            pygame.Vector2(self.get_rect().size).y * 0.45,
        ), margin)
        self.hand_zone = HandZone(self.player, pygame.Rect(
            self.support_zone.get_rect().right, self.battle_zone.get_rect().bottom,
            pygame.Vector2(self.get_rect().size).x * 0.72,
            pygame.Vector2(self.get_rect().size).y * 0.45
        ), margin)

        self.score_component = UIComponent(pygame.Rect(
            self.battle_zone.get_rect().right, 0,
            242, 32
        ), pygame.Vector2(4,4))