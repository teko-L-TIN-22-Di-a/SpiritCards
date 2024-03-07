
import pygame
from spirit_cards.core.context import Context
from spirit_cards.core.entity_manager import EntityManager
from spirit_cards.scenes.gathering_scenes.gathering_services import GatheringServices
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import GlobalServices
from spirit_cards.asset_map import AssetMap
from spirit_cards.scenes.gathering_scenes.isometric_entity import IsometricEntity


class GatheringPlayer(IsometricEntity):
    def __init__(self, context: Context):
        super().__init__(pygame.Vector3(0,1,0))
        asset_manager: AssetManager = context.get_service(GlobalServices.ASSET_MANAGER)
        self.surface = asset_manager.get_image(AssetMap.TEST_SPRITE_PLAYER)
        self.offset = pygame.Vector2(self.surface.get_size()) / -2
        print(self.position)

    def update(self, delta: float) -> None:

        speed = 0.05
        pressed_keys = pygame.key.get_pressed()
        temp_movement = pygame.Vector3(0,0,0)
        
        if(pressed_keys[pygame.K_UP]):
            temp_movement.z -= 1
        if(pressed_keys[pygame.K_DOWN]):
            temp_movement.z += 1
        if(pressed_keys[pygame.K_LEFT]):
            temp_movement.x -= 1
            if self.direction:
                self.direction = False
                self.flip_surface()
        if(pressed_keys[pygame.K_RIGHT]):
            temp_movement.x += 1
            if not self.direction:
                self.direction = True
                self.flip_surface()

        if(temp_movement.length() != 0):
            # Rotate movement from isometric towards camera to make it less awkward.
            position = self.position + temp_movement.rotate_y(45).normalize() * speed
            if self.bounds.collidepoint(position.x, position.z) :
                self.position = position
                print(self.bounds.collidepoint(position.x, position.z))
                print(position)

    def check_colliders(self, position: pygame.Vector3):
        for collider in self.colliders:
            if collider.collidepoint(position.x, position.z):
                return True
        return False

    def precise_collision(self):
        self.bounds.get

    def cleanup(self) -> None:
        pass