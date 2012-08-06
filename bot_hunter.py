#!/usr/bin/python3
# Hunter is a simple improvement.

import sys
import cmd
from pprint import pprint
from random import randrange, randint
import comm

class AI:
  def __init__(self):
    pass
  def FirstPhase(self):
    if 'cabbage' in self.inventory:
        print ("Time to THROW!!!!")
        self.me.throw_cabbage(2,2)
        # self.me.go(0,0)
        return 
    for i in self.square:
        if self.x + i[0] >= self.max_x:
          continue
        if self.x + i[0] < 0:
          continue
        if self.y + i[1] >= self.max_y:
          continue
        if self.y + i[1] < 0:
          continue
        if board[self.x+i[0]][self.y+i[1]][1] != 0:
          print ("Victim is near!")
          self.me.go(0,0)
          return
        
    for i in self.neighbours:
        if self.x + i[0] >= self.max_x:
          continue
        if self.x + i[0] < 0:
          continue
        if self.y + i[1] >= self.max_y:
          continue
        if self.y + i[1] < 0:
          continue
        
        if str(self.board[self.x+i[0]][self.y+i[1]] [0] ) != "0" :
          print ("Found direction: " + str(i[0]) + ","+str(i[1]) )
          self.me.go(i[0],i[1])
          return
          
    self.me.go(randint(-1,1),randint(-1,1))
    
  def SecondPhase(self):
    
    for i in self.square:
        if self.x + i[0] >= self.max_x:
          continue
        if self.x + i[0] < 0:
          continue
        if self.y + i[1] >= self.max_y:
          continue
        if self.y + i[1] < 0:
          continue
        if board[self.x+i[0]][self.y+i[1]][1] != 0:
          self.me.prick(i[0],i[1],-10)
          print ("PRICK!!!")
          return 
    
    mycell = str(self.board[self.x][self.y] [0] )
    if mycell == "cabbage":
      self.me.pick()
      # self.me.relax()
    elif mycell == "0":
      self.me.relax()
    else:
      self.me.eat_from_cell()

# Parse options
# Initialising connection ...
clientconf = dict()
stringparams = ('address', 'name', 'port')

for opt in sys.argv[1:]:
    if opt.startswith('-C'):
        conf = clientconf
    else:
        raise ArgumentError("unrecognized command line option")

    name, value = opt[2:].split('=', 1)
    name = name.strip().lower().replace('-', '_')
    conf[name] = int(value.strip()) if name not in stringparams else value

# Begin communication
print (value)
me = comm.Client(value)
ai = AI() ## Change it if You want
ai.me = me

ai.neighbours = [(1, 0), (1, 1), (0, 1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
ai.square     = [(1, 0), (0, 1), (-1,0), (0,-1)]
#Stupid h.
a, b = 15, 15
ai.max_x = a
ai.max_y = b
for i, (board, myself) in enumerate(me.connect()):
    
    print("Next move.")
    #print(board)
    #print(myself)
    #print (board[1][1])
    ai.board = board
    ai.myself = myself
    ai.hp = myself[1]
    ai.ap = myself[2]
    ai.inventory = myself[3]
    ai.x = myself[4]
    ai.y = myself[5]
    # hed_flag = False
    # border_flag = False
    
    if i % 2 == 0:
        ai.FirstPhase()     

    else:
       ai.SecondPhase()


