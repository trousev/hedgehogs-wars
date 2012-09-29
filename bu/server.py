#!/usr/bin/python3

import sys
from random import randrange

import comm
import game

# Parse options

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

world = game.World(**worldconf)
server = comm.Server(world.size_a, world.size_b, **serverconf)

world.generate_stuff(1, 9)
world.generate_stuff(1, 9)
world.generate_stuff(1, 9)

# Establish player connections

print("* The game is ready to start, ladies and gentlemen... Anyone?")

hedgehogs = dict()
for name in server.greet():
    hedgehog = game.Hedgehog(name)

    x, y = randrange(world.size_a), randrange(world.size_b)
    
    while world.cells[x][y].hedgehog != 0: #TODO Use 'None' here!
        x, y = randrange(world.size_a), randrange(world.size_b)
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

cab_flag = False
while len(hedgehogs) > 1:
    # TODO Deaths are detected in a hackish way (see Hedgehog.die() for where
    # they should really be handled). World.game_over() could (should?)
    # have been used to terminate the main loop, but it can't be.
    # TODO smth with cabbage and its phase
    server.broadcast((name, hedgehog.get_all_info())
                     for name, hedgehog in hedgehogs.items())


#TODO the first phase isn't working!
    
    for name, act, i, j in server.moves():
        print (name, act)
        if act =='go':
            hedgehogs[name].go(i, j)
        elif act == 'throw':
           hedgehogs[name].throw_cabbage(i, j)
           cab_flag = True
        else:
            assert False  
    
    announce(server, hedgehogs)
    server.broadcast((name, hedgehog.get_all_info())
                     for name, hedgehog in hedgehogs.items())

    for name, move, *params in server.actions():
        # Note that 'params' are guaranteed to be valid (apart from
        # possible TODO World.cabbage_fail() calls that are not handled
        # at all).

        if move == 'relax':
            pass
        #elif move == 'throw':
        #   hedgehogs[name].throw_cabbage(params[0], params[1])
        elif move == 'eat-from-cell' and cab_flag == False:
            hedgehogs[name].eat_from_cell()
        elif move == 'eat-from-bag' and cab_flag == False:
            hedgehogs[name].eat_from_bag() # TODO This won't work.
        elif move == 'prick' and cab_flag == False:
            hedgehogs[name].prick(params[0], params[1], params[2])
        elif move == 'pick' and cab_flag == False:
            hedgehogs[name].pick_in_bag()
        else:
            assert False # We're screwed.

    announce(server, hedgehogs)
    cab_flag = False

server.shutdown()
if len(hedgehogs) > 0:
    print("* We have a winner! And it's '{0}'.".format(list(hedgehogs.keys())[0]))
else:
    print("* Draw :( Better luck next time!")
