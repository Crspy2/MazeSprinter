from Player import *
from Goal import *
from Wall import Wall

class Controller:
    """ Receives and acts upon messages received from the other computer. """
   
    def __init__(self, zombie, screen, wall_controller, goal, player):
        self.zombie = zombie 
        self.screen = screen
        self.wall_controller = wall_controller
        self.goal = goal
        self.player = player
        
    # noinspection PyUnusedLocal
    def act_on_message_received(self, message, sender_id):
        """
        Moves this Controller's "zombie" Player to the position
        that was sent by the other computer.
        Parameters:
          -- message: Must be a string that represents two non-negative
                      integers separated by one or more spaces, e.g. "100 38"
          -- sender_id: The number of the computer sending the message
                        (unused by this method)
          :type message:   str
          :type sender_id: int
        """

        #print(message)

        x = float(message.split()[0])
        y = float(message.split()[1])
        
        self.map_num = int(message.split()[2])
        self.goal_num = int(message.split()[3])

        self.force_x = int(message.split()[5])
        self.force_y = int(message.split()[6])

        if self.map_num != -1 and self.goal_num != -1:
            sync_generation(self.map_num, self.goal_num, self.wall_controller, self.goal, self.player)
            
        if self.force_x != -1 and self.force_y != -1:
            self.player.move_to(self.force_x, self.force_y)
            print('Zombie Pos Reset')


        self.zombie.move_to(x, y)

        self.zombie.score = int(message.split()[4])


        
        

def sync_generation(map_number, goal_number, wall_controller, goal, player):
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