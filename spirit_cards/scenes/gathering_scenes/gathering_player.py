
import pygame
from spirit_cards.core.context import Context
from spirit_cards.core.entity_manager import EntityManager
from spirit_cards.scenes.gathering_scenes.gathering_services import GatheringServices
from spirit_cards.scenes.gathering_scenes.isometric_entity import IsometricEntity


class GatheringPlayer(IsometricEntity):
    def __init__(self, context: Context):
        # TODO pass actual player surface
        super().__init__(pygame.Vector3(0,1,0))

    def update(self, delta: float) -> None:

        speed = 0.1
        pressed_keys = pygame.key.get_pressed()
        temp_movement = pygame.Vector3(0,0,0)
        
        if(pressed_keys[pygame.K_UP]):
            temp_movement.z -= 1
        if(pressed_keys[pygame.K_DOWN]):
            temp_movement.z += 1
        if(pressed_keys[pygame.K_LEFT]):
            temp_movement.x -= 1
        if(pressed_keys[pygame.K_RIGHT]):
            temp_movement.x += 1

        if(temp_movement.length() != 0):
            # Rotate movement from isometric towards camera to make it less awkward.
            self.position += temp_movement.rotate_y(45).normalize() * speed
            

    def cleanup(self) -> None:
        pass