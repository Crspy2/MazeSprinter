import pygame

class Goal:
    def __init__(self, screen):
        
        self.screen = screen
        self.image_checkered = pygame.image.load("assets/Checkerboard.png")
        self.new_size = (60, 60)
        self.scaled_current_image = pygame.transform.scale(self.image_checkered, self.new_size)
        
        self.width = 60
        self.height = 60
        self.x = -100
        self.y = -100
        self.positions = [(600, 80), (460, 80), (760, 380), (500, 390), (70, 530),       (70, 530), (660, 10), (400, 260), (660, 120), (810, 530), (740, 530), (330, 530), (10,10)]

    def draw(self):
        self.collider = pygame.Rect(self.x, self.y, 60, 60)
        self.screen.blit(self.scaled_current_image, (self.x, self.y))



