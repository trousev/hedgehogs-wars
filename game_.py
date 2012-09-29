import pickle
import pygame, sys
from random import random
from pygame.locals import *
import os
if os.name == 'nt':
        os.environ['SDL_VIDEODRIVER']='windib'

from random import randrange

import comm
import time


class World:
        #I'm hedgehogs' world. My size is size_a, size_b.
        def __init__(self, size_a=10, size_b=5, delta_health_collision=-3, delta_health_cabbage=-20, bag_size=3,
                     max_health=100, max_power=100, delta_health_kit=50, delta_power_apple=10,
                     cabbage_min_d_sqr=9, cabbage_max_d_sqr=25, prick_delta_power_max=-10):
                self.cell_size=32
                self.cells=[[Cell(i, j, self) for j in range(size_b)] for i in range(size_a)]
                self.world_info=[[0 for j in range(size_b)] for i in range(size_a)]
                self.size_a=size_a
                self.size_b=size_b
                self.moving=[]
                self.moving_counter=0
                self.hedgehog_num=0
                self.same_cell=[]
                self.hedgehogs=set()
                self.delta_health_collision=delta_health_collision
                self.delta_health_cabbage=delta_health_cabbage
                self.bag_size=bag_size
                self.max_power=max_power
                self.max_health=max_health
                self.delta_health_kit=delta_health_kit
                self.delta_power_apple=delta_power_apple
                self.cabbage_min_d_sqr=cabbage_min_d_sqr
                self.cabbage_max_d_sqr=cabbage_max_d_sqr
                self.prick_delta_power_max=prick_delta_power_max
                self.hedgehogs_info=()
                self.ready_to_die=[]
                self.flying_cabbage=[]
                self.pricking_hedgehogs=[]
                self.info_rect=pygame.Surface((10*cell_size,self.size_b*cell_size))
                self.info_pos=(self.size_a*cell_size,0)
        def __str__ (self):
                res=''
                for i in range(self.size_a):
                        for j in range(self.size_b):
                                res+=str(self.cells[i][j])+ ' '
                        res+='\n'
                return res
        def generate_stuff(self, type, n=1):
                # Generates no more than n new objects of a certain type in this wonderful new world.
                #Facing not empty cell, it does noting.
                for k in range (n):
                        i,j=int(random()*self.size_a),int(random()*self.size_b)
                        self.cells[i][j].new_stuff(type)
        def inc_moving_counter(self):
                #When all the hedgehogs have chosen their moving it makes world thinking
                self.moving_counter+=1
                #if (self.moving_counter==self.hedgehog_num):
                        #self.start_moving()
        def first_phase(self):
                #Hedgehogs are moving and throwing cabbage
                self.start_moving()
                self.move()
                self.throw_all_cabbage()
                self.kill_ready_to_die()
                self.draw_whole_world()
                self.draw_info_pannel()
                self.check_winner()
                clock.tick(1)
                pygame.display.update()
        def second_phase(self):
                self.draw_pricking()
                self.kill_ready_to_die()
                self.draw_whole_world()
                self.draw_info_pannel()
                self.check_winner()
                clock.tick(1)
                pygame.display.update()
        def check_winner(self):
                if len(self.hedgehogs)==1:
                        self.draw_win()
        def draw_pricking(self):
                for t in range (pricking_time):
                        self.draw_whole_world
                        for i in self.pricking_hedgehogs:
                                i[0].draw_pricking_prep(t)
                        clock.tick(2)
                        pygame.display.update()
                for i in self.pricking_hedgehogs:
                        if i[2]==1:
                                i[0].draw_pricking("right")
                        elif i[2]==-1:
                                i[0].draw_pricking("left")
                        elif i[1]==1:
                                i[0].draw_pricking("down")
                        elif i[1]==-1:
                                i[0].draw_pricking("up")
                pygame.display.update()
                clock.tick(1)
                self.pricking_hedgehogs=[]
        def start_moving(self):
                #Машет руками так, что все в результате благополучно подвинутся.
                for i in range (self.hedgehog_num):
                        #Make sure, the hedgehogs aren't ghosts.
                        for j in range (self.hedgehog_num):
                                if i!=j:
                                        if ((self.moving[i][3:5]==self.moving[j][1:3])
                                        and (self.moving[i][1:3]==self.moving[j][3:5])):
                                                self.moving[i][3:5]=self.moving[i][1:3]
                                                self.moving[i][5]+=self.delta_health_collision
                                                self.moving[j][3:5]=self.moving[j][1:3]
                                                self.moving[j][5]+=self.delta_health_collision
                self.check_moving()
                        #checks if there are hedgehogs trying to force the same cell.
        def check_moving(self):
                #checks if there are hedgehogs trying to force the same cell. Deals with it
                a=0
                for i in self.moving:
                        for j in self.same_cell:
                                if i[3:5]==j[0][3:5]:
                                        j.append(i)
                                        a=1
                                        break
                        self.same_cell.append([i])
                for i in self.same_cell:
                        if len(i)>1:
                                        for j in i:
                                                j[3:5]=j[1:3]
                                                j[5]+=self.delta_health_collision
                self.same_cell=[]
                if a: self.check_moving()
                                                        
        def move(self):
                #moves all the hedgehogs. changes theirs health.
                for i in self.moving:
                        i[0].change_health(i[5])
                for i in (self.ready_to_die):
                        self.moving.remove(i)
                self.kill_ready_to_die()
                self.draw_moving()
                for i in self.moving:
                        i[0].move(i[3:5])                
                self.moving_counter=0
                self.moving=[]
        def draw_moving(self):
                #Draws hedgehog's and cabbage moving
                c=len(self.flying_cabbage)
                if c:
                        for i in self.flying_cabbage:
                                i.append([i[0]*cell_size, i[1]*cell_size])
                                i.append([i[2]*cell_size/moving_time, i[3]*cell_size/moving_time])
                if len(self.moving):
                        for i in self.moving:
                                i.append([(i[3]-i[1])*cell_size/moving_time, (i[4]-i[2])*cell_size/moving_time])
                                if (i[6][0] or i[6][1]):
                                        i.append(1)
                                else:
                                        i.append(0)
                        for t in range (moving_time):
                              self.draw()
                              for i in self.moving:
                                      if i[7]:
                                              i[0].pos[0]+=i[6][0]
                                              i[0].pos[1]+=i[6][1]
                                              i[0].draw_moving(t)
                                      else:
                                              i[0].draw()
                              if c:
                                      for i in self.flying_cabbage:
                                              i[4][0]+=i[5][0]
                                              i[4][1]+=i[5][1]
                                              screen.blit(eval("pic_flying_cabbage"), i[4])
                              clock.tick(18)
                              pygame.display.update()
        def kill_ready_to_die(self):
                #For hedgehogs
                self.draw_dying()
                for i in (self.ready_to_die):
                        print("They are dying!")
                        i.die()
                self.ready_to_die=[]
        def draw_dying(self):
                for t in range(dying_time):
                        self.draw_whole_world()
                        for i in (self.ready_to_die):
                                screen.blit(eval("pic_dying_hedgehog_"+str(t)), i.pos)
                        clock.tick(2)
                        pygame.display.update()                
        def throw_all_cabbage(self):
                #Throws cabbage from hedgehog at i,j to i+delta_i, j+delta_j cell.
                #Thinks about results
                for c in self.flying_cabbage:
                        self.cells[c[0]+c[2]][c[1]+c[3]].kill_hedgehog()
                        for d_i in [1, 0, -1]:
                                for d_j in [1, 0, -1]:
                                        self.cabbage_damage(c[0]+c[2]+d_i, c[1]+c[3]+d_j)
                self.flying_cabage=[]
        def throw_cabbage(self, i, j, delta_i, delta_j):
                #Prepares the right array.
                if 0<=i+delta_i<self.size_a and 0<=j+delta_j<self.size_b:
                        self.flying_cabbage.append([i,j,delta_i,delta_j])
                else:
                        return(1)
        def cabbage_damage(self,i ,j):
                #If you were a bit lucky
                if (0<=i<self.size_a) and (0<=j<self.size_b):
                        self.cells[i][j].change_hedgehog_health(self.delta_health_cabbage)
        def delta_power_cabbage(self, delta_i, delta_j):
                #Counts the amount of power you need to throw cabbage)
                return(-int((delta_i**2+delta_j**2)**0.5))
        def prick_damage(self, delta_power):
                #Counts the damege from pricking with delta_power
                return(delta_power-1)
        def dec_hedgehog_num (self):
                self.hedgehog_num-=1
                if self.hedgehog_num==1:
                        self.game_over
        def game_over(self):
                print("Game over!")
        def get_info (self):
                #Returns the information about the whole world.
                for i in range (self.size_a):
                        for j in range (self.size_b):
                                self.world_info[i][j]=self.cells[i][j].get_info()
                return self.world_info
        def draw (self):
                #Draws cells and stuff only
                for i in range (self.size_a):
                        for j in range (self.size_b):
                                self.cells[i][j].draw()
        def draw_whole_world(self):
                #Drafs cells, stuff and hedgehogs
                self.draw()
                for i in self.hedgehogs:
                        i.draw()
        def draw_info_pannel(self):
                self.info_rect.fill((161,195,142))
                screen.blit(eval('self.info_rect'), self.info_pos)
                for i in self.hedgehogs:
                        i.draw_info()
        def draw_win(self):
                self.info_rect.fill((161,195,142))
                screen.blit(eval('self.info_rect'), self.info_pos)
                for i in self.hedgehogs:
                    i.draw_win()                        

                
class Cell:
        #I'm a cell in this world. i and j are my coordinates.
        def __init__ (self, i, j, world):
                self.i, self.j=i, j
                self.hedgehog=0
                self.stuff=0
                self.world=world
                self.pos=(i*cell_size,j*cell_size)
                self.screen=screen
                self.stuff_names=[0, "apple", "kit", "cabbage"]
                self.stuff_pos=(0,0)
                return None
        def __str__ (self): return "(%s;%s)" %(self.hedgehog, self.stuff)
        def put_hedgehog(self, hedgehog):
                #Поздравляем, у вас ёжик.
                self.hedgehog=hedgehog
        def new_stuff(self, type): 
                # 0=None, 1=apple, 2=first aid kit, 3=shotgun (type=cabbage).
                if not self.stuff:
                        self.stuff=self.stuff_names[type%4]
                self.draw()
        def del_hedgehog(self, hedgehog):
                #if this hedgehog stands on this cell, delete it. Don't use for killing
                if(self.hedgehog==hedgehog):
                        self.hedgehog=0
                        self.draw()
        def kill_hedgehog(self):
                #If there is a hedgehog here, kill it
                if(self.hedgehog):
                        self.hedgehog.become_ready_to_die()
        def change_hedgehog_health(self, delta_health):
                #If there are a hedgehog here, change its health.
                if(self.hedgehog):
                        self.hedgehog.change_health(delta_health)
        def get_stuff(self):
                #returns object, deletes it from the cell. If there are no object, returns 0
                stuff=self.stuff
                self.stuff=0
                self.draw()
                self.hedgehog.draw()
                return (stuff)
        def prick_hedgehog (self, delta_power):
                #someone pricks your hedgehog, bro.
                if self.hedgehog:
                        self.hedgehog.change_health(self.world.prick_damage(delta_power))
        def get_info(self):
                #Returns the information about self objects and hedgehog
                info=[0,0]
                info[0]=(self.stuff)
                if self.hedgehog:
                        info[1]=self.hedgehog.get_info()
                return (info)
        def draw(self):
                screen.blit(eval("pic_grass"), self.pos)
                if self.stuff:
                        screen.blit(eval("pic_"+self.stuff), self.pos)

                
        
                

class Hedgehog:
        #I'm a hedgehog! The most intelligent creature in your world.
        def __init__ (self, name="Bubuka", health=100, power=20):
                # Creates an instance with some health, power and empty bag.
                self.bag=[]
                self.health=health
                self.power=power
                self.name=name
                #self.surname=int random()*1000
                return None
        def __str__ (self): return "1"
        def look_inside(self):
                #Get the information about health, power and bag
                print("Name=%s, health=%d, power=%d, bag=%s, i=%d, j=%d" %(self.name, self.health, self.power, self.bag, self.i, self.j))
        def put_on_cell(self, world, i, j):
                                #This puts a hedgehog (first time in the world) on cell i, j, but doesn't check if it's empty.
                self.screen=world.cells[i%world.size_a][j%world.size_b].put_hedgehog(self)
                self.world=world
                k=len(self.world.hedgehogs)
                self.world.hedgehogs.add(self)
                self.init_info(k)
                self.world.hedgehog_num+=1
                self.i, self.j=i,j
                self.count_pos()
                self.draw()
        def init_info(self, k):
                self.info_pos_1=(self.world.size_a*cell_size,4*k*cell_size)
                self.info_pos_2=((self.world.size_a+2)*cell_size,4*k*cell_size)
                self.info_pos_3=((self.world.size_a+2)*cell_size,(4*k+1)*cell_size)
                self.info_pos_4=((self.world.size_a+2)*cell_size,(4*k+2)*cell_size)
                font = pygame.font.Font(None, 36)
                self.text_name = font.render(self.name, 1, (0, 0, 0))
        def count_pos(self):
                self.pos=[self.i*cell_size, self.j*cell_size]
        def go(self, delta_i, delta_j):
                #Starts moving. delta_i, delta_j should be +-1, 0. If you try to force the wall do nothing.
                if (0<=self.i+delta_i<self.world.size_a) and (0<=self.j+delta_j<self.world.size_b):
                        self.world.moving.append([self, self.i, self.j, self.i+delta_i, self.j+delta_j, 0])
                else:
                        self.world.moving.append([self,self.i,self.j,self.i,self.j,0])
                self.world.inc_moving_counter()
        def move(self, moving_par):
                #New cell!
                #Here you can add some effects caused by heigth changing.
                # NB! if you want continious moving, you should rewrite cell.del_hedgehog
                print("I'm moving!")
                self.world.cells[self.i][self.j].del_hedgehog(self)
                self.i=moving_par[0]
                self.j=moving_par[1]
                self.world.cells[self.i][self.j].put_hedgehog(self)
                self.count_pos()
                self.draw()
        def change_health(self, delta_health):
                #Comes as is.
                self.health+=delta_health
                if self.health<=0:
                        self.become_ready_to_die()
                elif self.health>self.world.max_health:
                                self.health=self.world.max_health
        def change_power(self, delta_power):
                #Comes as is.
                self.power+=delta_power
                if self.power>self.world.max_power:
                        self.power=self.world.max_power
        def become_ready_to_die(self):
                self.world.ready_to_die.append(self)
                self.world.hedgehogs.discard(self)
                self.world.dec_hedgehog_num()
                
        def die (self):
                #You've failed the game.
                print("I've died!")
                self.health=0
                self.world.cells[self.i][self.j].del_hedgehog(self)
                #Here should be something
        def throw_cabbage(self, delta_i, delta_j):
                #Tries to use shotgun.
                distance_sqr=delta_i**2+delta_j**2
                if ("cabbage" in self.bag):
                        #Do you really have cabbage?
                        if self.world.cabbage_min_d_sqr<=distance_sqr<=self.world.cabbage_max_d_sqr:
                                #Could you do it?
                                delta_power=self.world.delta_power_cabbage(delta_i, delta_j)
                                if (self.power>=delta_power):
                                        #Do you own the power? Ok, then do it
                                        if self.world.throw_cabbage(self.i, self.j, delta_i, delta_j):
                                                self.cabbage_fail()
                                        self.bag.remove("cabbage")
                                        self.power+=delta_power
                                else: self.cabbage_fail()
                        else: self.cabbage_fail()
                else:self.cabbage_fail()
        def cabbage_fail(self):
                #It happens, when the hedgehog can't throw cabbage for some reason
                pass
        def pick_in_bag (self):
                #Puts an object from the cell to your bag
                if len(self.bag)<self.world.bag_size and self.world.cells[self.i][self.j].stuff:
                        self.bag.append(self.world.cells[self.i][self.j].get_stuff())
        def eat_from_cell(self):
                #Eats object from the cell.
                self.eat(self.world.cells[self.i][self.j].get_stuff())
        def eat_from_bag(self, food):
                #Eats food from the bag, if any of this kind. food should be "kit" or "apple"
                if food in self.bag:
                        self.bag.remove(food)
                        self.eat(food)
        def eat(self, food):
                #eats this foor, if it's eatable.
                if food=="kit":
                        self.change_health(self.world.delta_health_kit)
                if food=="apple":
                        self.change_power(self.world.delta_power_apple)
                if food=="cabbage":
                        self.become_ready_to_die()
        def prick(self, delta_i, delta_j, delta_power):
                #Pricks with a needle hedgehod on that cell with power. delta_i, delta_j should be +-1
                if delta_power<self.world.prick_delta_power_max:
                        delta_power=self.world.prick_delta_power_max
                if self.power+delta_power<0:
                        #do you have enought power?
                        delta_power=-self.power       
                if  0<self.i+delta_i<self.world.size_a or 0<self.j+delta_j<self.world.size_b:
                        #If there is a world there
                        self.world.cells[self.i+delta_i][self.j+delta_j].prick_hedgehog(delta_power)
                        self.world.pricking_hedgehogs.append([self, delta_i, delta_j])
                self.change_power(delta_power)
        def pickle_information(self):
                #Makes a string file to send a player
                return(1)
        def get_info(self):
                #information for all the players
                return ([self.name, self.health, self.power])
        def my_info(self):
                #information for my player
                t=self.get_info()
                t.append(self.bag)
                return (t+[self.i, self.j])
        def get_all_info(self):
                #get all the information about world
                return ([self.world.get_info(), self.my_info()])
        def draw(self):
                screen.blit(eval("pic_hedgehog"), self.pos)
                self.draw_name(self.pos)
        def draw_name(self, pos):
                font = pygame.font.Font(None, 16)
                text_name = font.render(self.name, 1, (0, 0, 0))
                screen.blit(eval("text_name"), pos)
        def draw_pricking_prep(self, t):
                screen.blit(eval("pic_grass"), self.pos)
                screen.blit(eval("pic_prick_"+str(t+1)), self.pos)
                self.draw_name(self.pos)
        def draw_pricking(self, direction):
                screen.blit(eval("pic_grass"), self.pos)
                screen.blit(eval("pic_prick_"+str(5)), self.pos)
                screen.blit(eval("pic_prick_"+str(direction)), self.pos)
                self.draw_name(self.pos)
        def draw_moving(self, t=0):
                screen.blit(eval("pic_moving_hedgehog_"+str(t%2)), self.pos)
                self.draw_name(self.pos)
        def draw_info(self):
                screen.blit(eval("pic_big_hedgehog"), self.info_pos_1)
                screen.blit(eval("self.text_name"), self.info_pos_2)
                font = pygame.font.Font(None, 20)
                self.text_health_power=font.render("health="+str(self.health)+"   power="+str(self.power), 1, (0, 50, 0))
                screen.blit(eval("self.text_health_power"), self.info_pos_3)
                for i in range (len(self.bag)):
                        if self.bag[i]:
                                pos=((self.info_pos_4[0]+i*cell_size), self.info_pos_4[1])
                                screen.blit(eval("pic_big_"+self.bag[i]), pos)
        def draw_win(self):
                screen.blit(eval("pic_big_hedgehog"), self.info_pos_1)
                font = pygame.font.Font(None, 36)
                text_win = font.render(self.name+" win!!", 1, (0, 0, 0))
                screen.blit(eval("text_win"), self.info_pos_2)
                
        
                                

#ToDo: throw away from the bag. dont eat cabbage
pygame.init()
cell_size=32
clock=pygame.time.Clock()
moving_time=32
dying_time=1
pricking_time=4
size_a=15
size_b=15

screen=pygame.display.set_mode(((size_a+10)*cell_size,size_b*cell_size))
world=World(size_a, size_b)
pygame.display.set_caption('Hedgehogs')

pic_grass=pygame.image.load('grass.png').convert_alpha(screen)               
pic_cabbage=pygame.image.load('cabbage.png').convert_alpha(screen)
pic_apple=pygame.image.load('apple.png').convert_alpha(screen)
pic_kit=pygame.image.load('kit.png').convert_alpha(screen)
pic_big_cabbage=pygame.image.load('cabbage_big.png').convert_alpha(screen)
pic_big_apple=pygame.image.load('apple_big.png').convert_alpha(screen)
pic_big_kit=pygame.image.load('kit_big.png').convert_alpha(screen)
pic_flying_cabbage=pygame.image.load('cabbage_big.png').convert_alpha(screen)
pic_hedgehog=pygame.image.load('hedgehog.png').convert_alpha(screen)
pic_big_hedgehog=pygame.image.load('big_hedgehog.png').convert_alpha(screen)
pic_moving_hedgehog_0=pygame.image.load('moving_hedgehog_0.png').convert_alpha(screen)
pic_moving_hedgehog_1=pygame.image.load('moving_hedgehog_1.png').convert_alpha(screen)
pic_dying_hedgehog_0=pygame.image.load('dying_hedgehog.png').convert_alpha(screen)
pic_prick_right=pygame.image.load('pr5e.png').convert_alpha(screen)
pic_prick_left=pygame.image.load('pr5w.png').convert_alpha(screen)
pic_prick_up=pygame.image.load('pr5n.png').convert_alpha(screen)
pic_prick_down=pygame.image.load('pr5s.png').convert_alpha(screen)
pic_prick_1=pygame.image.load('pr1.png').convert_alpha(screen)
pic_prick_2=pygame.image.load('pr2.png').convert_alpha(screen)
pic_prick_3=pygame.image.load('pr3.png').convert_alpha(screen)
pic_prick_4=pygame.image.load('pr4.png').convert_alpha(screen)
pic_prick_5=pygame.image.load('pr5.png').convert_alpha(screen)



world.generate_stuff(2, 20)
world.generate_stuff(1, 20)
world.generate_stuff(3, 20)
world.draw_whole_world()
world.draw_info_pannel()
pygame.display.update()

worldconf = dict()
serverconf = dict()
stringparams = ('address',)

for opt in sys.argv[1:]:
    if opt.startswith('-W'):
        conf = worldconf
    elif opt.startswith('-S'):
        conf = serverconf
    else:
        raise ValueError("unrecognized command line option")

    name, value = opt[2:].split('=', 1)
    name = name.strip().lower().replace('-', '_')
    conf[name] = int(value.strip()) if name not in stringparams else value

# Create the game world

#world = game.World(**worldconf)
server = comm.Server(world.size_a, world.size_b, **serverconf)
print(world.size_a, world.size_b)

#world.generate_stuff(1, 9)
#world.generate_stuff(2, 9)
#world.generate_stuff(3, 3)

# Establish player connections

print("* The game is ready to start, ladies and gentlemen... Anyone?")

hedgehogs = dict()
for name in server.greet():
    hedgehog = Hedgehog(name)
    x, y = randrange(2, world.size_a-1), randrange(2, world.size_b-1)

    while world.cells[x][y].hedgehog != 0: #TODO Use 'None' here!
        x, y = randrange(2, world.size_a-1), randrange(2, world.size_b-1)
    hedgehog.put_on_cell(world, x, y)

    hedgehogs[name] = hedgehog

    print("- Welcome '{0}'!".format(name))

# Run the game



print("* Showtime!")

def announce(server, hedgehogs):
    """Check for killed hedgehogs and send status codes"""

    for name, hedgehog in list(hedgehogs.items()):
        if hedgehog.health > 0:
            continue
        print("- Poor hedgehog '{0}' died.".format(name))
        server.kill(name)
        del hedgehogs[name]

    server.announce()

while len(hedgehogs) > 1:
    # TODO Deaths are detected in a hackish way (see Hedgehog.die() for where
    # they should really be handled). World.game_over() could (should?)
    # have been used to terminate the main loop, but it can't be.
    #
    server.broadcast((name, hedgehog.get_all_info())
                     for name, hedgehog in hedgehogs.items())

    #TODO the first phase doesn't work!
    cab_flag = False
    for name, act, i, j in server.moves():
        if act =='go':
            hedgehogs[name].go(i, j)
        elif act == 'throw':
            hedgehogs[name].throw_cabbage(i, j)
            cab_flag = True
        else:
            assert False
    world.first_phase()
    announce(server, hedgehogs)
    server.broadcast((name, hedgehog.get_all_info())
                     for name, hedgehog in hedgehogs.items())

    for name, move, *params in server.actions():
        # Note that 'params' are guaranteed to be valid (apart from
        # possible TODO World.cabbage_fail() calls that are not handled
        # at all).

        if move == 'relax':
            pass
        elif move == 'eat-from-cell' and not cab_flag:
            hedgehogs[name].eat_from_cell()
        elif move == 'eat-from-bag' and not cab_flag:
            hedgehogs[name].eat_from_bag() # TODO This won't work.
        elif move == 'prick' and not cab_flag:
            hedgehogs[name].prick(params[0], params[1], params[2])
        elif move == 'pick' and not cab_flag:
            hedgehogs[name].pick_in_bag()
        else:
            assert False # We're screwed.
    world.second_phase()
    world.generate_stuff(1, 2)
    world.generate_stuff(2, 2)
    world.generate_stuff(3, 2)
    announce(server, hedgehogs)

server.shutdown()
if len(hedgehogs) > 0:
    print("* We have a winner! And it's '{0}'.".format(list(hedgehogs.keys())[0]))
else:
    print("* Draw :( Better luck next time!")

pygame.time.delay(5000)    
pygame.display.quit()


