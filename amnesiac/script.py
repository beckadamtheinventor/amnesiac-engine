
from amnesiac.game import game
from amnesiac.util import *
from amnesiac.globs import *

import importlib.util,json,time,os

class Script:
    def __init__(self, fname):
        self.fname = pathrep(fname)
        self.sfile = GAME_FOLDER + "/saves/save/" + self.fname + "/save.json"
        spec = importlib.util.spec_from_file_location("*", self.fname)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.module = module
        try:
            os.makedirs(self.sfile.rsplit("/", maxsplit=1)[0])
        except:
            pass
        try:
            with open(self.sfile) as f:
                self.data = json.load(f)
        except:
            self.data = {}

    def run_init(self):
        game._data[self.fname] = self.data
        self.data["_time_main"] = self.data["_time_draw"] = time.time()
        self.run_func("init")

    def run_main(self):
        t = time.time();
        game.dt = t - self.data["_time_main"];
        self.data["_time_main"] = t
        self.run_func("main")

    def run_draw(self):
        t = time.time();
        game.dt = t - self.data["_time_draw"];
        self.data["_time_draw"] = t
        self.run_func("draw")

    def run_save(self):
        self.run_func("save")
        try:
            os.makedirs(self.sfile.rsplit("/", maxsplit=1)[0])
        except:
            pass
        with open(self.sfile, 'w') as f:
            json.dump(self.data, f)

    def run_func(self, func):
        game.push(game._data[self.fname])
        if hasattr(self.module, func):
            getattr(self.module, func)()
        game.pop()
