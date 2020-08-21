
from pyglet.window import key


def init(game):
    if "panels_active" in game.data.keys():
        if game.data["panels_active"]:
            activate_panels(game)

def main(game):
    pass


def activate_panels(game):
    old_map = game.targetMap(0)
    for y in range(35,44):
        for x in range(7,9):
            game.setTile(x,y,14)
    game.targetMap(old_map)
