#!/usr/bin/python3
import pyglet
from amnesiac.window import *



if __name__ == '__main__':
    win = Window(15 * 32, 15 * 32, caption="Amnesiac Engine " + VERSION, resizable=False)
    pyglet.app.run()
