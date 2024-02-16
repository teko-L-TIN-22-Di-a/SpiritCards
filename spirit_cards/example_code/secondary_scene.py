import pygame

from spirit_cards.pygame_extension.pygame_services import *
from spirit_cards.core.scene import Scene

class SecondaryScene(Scene):

    _surface: pygame.Surface
    _font: pygame.font.Font

    def init(self, parameters: any = None) -> None:
        self._surface = self.context.get_service(SCREEN_SURFACE)
        self._font = pygame.font.SysFont('timesnewroman',  24)

    def process(self, delta: int) -> None:
        
        self._surface.fill(pygame.Color(50,50,50))
        text = self._font.render("Heyo", True, "Black")
        self._surface.blit(text, (4, 4))


    def cleanup(self) -> None:
        pass