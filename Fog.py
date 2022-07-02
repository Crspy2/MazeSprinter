import pygame

class Fog:
    def __init__(self, screen):
        self.screen = screen
        self.enable = True
        self.fog_img = pygame.image.load("FogOfWar.png")


    def draw(self, player):
        # Player X Coordinate
        playerCenterX = player.x + player.width // 2
        # Player Y Coordinate
        playerCenterY = player.y + player.height // 2

        ImageCenterX = playerCenterX - self.fog_img.get_width() // 2
        ImageCenterY = playerCenterY - self.fog_img.get_height() // 2

        if self.enable:
            pygame.draw.rect(self.screen, (0, 0, 0, 255), (0, 0, playerCenterX - 100, self.screen.get_height())) # Left Rectangle
            pygame.draw.rect(self.screen, (0, 0, 0, 255), (0, 0, self.screen.get_width(), playerCenterY - 100)) # Top Rectangle
            pygame.draw.rect(self.screen, (0, 0, 0, 255), (playerCenterX + 100, 0,  self.screen.get_width() - playerCenterX - 50, self.screen.get_height())) # Right Rectangle
            pygame.draw.rect(self.screen, (0, 0, 0, 255), (0, playerCenterY + 100,  self.screen.get_width(), self.screen.get_height() - playerCenterY - 50)) # Bottom Rectangle
            self.screen.blit(self.fog_img, (ImageCenterX, ImageCenterY))