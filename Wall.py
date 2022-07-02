import pygame

class Wall:
    def __init__(self,screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collider=pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (169, 169, 169)

    def draw(self):
        pygame.draw.rect(self.screen, (self.color), (self.x, self.y, self.width, self.height))
