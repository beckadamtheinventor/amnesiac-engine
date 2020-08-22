
import math

EntityViewRange = 100
EntitySpeed = 0.6

def init():
    game.data["x"]=0
    game.data["y"]=0
    game.data["dx"]=0
    game.data["dy"]=0

def main():
    x,y = game.player.pos
    dx,dy = game.player.movement
    x+=dx*3; y+=dy*3
    distance=game.model.getDistance(x,y,game.data["x"],game.data["y"])
    if distance<EntityViewRange:
        angle = math.atan2(y-game.data["y"],x-game.data["x"])
        dx,dy = math.cos(angle)*EntitySpeed,math.sin(angle)*EntitySpeed
        game.data["x"]+=dx; game.data["y"]+=dy


def draw():
    scale = game.model.scale
    mid_x,mid_y = game.model.size_x//2,game.model.size_y//2
    game.drawSprite("$GFX/tex/tex_None.png",game.data["x"]*scale,game.data["y"]*scale+mid_y,2,2)

