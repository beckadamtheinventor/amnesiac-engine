
from pyglet.window import key
import random

COUNTER="nexus-count"

def init(game,x,y):
	pass

def main(game):
	model=game.model
	player=game.player
	x,y = model.x,model.y
	#crossing x=63 between y=25 and y=38
	if y>=24 and y<38 and x>71:
		game.load_level("data/level/caves/open-air/index")
		game.set_pos(7,y)

