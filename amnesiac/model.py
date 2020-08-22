
import os, sys, math, pyglet
from pyglet.window import key
from pyglet.gl import *
from amnesiac.globs import *
from amnesiac.player import *
from amnesiac.window import *
from amnesiac.script import *
from amnesiac.entity import *
from amnesiac.game import *
from amnesiac.util import *



class Model:
    def __init__(self, level=None):
        self._cutstack = []
        self._levelstack = []
        self.batch = [pyglet.graphics.Batch() for N in range(8)]
        self.none_tex = self.get_tex(GFX_FOLDER + "/tex/tex_None.png")
        self.none_tileset = {"-1": self.none_tex}
        self.sprites = [pyglet.sprite.Sprite(self.none_tex, batch=self.batch[N // (25 * 25)], x=-1000, y=-1000) for N in
                        range(25 * 25 * 8)]
        self.x = self.y = 0
        self.level_name = level
        self.drawPlayer = True
        self.lockPlayer = False
        self.playeratlas = []
        self.scripts = []
        self.entities = []
        self._draw_next = []
        self._draw_next_scale = 1
        self._draw_next_scale_xy = [1, 1]
        try:
            for s in ["down", "up", "left", "right"]:
                self.playeratlas.append(self.get_tex(GFX_FOLDER + "/player-" + s + ".png"))
            self.playersprite = pyglet.sprite.Sprite(self.playeratlas[0], x=32 * 7, y=32 * 7)
            self.playersprite.scale = 1
        except:
            pass

        self.solids = []

        self.image = None
        self.renderMode = 0
        self._keyhandlers = {}

    def set_game(self, game):
        self.game = game

    def exit_level(self):
        for script in self.scripts:
            script.run_save(self.game)
        self.scripts.clear()
        self.entities.clear()
        try:
            del self.tileset
            del self.level
        except:
            pass

    def enter_level(self, player):
        if player.has_loaded_level:
            self.x, self.y = player.pos
        else:
            self.x, self.y = self.level["start"]
        for script in self.scripts:
            script.run_init(self.game)

    def load_level(self, fname):
        try:
            self.exit_level()
        except:
            pass
        self.tileset = self.none_tileset
        self.level = {"list": [], "start": [0, 0]}
        p = ""
        with open(pathrep(fname)) as f:
            data = f.read().splitlines()
        for line in data:
            if line.startswith("map:"):
                with open(p + line[4:]) as f:
                    level = {}
                    level["area"] = m = [[int(c) for c in l.split(",")] for l in f.read().splitlines()]
                    level["height"] = len(m)
                    level["width"] = len(m[0])
                    self.level["list"].append(level)
            elif line.startswith("tex:"):
                w = line[4:].split(",", maxsplit=1)
                self.tileset[w[0]] = self.get_tex(pathrep(p + w[1]))
            elif line.startswith("start:"):
                c = line[6:].split(",")
                self.level["start"] = [int(c[0]), int(c[1])]
            elif line.startswith("path:"):
                p = pathrep(line[5:] + "/")
            elif line.startswith("script:"):
                self.scripts.append(Script(pathrep(p + line[7:])))
            elif line.startswith("solid:"):
                for w in line[6:].split(","):
                    self.solids.append(int(w))
        self.targetMap(0)

    def add_entity(self, entity):
        self.entities.append(entity)

    def update(self, vx, vy, keys):
        x = vx + self.x
        y = vy + self.y
        if not self.lockPlayer:
            m = -1
            if vx > 0:
                m = 3
            elif vx < 0:
                m = 2
            elif vy > 0:
                m = 0
            elif vy < 0:
                m = 1
            if m != -1:
                self.playersprite.image = self.playeratlas[m]

            if not self.checkColided(vx, vy):
                self.x, self.y = x, y
        self.tryRunScript(x, y, keys)
        for entity in self.entities:
            entity.update(self.game)

    def checkColided(self, vx, vy):
        self.targetMap(0)
        X, Y = self.x + vx + .5, self.y + vy + .5
        t = self.getTile(X, Y)
        if t in self.solids or t is None:
            return True
        t = self.getTile(X, Y + .5)
        if t in self.solids or t is None:
            return True
        return False

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def addEntity(self, ent):
        self.entities.append(ent)

    def removeEntity(self, ent):
        self.entities.remove(ent)

    def getDistance(self, x1, y1, x2=None, y2=None):
        if x2 == None: x2 = self.x
        if y2 == None: y2 = self.y
        return pow(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2), 1 / 2)

    def enterCutscene(self, drawplayer=False, lockplayer=True):
        self._cutstack.append([self.x, self.y, self.drawPlayer, self.lockPlayer])
        self.drawPlayer = drawplayer
        self.lockPlayer = lockplayer
        return len(self._cutstack)

    def exitCutscene(self):
        self.x, self.y, self.drawPlayer, self.lockPlayer = self._cutstack.pop(-1)
        return len(self._cutstack)

    def enterLevel(self, player, fname):
        self.exit_level()
        self.load_level(fname)
        self.enter_level(player)

    def setKeyHandler(self,key,func):
        if key in self._keyhandlers.keys():
            self._keyhandlers[key].append(func)
        else:
            self._keyhandlers[key] = [func]

    def handle_keys(self,dt):
        for key in self._keyhandlers.keys():
            self._keyhandlers[key](dt)


    def getTile(self, x, y):
        if self.curlevel is not None:
            if int(x) in range(self.curlevel["width"]) and int(y) in range(self.curlevel["height"]):
                return self.curlevel["area"][int(y)][int(x)]
        return None

    def setTile(self, x, y, tile):
        if self.curlevel is not None:
            if int(x) in range(self.curlevel["width"]) and int(y) in range(self.curlevel["height"]):
                self.curlevel["area"][int(y)][int(x)] = tile
                return True
            return False
        return None

    def targetMap(self, mapno):
        try:
            old = self.level["list"].index(self.curlevel)
        except:
            old = 0
        if mapno < len(self.level["list"]):
            self.curlevel = self.level["list"][mapno]
        else:
            self.curlevel = None
        return old

    def tryRunScript(self, x, y, keys):
        self.x_pos = x
        self.y_pos = y
        self.x_tile = int(x)
        self.y_tile = int(y)
        for script in self.scripts:
            script.run_main(self.game)

    def get_tex(self, fname):
        try:
            tex = pyglet.image.load(fname).get_mipmapped_texture()
        except:
            tex = pyglet.image.load(GFX_FOLDER + "/tex/tex_None.png").get_mipmapped_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return tex

    def setImage(self, fname=None, x=0, y=0):
        old = self.image
        if fname is None:
            self.image = None
        else:
            self.image = pyglet.image.load(pathrep(fname))
        self.image_x = x;
        self.image_y = y
        return self.image

    def getImage(self):
        return self.image

    def draw(self):
        self.size_x, self.size_y = self.game.window.get_size()
        self.scale = min(self.size_x, self.size_y) // 15
        if self.renderMode == 0:
            self.get_tiles([self.x, self.y])
            for i in range(len(self.level["list"])):
                self.batch[i].draw()
            if self.drawPlayer:
                self.playersprite.x = self.size_x / 2 - 16
                self.playersprite.y = self.size_y / 2 - 16
                self.playersprite.draw()
        elif self.renderMode == 1:
            self.image.blit(self.image_x, self.image_y)
        for entity in self.entities:
            entity.draw(self.game)
        for script in self.scripts:
            script.run_draw(self.game)
        for item in self._draw_next:
            item.draw()
        self._draw_next.clear()

    def draw_item_scale(self, x=1, y=None):
        if y is None:
            self._draw_next_scale = x
        elif x != y:
            self._draw_next_scale = None
            self._draw_next_scale_xy = [x, y]
        else:
            self._draw_next_scale = x

    def draw_sprite(self, img, x=0, y=0):
        spr = pyglet.sprite.Sprite(img, x, y)
        if self._draw_next_scale is None:
            x, y = self._draw_next_scale_xy
        else:
            x = y = self._draw_next_scale

        spr.update(scale_x=x, scale_y=y)
        self._draw_next.append(spr)
        return len(self._draw_next)

    def get_tiles(self, pos):
        x = int(pos[0]);
        y = int(pos[1])
        fx = (self.x - int(self.x)) * self.scale
        fy = -((self.y - 1) - int(self.y)) * self.scale
        offset = i = 0
        for m in self.level["list"]:
            Y = 20 * self.scale
            for iy in range(y - 12, y + 13):
                X = -5 * self.scale
                for ix in range(x - 12, x + 13):
                    spr = self.sprites[i]
                    tn = -1
                    if iy in range(m["height"]) and ix in range(m["width"]):
                        tn = int(m["area"][iy][ix])
                    if tn != -1:
                        spr.image = self.tileset[str(tn)]
                        spr.update(scale=self.scale / 32, x=X - fx, y=Y - fy)
                    else:
                        spr.update(x=-1000, y=-1000)
                    X += self.scale;
                    i += 1
                Y -= self.scale
