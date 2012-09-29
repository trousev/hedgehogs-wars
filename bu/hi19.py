import pickle
import pygame, sys
from random import random
from pygame.locals import *
import os
if os.name == 'nt':
        os.environ['SDL_VIDEODRIVER']='windib'


class World:
        #I'm hedgehogs' world. My size is size_a, size_b.
        def __init__(self, size_a=10, size_b=5, delta_health_collision=-3, delta_health_cabbage=-20, bag_size=3,
                     max_health=100, max_power=100, delta_health_kit=50, delta_power_apple=10,
                     cabbage_min_d_sqr=16, cabbage_max_d_sqr=64, prick_delta_power_max=-10):
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
                #Hedgehogs are moving and throwig cabbage
                self.start_moving()
                self.move()
                self.throw_all_cabbage()
                self.kill_ready_to_die()
                self.draw_whole_world()
                clock.tick(1)
                pygame.display.update()
        def second_phase(self):
                self.draw_pricking()
                self.kill_ready_to_die()
                self.draw_whole_world()
                clock.tick(1)
                pygame.display.update()
        def draw_pricking(self):
                for t in range (pricking_time):
                        self.draw_whole_world
                        for i in self.pricking_hedgehogs:
                                if i[2]==1:
                                        screen.blit(eval("pic_prick_right"), i[0])
                                elif i[2]==-1:
                                        screen.blit(eval("pic_prick_left"), i[0])
                                elif i[1]==1:
                                        screen.blit(eval("pic_prick_down"), i[0])
                                elif i[1]==-1:
                                        screen.blit(eval("pic_prick_up"), i[0])
                        clock.tick(10)
                        pygame.display.update()
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
                screen.fill([50,255,50])
                for i in range (self.size_a):
                        for j in range (self.size_b):
                                self.cells[i][j].draw()
        def draw_whole_world(self):
                #Drafs cells, stuff and hedgehogs
                self.draw()
                for i in self.hedgehogs:
                        i.draw()
        def draw_info_pannel(self):
                for i in self.hedgehogs:
                        pass
                        

                
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
                self.world.hedgehogs.add(self)
                self.world.hedgehog_num+=1
                self.i, self.j=i,j
                self.count_pos()
                self.draw()
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
                        self.world.pricking_hedgehogs.append([self.pos, delta_i, delta_j])
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
        def draw_moving(self, t=0):
                screen.blit(eval("pic_moving_hedgehog_"+str(t%2)), self.pos)

                
        
                                

#ToDo: throw away from the bag. dont eat cabbage
pygame.init()
cell_size=32
clock=pygame.time.Clock()
moving_time=32
dying_time=1
pricking_time=1

size_a=15
size_b=15

screen=pygame.display.set_mode(((size_a+10)*cell_size,size_b*cell_size))
my_world=World(size_a, size_b)
pygame.display.set_caption('Hedgehogs')

pic_grass=pygame.image.load('grass.png').convert_alpha(screen)               
pic_cabbage=pygame.image.load('cabbage.png').convert_alpha(screen)
pic_flying_cabbage=pygame.image.load('cabbage.png').convert_alpha(screen)
pic_apple=pygame.image.load('apple.png').convert_alpha(screen)
pic_kit=pygame.image.load('kit.png').convert_alpha(screen)
pic_hedgehog=pygame.image.load('hedgehog.png').convert_alpha(screen)
pic_moving_hedgehog_0=pygame.image.load('moving_hedgehog_0.png').convert_alpha(screen)
pic_moving_hedgehog_1=pygame.image.load('moving_hedgehog_1.png').convert_alpha(screen)
pic_dying_hedgehog_0=pygame.image.load('dying_hedgehog.png').convert_alpha(screen)
pic_prick_right=pygame.image.load('prick_right.png').convert_alpha(screen)
pic_prick_left=pygame.image.load('prick_left.png').convert_alpha(screen)
pic_prick_up=pygame.image.load('prick_up.png').convert_alpha(screen)
pic_prick_down=pygame.image.load('prick_down.png').convert_alpha(screen)


my_world.generate_stuff(2, 10)
my_world.generate_stuff(1, 10)
my_world.generate_stuff(3, 10)
my_world.draw_whole_world()
pygame.display.update()
pygame.time.delay(1000)
                                       
b=Hedgehog()
c=Hedgehog()
d=Hedgehog()
b.put_on_cell(my_world, 1, 2)
c.put_on_cell(my_world, 3, 3)
d.put_on_cell(my_world, 7, 2)
print(my_world)
b.look_inside()
c.look_inside()
d.look_inside()
pygame.display.update()
pygame.time.delay(1000)
b.bag.append("cabbage")
b.prick(0,1,-5)
b.throw_cabbage(7,0)
c.go(1,1)
b.go(0,1)
d.go(1,0)
my_world.first_phase()
c.prick(1,0, 1)
b.prick(0,1, 1)
c.eat_from_cell()
b.pick_in_bag()
my_world.second_phase()
print(my_world)
pygame.display.update()
pygame.time.delay(1000)
b.look_inside()
c.look_inside()
d.look_inside()

#print(b.get_all_info())
pygame.quit()

