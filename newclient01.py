#!/usr/bin/python3

import sys
import cmd
from pprint import pprint
from random import randrange
import comm

# Parse options

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
#me = comm.Client (**clientconf)

"""i = 0
for (board, myself) in me.connect():
    print (board)
    print ("next")
    print (myself)
    if i == 0:
        me.go (1,1)
        
        
    elif i == 1:
        me.relax()
               
    
    i = ( i + 1 ) % 2
    
"""
neighbours = [(1, 0), (1, 1), (0, 1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]

a, b = 15, 15
for i, (board, myself) in enumerate(me.connect()):
    print(board)
    print("next")
    print(myself)
    hed_flag = False
    border_flag = False
    
    if i % 2 == 0:
        x = myself[4]
        y = myself[5]
        print (x, y)
        dx, dy = 0,0
        if x == 1:
            dx = 1
            border_flag = True
        if x == a-1:
            dx = -1
            border_flag = True
        if y == 1:
            dy = 1
            border_flag = True
        if y == b-1:
            dy = -1
            border_flag = True
    
        if border_flag:
            me.go(dx,dy)
        else:
            me.go(randrange(3)-1, randrange(3)-1)
    else:
       x = myself[4]
       y = myself[5]
       if board[x][y][0]!=0:
           print ("stuff: ", board[x][y][0])
           me.eat_from_cell()
       else:
           me.relax()


