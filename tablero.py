import pygame
import random
import time

"""This code is a basic implementation of the A* algorithm on a randomly generated game board using Pygame"""
class Window:
    """The Window function is the main class that handles all of Pygame's window and game logic"""
    def __init__(self) -> None:
        """__init__ initializes several variables and the draw_board function is called to generate the game board. The main loop then takes care of updating 
        the Pygame window and handling the game shutdown. In addition, there is a boolean attribute check, which is used to check if a new destination needs to be found."""
        pygame.init()
        pygame.display.set_caption("Practice 1")
        self.screen = pygame.display.set_mode((480, 480))
        self.check = True
        self.coord_destino = None
        self.walls = []
        self.open = []
        self.close = []
        self.tile_size = 60
        self.board_width = 8 * self.tile_size
        self.board_height = 8 * self.tile_size
        self.running = True
        self.draw_board()
        while self.running:
            if self.check:
                self.algoritm_a_prime()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()
        pygame.quit()

    def draw_board(self):
        """The draw_board function is used to generate the game board. First, the floor or walls are drawn based on the probability of a generated random value. 
        Then the edges of the board are drawn and a random destination is generated. The random source is then generated and added to the open list, which is used to 
        store the nodes to consider. Finally, pygame.display.update() is called to display the board in the Pygame window."""
        for row in range(8):
            for col in range(8):
                x = col * self.tile_size
                y = row * self.tile_size
                if random.randint(0, 5) == 5:
                    self.walls.append((col, row))
                    self.draw_floor_or_wall(color=(0, 0, 0),x=x,y=y)
                else:
                    self.draw_floor_or_wall(color=(0, 120, 0),x=x,y=y)
                # Esta linea dibuja los bordes del tablero
                self.open.append((col,row))
                self.draw_border(color=(0, 0, 0),x=x,y=y,border=1)

        # Con esto generamos el destino
        x_o = random.randint(0, 7)
        y_o = random.randint(0, 7)
        while (x_o, y_o) in self.walls:
            x_o = random.randint(0, 7)
            y_o = random.randint(0, 7)
        self.draw_circle(color=(139, 69, 19),x=x_o,y=y_o,diametre=20)
        self.coord_destino = (x_o, y_o)
        
        # # Con esto generamos el origen
        x_o = random.randint(0, 7)
        y_o = random.randint(0, 7)
        while (x_o, y_o) in self.walls or (x_o, y_o) == self.coord_destino:
            x_o = random.randint(0, 7)
            y_o = random.randint(0, 7)
        self.draw_circle(color=(255, 0, 0),x=x_o,y=y_o,diametre=20)        
        self.open.insert(0,(x_o, y_o))
        pygame.display.update()
        
    def algoritm_a_prime(self):
        """algoritm_a_prime is where the A* algorithm is implemented. You start by marking the source as closed and removing it from the open list. Then, a search range is 
        created around the current node, and the F-score of each node within the range is calculated. The F-score is calculated as the sum of the Manhattan distance from the 
        current node to the destination and the distance from the current node to the source. The path with the lowest F-score is considered the next current node. If the 
        current node is the destination, the total cost of the path is printed and the loop is terminated. If it is not the destination, it is marked as closed and added to the 
        list of fathers, lt_fathers. The create_range function is used to generate a search range around the current node, and draw_circle and draw_label are used to draw in the
        Pygame window."""
        self.check = False
        origen = self.open[0]
        self.close.append(origen)
        self.open.clear()
        self.draw_border(color=(0, 50, 150),x=origen[0]* self.tile_size,y=origen[1]*self.tile_size,border=2)
        lt_fathers = []
        while origen != self.coord_destino:
            time.sleep(2)
            x = origen[0]
            y = origen[1]
            list_lists = self.create_range(x,y)
            lt_x = list_lists[0]
            lt_y = list_lists[1]
            coord = None
            F = 9999
            for itemx in lt_x:
                for itemy in lt_y:
                    if ((x,y) == (itemx,itemy)) or (itemx, itemy) in self.close or (itemx, itemy) in self.walls:
                        pass
                    else:
                        if (itemx,itemy) == (x-1 , y-1) or (itemx,itemy) == (x+1 , y+1) or (itemx,itemy) == (x-1 , y+1) or (itemx,itemy) == (x+1 , y-1):
                                val = 14
                        else:
                                val = 10
                        self.close.append((itemx, itemy))
                        tmp = (abs(self.coord_destino[0]-itemx),abs(self.coord_destino[1]-itemy))
                        self.draw_circle(color=(0, 0, 255),x=itemx,y=itemy,diametre=5)
                        self.draw_label(text_size=15,x=itemx,y=itemy,mrg_x=15,mrg_y=18,text=(tmp[0]+tmp[1])*10)
                        if (itemx == self.coord_destino[0] and itemy == self.coord_destino[1]):
                            print(f"Coste de la llegada: {sum([elemento for elemento in lt_fathers])+((tmp[0]+tmp[1])*10)+val}")
                            coord = (itemx,itemy)
                            break
                        self.draw_label(text_size=15,x=itemx,y=itemy,mrg_x=-25,mrg_y=18,text=val)
                        self.draw_label(text_size=15,x=itemx,y=itemy,mrg_x=-25,mrg_y=-20,text=((tmp[0]+tmp[1])*10)+val)
                        if F > ((tmp[0]+tmp[1])*10)+val:
                            F = ((tmp[0]+tmp[1])*10)+val
                            coord = (itemx,itemy)
            lt_fathers.append(F)              
            pygame.draw.line(self.screen, (255, 255, 255), (origen[0] * self.tile_size + self.tile_size // 2, origen[1] * self.tile_size + self.tile_size // 2), (coord[0] * self.tile_size + self.tile_size // 2, coord[1] * self.tile_size + self.tile_size // 2),width=5)
            pygame.display.update()
            origen = coord
            self.draw_border(color=(0, 50, 150),x=coord[0]* self.tile_size,y=coord[1]*self.tile_size,border=2)
            if origen == self.coord_destino:
                break
        self.running=False 
        
    def create_range(self,x,y):
        lt_x = []
        lt_y = []
            
        if x == 0:
            lt_x = [x, x + 1]
        elif x == 8:
            lt_x = [x - 1, x]
        else:
            lt_x = [x - 1, x, x + 1]
        if y == 0:
                lt_y = [y, y + 1]
        elif y == 8:
            lt_y = [y - 1, y]
        else:
            lt_y = [y - 1, y, y + 1]
                        
        return (lt_x,lt_y)
    
    """The draw_floor_or_wall, draw_border, draw_circle, and draw_label functions are helper functions for drawing in the Pygame window. Each of these functions takes position 
    and color as parameters and draws the corresponding figure in the window."""
    
    def draw_label(self,text_size,x,y,mrg_x,mrg_y,text):
        font = pygame.font.Font(None, text_size)
        label = font.render(f"{text}", True, (255, 255, 255))
        self.screen.blit(label, ((x * self.tile_size + self.tile_size / 2) + mrg_x, (y * self.tile_size + self.tile_size / 2) + mrg_y))
        pygame.display.update()
    
    def draw_circle(self,color,x,y,diametre):
        pygame.draw.circle(self.screen,color,(x * self.tile_size + self.tile_size / 2,y * self.tile_size + self.tile_size / 2,),diametre)
        pygame.display.update()
        
    def draw_floor_or_wall(self,color,x,y):
        pygame.draw.rect(self.screen, color, (x, y, self.tile_size, self.tile_size))
        pygame.display.update()
        
    def draw_border(self,color,x,y,border):
        pygame.draw.rect(self.screen, color, (x, y, self.tile_size,self.tile_size), border)
        pygame.display.update()
        
    """In general, the code is a basic implementation of the A* algorithm with a simple visualization using Pygame. The game board is randomly generated and the 
    destination and origin are also randomly generated. The user cannot interact with the game."""