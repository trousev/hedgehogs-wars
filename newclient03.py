#!/usr/bin/python3

import sys
import cmd
from pprint import pprint
from random import randrange
import comm

# Parse options

clientconf = dict()
stringparams = ('address', 'name')

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


neighbours = [(1, 0), (1, 1), (0, 1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
#Throwing h.
a, b = 15, 15
for i, (board, myself) in enumerate(me.connect()):
    print(board)
    print("next")
    print(myself)
    hed_flag = False
    stuff_flag = False
    border_flag = False
    
    if i % 2 == 0:
        x, y = randrange(a), randrange(b)
        me.throw_cabbage(x, y) 
        
    else:
        me.relax()


