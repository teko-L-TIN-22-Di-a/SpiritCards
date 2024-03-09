
import pygame
from spirit_cards.asset_map import AssetMap
from spirit_cards.core.context import Context
from spirit_cards.core.entity import Entity
from spirit_cards.pygame_extension.pygame_services import PygameServices
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

    def get_pos(self):
        return self.bounds.topleft

    def update(self, delta: float) -> None:
         # TODO Follow player instead of doing whatever this is.
        speed = 10

        pressed_keys = pygame.key.get_pressed()
        if(pressed_keys[pygame.K_w]):
            self.bounds.y += speed
        if(pressed_keys[pygame.K_s]):
            self.bounds.y -= speed
        if(pressed_keys[pygame.K_a]):
            self.bounds.x += speed
        if(pressed_keys[pygame.K_d]):
            self.bounds.x -= speed