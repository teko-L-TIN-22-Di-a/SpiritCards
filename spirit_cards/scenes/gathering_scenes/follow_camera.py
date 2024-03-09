
import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.pygame_services import PygameServices
from spirit_cards.scenes.gathering_scenes.gathering_services import GatheringServices
from spirit_cards.scenes.gathering_scenes.gathering_player import GatheringPlayer
from spirit_cards.scenes.gathering_scenes.isometric_tile_map import IsometricTileMap
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices


class FollowCamera(Entity):

    TAG = "camera"

    bounds: pygame.Rect

    def __init__(self, context: Context):
        screen: pygame.Surface = context.get_service(PygameServices.SCREEN_SURFACE)
        screen_size = pygame.Vector2(screen.get_size())
        self.bounds = pygame.Rect(0,0, screen_size.x, screen_size.y)
        self._entity_manager = context.get_service(GatheringServices.ENTITY_MANAGER)

    def get_pos(self):
        return self.bounds.topleft

    def update(self, delta: float) -> None:
         # TODO Follow player instead of doing whatever this is.
        speed = 10

        player_entity: GatheringPlayer = self._entity_manager.get_filtered(GatheringPlayer.TAG)[0]

        self.bounds.y -= player_entity.camera_movement.y
        self.bounds.x -= player_entity.camera_movement.x

        pressed_keys = pygame.key.get_pressed()
        if(pressed_keys[pygame.K_w]):
            self.bounds.y += speed
        if(pressed_keys[pygame.K_s]):
            self.bounds.y -= speed
        if(pressed_keys[pygame.K_a]):
            self.bounds.x += speed
        if(pressed_keys[pygame.K_d]):
            self.bounds.x -= speed

    def move(self, movement: pygame.Vector2):
        self.bounds.centerx += movement.x
        self.bounds.centery += movement.y