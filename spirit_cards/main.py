import pygame

from .core.engine import Engine
from .constants import *

from .example_code.example_scene import ExampleScene

def main():
    running = True

    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((1280, 720))
    
    icon = pygame.Surface((32, 32))
    icon.fill(pygame.Color(0,0,0))
    
    # For testing
    sheet = pygame.image.load("assets/link_sprite_sheet.png")
    rect = sheet.get_rect()
    bounding_rect = pygame.rect.Rect(0, 0, 92, 112)
    # remove above code

    engine = Engine({
        PYGAME_SURFACE: surface
    })
    # Todo add proper scene initialisation
    engine.load_scene(ExampleScene(engine.context))

    try:
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # TODO Add proper delta
            engine.process(1)

            # For testing
            surface.fill("black")
            surface.blit(sheet, rect, bounding_rect)
            # remove above code

            pygame.display.update()
            pygame.display.flip()

            clock.tick(60)
    except:
        print("Game ungracefully stopped because of an exception")
        raise

    pygame.quit()

if __name__ == "__main__":
    main()