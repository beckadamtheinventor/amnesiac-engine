
import os, sys, math, pyglet
from pyglet.window import key
from pyglet.gl import *
from amnesiac.globs import *
from amnesiac.player import *
from amnesiac.model import *
from amnesiac.util import *
from amnesiac.game import makeGameObject



class Window(pyglet.window.Window):
    def push(self, pos, rot): glPushMatrix(); glRotatef(-rot[0], 1, 0, 0); glRotatef(-rot[1], 0, 1, 0); glTranslatef(
        -pos[0], -pos[1], -pos[2])

    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()

    def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()

    def set2d(self): self.Projection(); gluOrtho2D(0, self.width, 0, self.height); self.Model()

    # def set3d(self): self.Projection(); gluPerspective(80,self.width/self.height,0.05,1000); self.Model()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.set_icon(pyglet.image.load(GAME_FOLDER + "/icon.png"))
        self.player = Player()
        self.player.loadgame()
        self.model = Model(self.player.level)
        self.game = makeGameObject(self.model,self.player,self.keys,self)
        self.model.set_game(self.game)
        self.game.loadLevel(self.player.level)

    def update(self, dt):
        x, y = self.player.update(dt, self.keys)
        self.model.update(x, y, self.keys)
        self.player.move(self.model.x, self.model.y)

    def on_draw(self):
        self.set2d()
        self.clear()
        self.model.draw()

    def on_close(self):
        self.model.exit_level()
        self.player.savegame()
        super().on_close()
