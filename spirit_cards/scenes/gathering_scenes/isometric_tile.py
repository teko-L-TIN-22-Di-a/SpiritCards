import pygame
from dataclasses import dataclass

@dataclass
class IsometricTile:
    position: pygame.Vector3
    accessible: bool = True