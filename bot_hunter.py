#!/usr/bin/python3
# Hunter is a simple improvement.

import sys
import cmd
from pprint import pprint
from random import randrange, randint
import comm

## API ##
# AI.x, AI.y -- self coordinates
# AI.max_x, AI.max_y -- max coordinates
# AI.board -- 2-dim array of all fields
#   AI.board[x][y] -- one cell, list: ['item in cell','hedgehog in cell']
#     AI.board[x][y][0] -- item in cell, can be [0,'kit','apple','cabbage']
#     AI.board[x][y][1] -- hedgehog in cell, can be 0 or string -- hedgehog name
# AI.inventory -- lists of items in inventory
#
# First phase actions:
# AI.me.go(dx,dy) -- moving
# AI.me.throw_cabbage(dx,dy) -- throwing
#
# Second phase actions:
#   self.me.prick(dx,dy,force) -- self-prick, power MUST be non-positive (unless you want to HEAL enemy :) )
#   self.me.eat_from_cell() -- eat item from cell.
#   self.me.pick() -- grab item from cell. Useful for cabbage only.

class AI:
  def state(self):
    state = {}
    state["nv_x"] = -1
    state["nv_y"] = -1
    state["nv"] = 9999
    state["cabbage"] = len(self.inventory)
    state["hp"] = int(self.hp/4)
    state["ap"] = int(self.ap/4)
    state["my_cell"] = str(board[self.x][self.y][0])
    for x in range(self.max_x):
      for y in range(self.max_y):
        if x == self.x and y == self.y : continue
        if str(self.board[x][y][1]) != "0":
          l = (self.x-x)*(self.x-x) + (self.y-y)*(self.y-y)
          if l < state["nv"]:
            state["nv_x"] = x
            state["nv_y"] = y
            state["nv"] = l
    return state
  def __init__(self):
    pass
  def FirstPhase(self):
    print (self.state())
    self.me.go(0,0)
  def SecondPhase(self):
    self.me.relax()

######################################################################################################

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


