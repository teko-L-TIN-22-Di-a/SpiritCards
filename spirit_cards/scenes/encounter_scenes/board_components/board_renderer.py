import pygame
from dataclasses import dataclass
from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.action_instance import ActionInstance
from spirit_cards.card_engine.card_engine import CardEngine
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.card_engine.round_state import RoundState

from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.gui.button import Button, ButtonConfig
from spirit_cards.pygame_extension.gui.button_container import ButtonContainer
from spirit_cards.pygame_extension.gui.ui_component import UIComponent
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.encounter_scenes.board_components.board_side import BoardSide
from spirit_cards.scenes.encounter_scenes.encounter_services import EncounterServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices

class BoardRenderer(Entity):

    BOARD_SPACE_BETWEEN = 32

    _context: Context
    _surface: pygame.surface.Surface
    _card_engine: CardEngine

    following_player: CardPlayer

    player1_side: BoardSide # Always also the following_player
    player2_side: BoardSide
    middle_component: UIComponent

    def __init__(self, following_player: CardPlayer, context: Context):
        self._context = context
        self.following_player = following_player
        self._surface = context.get_service(PygameServices.SCREEN_SURFACE)
        self._card_engine = context.get_service(EncounterServices.CARD_ENGINE)
        asset_manager: AssetManager = self._context.get_service(GlobalServices.ASSET_MANAGER)

        self._font = asset_manager.get_font(AssetMap.MONTSERRAT_24)

        self._initialize_components()

    def update(self, delta: float) -> None:
        self.player1_side.update()
        self.player1_side.update()

    def render(self, delta: float) -> None:

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        player2_mouse_pos = mouse_pos - pygame.Vector2(self.player2_side.get_local_rect().topleft)
        player1_mouse_pos = mouse_pos - pygame.Vector2(self.player1_side.get_local_rect().topleft)

        self._surface.blit(self.player2_side.draw_to_surface(player2_mouse_pos, True), self.player2_side.get_rect())
        self._surface.blit(self.player1_side.draw_to_surface(player1_mouse_pos), self.player1_side.get_rect())
        
        self._render_round_info()
        self._render_round_actions()

    def _render_round_actions(self):
        buttons = []
        for action in self._card_engine.round_state.get_actions(self.following_player):
            buttons.append(Button(self._context, ButtonConfig(
                action,
                action.key,
                pygame.Vector2(156, 32),
                self._on_click
            )))

        if(len(buttons) <= 0):
            return

        action_container = ButtonContainer(buttons)
        container_size = pygame.Vector2(action_container.get_rect().size)
        position = pygame.Vector2(self.player1_side.get_rect().topright)
        action_container.relative_to = UIComponent(
            pygame.Rect(
                position.x - container_size.x, position.y,
                0, 0
            )
        )
        action_container.update()
        
        self._surface.blit(action_container.get_surface(), action_container.get_pos())

    def _on_click(self, action: Action):
        print(f"Button with tag <{action}> was pressed")
        self._card_engine.round_state.buffer_action(ActionInstance(action, self.following_player, None))

    def _render_round_info(self):
        center = pygame.Vector2(self.middle_component.get_rect().center)
        curr_state: RoundState = self._card_engine.round_state.current_state
        text = f"{curr_state.current_phase} - Round {self._card_engine.board_context.round_count}"
        text_surface: pygame.Surface = self._font.render(text, True, "Black")
        self._surface.blit(text_surface, center - pygame.Vector2(text_surface.get_rect().center))

    def _initialize_components(self):
        screen_size = pygame.Vector2(self._surface.get_size())
        board_size = pygame.Vector2(
            screen_size.x,
            screen_size.y / 2 - BoardRenderer.BOARD_SPACE_BETWEEN / 2
        )

        board_context = self._card_engine.board_context
        player1 = board_context.player1 if board_context.player1 == self.following_player else board_context.player2
        player2 = board_context.player2 if board_context.player2 != self.following_player else board_context.player1

        self.player1_side = BoardSide(pygame.Rect(
            0,board_size.y + BoardRenderer.BOARD_SPACE_BETWEEN,
            board_size.x, board_size.y   
        ), player1, self._context)
        self.player2_side = BoardSide(pygame.Rect(
            0,0,
            board_size.x, board_size.y   
        ), player2, self._context)

        self.middle_component = UIComponent(pygame.Rect(
            0, self.player2_side.rect.bottom,
            screen_size.x, BoardRenderer.BOARD_SPACE_BETWEEN
        ))
        
