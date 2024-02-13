import pygame

def main():
    pygame.init()
    surface = pygame.display.set_mode((1280, 720))
    icon = pygame.Surface((32, 32))
    icon.fill(pygame.Color(0,0,0))

    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    running = True

    sheet = pygame.image.load("assets/link_sprite_sheet.png")
    rect = sheet.get_rect()
    bounding_rect = pygame.rect.Rect(0, 0, 92, 112)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill("black")
        surface.blit(sheet, rect, bounding_rect)

        pygame.display.update()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()