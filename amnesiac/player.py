
from pyglet.window import key
import json
from amnesiac.util import pathrep
from amnesiac.globs import GAME_FOLDER

class Player:
    def __init__(self):
        self.pos = [0, 0]
        self.movement = [0, 0]
        self.speed = 7

    def update(self, dt, keys):
        vx = vy = 0
        if keys[key.W]: vy -= self.speed*dt
        if keys[key.S]: vy += self.speed*dt
        if keys[key.A]: vx -= self.speed*dt
        if keys[key.D]: vx += self.speed*dt
        return vx, vy

    def move(self, x, y):
        self.pos = x, y

    def loadgame(self, fname="$DATA/saves/save/save.json"):
        self.pos = [0, 0]
        self.level = "$DATA/level/index/index"
        self.has_loaded_level = False

        try:
            with open(pathrep(fname)) as f:
                j = json.load(f)
                self.pos = j["pos"]
                self.level = j["level"]
                self.has_loaded_level = j["has_loaded_level"]
        except:
            pass

    def savegame(self, fname="$DATA/saves/save/save.json"):
        fname = pathrep(fname)
        j = {"pos":self.pos,"level":self.level,"has_loaded_level":True}
        try:
            os.makedirs(fname.rsplit("/", maxsplit=1)[0])
        except:
            pass
        with open(fname, "w") as f:
            json.dump(j,f)
