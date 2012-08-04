import pickle
import connectivity
import time
#import pygame
import sys
from random import random
#from pygame.locals import *
#import os
#if os.name == 'nt':
#        os.environ['SDL_VIDEODRIVER']='windib'

from random import randrange
from logic import *
import comm

size_a=15
size_b=15

#screen=pygame.display.set_mode(((size_a+10)*cell_size,size_b*cell_size))
world=World(size_a, size_b)
#pygame.display.set_caption('Hedgehogs')



world.generate_stuff(2, 20)
world.generate_stuff(1, 20)
world.generate_stuff(3, 20)
#world.draw_whole_world()
#world.draw_info_pannel()
#pygame.display.update()

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
    hedgehog.spawn_x = x
    hedgehog.spawn_y = y
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
# print (world.size_a)


############### FIRST SYNC WITH GRAPHICS SERVER ##########################
session = connectivity.Session()
session.init(world.size_a,world.size_b)

session.message("preparing...")
for name, hedgehog in list(hedgehogs.items()):
    hedgehog.graphics_item = connectivity.Hedgehog(session)
    hedgehog.graphics_item.set_name(name)
    hedgehog.graphics_item.move(hedgehog.spawn_x, hedgehog.spawn_y)

time.sleep(3)
session.message("SHOWTIME!")
############################ SYNC END ####################################

while len(hedgehogs) > 1:
    # TODO Deaths are detected in a hackish way (see Hedgehog.die() for where
    # they should really be handled). World.game_over() could (should?)
    # have been used to terminate the main loop, but it can't be.
    #
    server.broadcast((name, hedgehog.get_all_info())
                     for name, hedgehog in hedgehogs.items())
    time.sleep(1)
    #TODO the first phase doesn't work!
    cab_flag = False
    for name, act, i, j in server.moves():
        if act =='go':
            hedgehogs[name].go(i, j)	# Relative coordinated hog moved
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

#pygame.time.delay(5000)    
#pygame.display.quit()



