#!/usr/bin/python3
from connectivity import Session, Hedgehog
import time
import random

try:    
    s = Session()
#try:    
    s.init(10,10)

    for i in range(5):
        s.morph(random.randint(0,9),random.randint(0,9),Session.Cabbage)
        s.morph(random.randint(0,9),random.randint(0,9),Session.Kit)
        s.morph(random.randint(0,9),random.randint(0,9),Session.Clean)
        s.morph(random.randint(0,9),random.randint(0,9),Session.Apple)

    hogs = []
    for i in range(10):
        h = Hedgehog(s)
        h.set_name("Jojeg")
        hogs.append(h)
        h.move(5,5)


    for i in reversed(range(10)):
        time.sleep(1)
        s.message(str(i)+" seconds left!")

    for i in range(10):
        for h in hogs:
            h.move(random.randint(-1,1),random.randint(-1,1))
        time.sleep(3)

    for h in hogs:
        h.kill()
    time.sleep(3)

    for h in hogs:
        h.take()

    s.close()
except NameError:
    s.close()
