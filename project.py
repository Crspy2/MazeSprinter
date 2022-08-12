import pygame
import sys
import time
import random

import simpleMQTT as mq
from Controller import Controller

from Wall import Wall
from Player import Player
from Goal import Goal
from Wall_Controller import Wall_Controller
from Fog import Fog

ZOMBIECOUNT = 1

def generate_map(map_number, goal_number, wall_controller, goal, player):
    if map_number == 1:
        wall_controller.wall_info =  wall_controller.wall_info_1
    else: 
        wall_controller.wall_info =  wall_controller.wall_info_2
    
    wall_controller.walls = []
    for wall in wall_controller.wall_info:
        wall_controller.walls.append(Wall(wall_controller.screen, wall[0], wall[1], wall[2], wall[3]))
    wall_controller.draw(player)
    
    goal.x = goal.positions[goal_number][0]
    goal.y = goal.positions[goal_number][1]

    goal.goalPosition = pygame.Rect(goal.x, goal.y, 60, 60)
    goal.draw()

    


def main(who_am_i):

    pygame.init()

    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()

    bg_image = pygame.image.load("Brown-Wooden-Table-Background-by-Anilakkus.jpg")
    bg_image = pygame.transform.scale(bg_image, (900, 600))

    fog = Fog(screen)
    if pygame.key.get_pressed()[pygame.K_f]:
        fog.enable = fog.enable
    
    # players = [player, zombie]
    wall_controller = Wall_Controller(screen)
    goal = Goal(screen)
    multiplayer = False
    start_time = time.time()

    pygame.display.set_caption("Find the goal!")
    best_sec = 0
    best_mins = best_sec // 60
    best_sec = best_sec % 60
    best_mins = best_mins % 60


    
    map_number = random.randint(0, 1)
    if map_number == 0:
        goal_number = random.randint(5, 11)
    else:
        goal_number = random.randint(0, 4)
    #override
    goal_number = 12
    
    player = Player(screen, 10, 10, "P1.png", map_number, goal_number, "Player")
    
    zombie = Player(screen, -100, -100, "P2.png", map_number, goal_number, "Zombie")
    
    sender = mq.Sender(who_am_i)
    controller = Controller(zombie, screen, wall_controller, goal, player)
    receiver = mq.Receiver(controller)
    player.set_sender(sender)

    generate_map(map_number, goal_number, wall_controller, goal, player)

    first_gen = 1

    pygame.mixer.music.load("soundtrack_Wilnado - Spaced Out Guitars (1).mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)


    # Game Loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():

            pressedKeys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                clickPos = event.pos
                print(clickPos)
            # if event.type == pygame.KEYDOWN and pressedKeys[pygame.K_f]:
            #     fog.enable = not fog.enable
            #     print(f"Fog status set to {fog.enable}")
            if event.type == pygame.KEYDOWN and pressedKeys[pygame.K_m]:
                multiplayer = not multiplayer
                if multiplayer:
                    mq.activate(lobby_id, sender, receiver)

        screen.fill((255, 255, 255))
        screen.blit(bg_image, (0, 0), )

        wall_controller.draw(player)
        goal.draw()

        player.draw()
        player.move_by_keys(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        
        # Check if multiplayer is disabled
        if not multiplayer:
            fog.draw(player)
            
            end_time = time.time()
            sec = end_time - start_time
            mins = sec // 60
            sec = sec % 60
            mins = mins % 60

            pygame.display.set_caption(f"Current Time: {int(mins):02d}:{int(sec):02d}, Best Time: {int(best_mins):02d}:{int(best_sec):02d}")

            if player.goal(goal):
                map_number = random.randint(0, 1)
                if map_number == 0:
                    goal_number = random.randint(5, 11)
                else:
                    goal_number = random.randint(0, 4)
                generate_map(map_number, goal_number, wall_controller, goal, player)

                player.x = 10
                player.y = 10

                if best_sec == 0 or best_sec > sec:
                    best_sec = int(sec)
                    best_mins = best_sec // 60
                    best_sec = best_sec % 60
                    best_mins = best_mins % 60

                start_time = time.time()
        # Check if multiplayer is enabled
        if multiplayer:
            if first_gen == 1:
                map_number = random.randint(0, 1)
                if map_number == 0:
                    goal_number = random.randint(5, 11)
                else:
                    goal_number = random.randint(0, 4)
                
                goal_number = 12
                generate_map(map_number, goal_number, wall_controller, goal, player)
                
                player.x = 10
                player.y = 10
                first_gen += 1

            pygame.display.set_caption(f"P1: {player.score} | P2: {zombie.score}")

            zombie.draw()
            if player.goal(goal):
                map_number = random.randint(0, 1)
                if map_number == 0:
                    goal_number = random.randint(5, 11)
                else:
                    goal_number = random.randint(0, 4)
                generate_map(map_number, goal_number, wall_controller, goal, player)

                force_x = 10
                force_y = 10

                player.score += 1
              
                player.sender.send_message(f"{player.x} {player.y} {map_number} {goal_number} {player.score} {force_x} {force_y}")
                
                player.x = 10
                player.y = 10
            fog.draw(player)

        


        pygame.display.update()



if __name__ == '__main__':
    lobby_id = str(input("Please enter your lobby ID (must be the same as the person you want to play with): "))
    player_id = int(input("Please enter your Player ID (It must be either 1 or 2 and cannot be the same as the person you want to play with): "))
    main(player_id)