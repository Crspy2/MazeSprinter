import pygame

class Player:
    def __init__(self, screen, x, y, image_file, map_num, goal_num, type):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.vx = 0
        self.vy = 0
        self.movespeed = 3
        self.just_happened = False
        self.type = type

        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.lastUsed = 2

        self.coords_check = 1
        self.coords = []
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)

        self.top_collision = False
        self.top_right_collision = False
        self.right_collision = False
        self.bottom_collision = False

        self.score = -1

        self.map_number = map_num
        self.goal_number = goal_num

        self.walk_count = 0
        self.Up = False
        self.Down = False
        self.Left = False
        self.Right = False

        #self.screen.blit(self.image, (self.x - 16, self.y - 16))

        self.walk_up = [(pygame.image.load("Sprites/Up/Up1.png")), (pygame.image.load("Sprites/Up/Up2.png"))]
        self.walk_down = [(pygame.image.load("Sprites/Down/Down1.png")), (pygame.image.load("Sprites/Down/Down2.png"))]
        self.walk_left = [(pygame.image.load("Sprites/Left/Left1.png")), (pygame.image.load("Sprites/Left/Left2.png"))]
        self.walk_right = [(pygame.image.load("Sprites/Right/Right1.png")), (pygame.image.load("Sprites/Right/Right2.png"))]

        self.walk_up_left = [(pygame.image.load("Sprites/Up-Left/Up-Left1.png")), (pygame.image.load("Sprites/Up-Left/Up-Left2.png"))]
        self.walk_up_right = [(pygame.image.load("Sprites/Up-Right/Up-Right1.png")), (pygame.image.load("Sprites/Up-Right/Up-Right2.png"))]
        self.walk_down_left = [(pygame.image.load("Sprites/Down-Left/Down-Left1.png")), (pygame.image.load("Sprites/Down-Left/Down-Left2.png"))]
        self.walk_down_right = [(pygame.image.load("Sprites/Down-Right/Down-Right1.png")), (pygame.image.load("Sprites/Down-Right/Down-Right2.png"))]

        self.idleUP = [(pygame.image.load("Sprites/Up/UpIdle1.png")), (pygame.image.load("Sprites/Up/UpIdle2.png"))]
        self.idleDOWN = [(pygame.image.load("Sprites/Down/DownIdle1.png")), (pygame.image.load("Sprites/Down/DownIdle2.png"))]
        self.idleLEFT = [(pygame.image.load("Sprites/Left/LeftIdle1.png")), (pygame.image.load("Sprites/Left/LeftIdle2.png"))]
        self.idleRIGHT = [(pygame.image.load("Sprites/Right/RightIdle1.png")), (pygame.image.load("Sprites/Right/RightIdle2.png"))]

        index = 0
        #Straight Directions
        for image in self.walk_up: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_up[index]=image
            index +=1
        index=0
        
        for image in self.walk_down: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_down[index]=image
            index +=1
        index=0

        for image in self.walk_left: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_left[index]=image
            index +=1
        index=0
        
        for image in self.walk_right: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_right[index]=image
            index +=1
        index=0
        
        # Diagonals
        for image in self.walk_up_left: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_up_left[index]=image
            index +=1
        index=0

        for image in self.walk_up_right: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_up_right[index]=image
            index +=1
        index=0
        
        for image in self.walk_down_left: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_down_left[index]=image
            index +=1
        index=0

        for image in self.walk_down_right: 
            image = pygame.transform.scale(image, (60, 60))
            self.walk_down_right[index]=image
            index +=1
        index=0

        # Idles
        for image in self.idleUP: 
            image = pygame.transform.scale(image, (60, 60))
            self.idleUP[index]=image
            index +=1
        index=0

        for image in self.idleDOWN: 
            image = pygame.transform.scale(image, (60, 60))
            self.idleDOWN[index]=image
            index +=1
        index=0

        for image in self.idleLEFT: 
            image = pygame.transform.scale(image, (60, 60))
            self.idleLEFT[index]=image
            index +=1
        index=0

        for image in self.idleRIGHT: 
            image = pygame.transform.scale(image, (60, 60))
            self.idleRIGHT[index]=image
            index +=1
        index=0


    def move_by_keys(self, up, down, left, right, up2, down2, left2, right2):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[up] or pressedKeys[up2]:
            self.vy = -self.movespeed
            self.Up = True
            self.Down = False
        elif pressedKeys[down]  or pressedKeys[down2]:
            self.vy = self.movespeed
            self.Up = False
            self.Down = True
        else: 
            self.vy = 0
            self.Up = False
            self.Down = False
        
        if pressedKeys[left] or pressedKeys[left2]:
            self.vx = -self.movespeed
            self.Left = True
            self.Right = False
        elif pressedKeys[right] or pressedKeys[right2]:
            self.vx = self.movespeed
            self.Left = False
            self.Right = True
        else: 
            self.vx = 0
            self.Left = False
            self.Right = False
        
        self.x += self.vx
        self.y += self.vy
        self.sender.send_message(f"{self.x} {self.y} {-1} {-1} {self.score} {-1} {-1}")


    def draw(self):
        if self.walk_count + 1 >= 24:
            self.walk_count = 0

        if self.coords_check == True:
            self.coords = [self.x, self.y]
            self.coords_check = False
            self.just_happened = True

        if self.coords_check == False and self.just_happened == False:
            self.coords_check = True 

        
        # (self.coords[0] > self.x or coords[0] < self.x or self.coords[1] > self.y or self.coords[1] < self.y)

        # Diagonal animations
        if self.Up and self.Left:# or (self.type == "Zombie" and self.coords[1] > self.y and self.coords[0] > self.x):
            self.screen.blit(self.walk_up_left[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 1
        elif self.Up and self.Right:# or (self.type == "Zombie" and self.coords[1] > self.y and self.coords[0] < self.x):
            self.screen.blit(self.walk_up_right[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 1
        elif self.Down and self.Left:# or (self.type == "Zombie" and self.coords[1] < self.y and self.coords[0] > self.x):
            self.screen.blit(self.walk_down_left[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 2
        elif self.Down and self.Right:# or (self.type == "Zombie" and self.coords[1] < self.y and self.coords[0] < self.x):
            self.screen.blit(self.walk_down_right[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 2
        
        # Directional animations
        elif self.Up:# or (self.type == "Zombie" and self.coords[1] < self.y):
            self.screen.blit(self.walk_up[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 1
        elif self.Down:# or (self.type == "Zombie" and self.coords[1] > self.y):
            self.screen.blit(self.walk_down[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 2
        elif self.Left:# or (self.type == "Zombie" and self.coords[1] < self.x):
            self.screen.blit(self.walk_left[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 3
        elif self.Right:# or (self.type == "Zombie" and self.coords[1] > self.x):
            self.screen.blit(self.walk_right[self.walk_count // 12], (self.x - 16, self.y - 16))
            self.walk_count += 1
            self.lastUsed = 4
        
        # Idle animations
        else:
            #self.screen.blit(self.idleDOWN[self.walk_count // 12], (self.x - 16, self.y - 16))
            if self.lastUsed == 1:
                self.screen.blit(self.idleUP[self.walk_count // 12], (self.x - 16, self.y - 16))
            if self.lastUsed == 2:
                self.screen.blit(self.idleDOWN[self.walk_count // 12], (self.x - 16, self.y - 16))
            if self.lastUsed == 3:
                self.screen.blit(self.idleLEFT[self.walk_count // 12], (self.x - 16, self.y - 16))
            if self.lastUsed == 4:
                self.screen.blit(self.idleRIGHT[self.walk_count // 12], (self.x - 16, self.y - 16))

        self.just_happened = False
    def set_sender(self, sender):
        self.sender = sender

    def collide(self, collide_object):
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collider_top = pygame.Rect(self.x, self.y, self.width, 5)
        self.collider_bot = pygame.Rect(self.x, self.y+self.height-5, self.width, 5)
        self.collider_left = pygame.Rect(self.x, self.y, 5, self.height)
        self.collider_right = pygame.Rect(self.x+self.width-5, self.y, 5, self.height)
        
        self.top_collide = self.collider_top.colliderect(collide_object.collider)
        self.bot_collide = self.collider_bot.colliderect(collide_object.collider)
        self.left_collide = self.collider_left.colliderect(collide_object.collider)
        self.right_collide = self.collider_right.colliderect(collide_object.collider)

        if self.top_collide and not self.bot_collide:
            self.y = collide_object.y+collide_object.height

        if self.bot_collide and not self.top_collide:
            self.y = collide_object.y-self.height
        
        if self.left_collide and not self.right_collide:
            self.x = collide_object.x+collide_object.width

        if self.right_collide and not self.left_collide:
            self.x = collide_object.x-self.width
        
    def goal(self, object):
        if self.collider.colliderect(object.collider):
            return True

    def move_to(self, x, y):
        """ Moves this Player to the given position. """
        self.x = x
        self.y = y
            






        