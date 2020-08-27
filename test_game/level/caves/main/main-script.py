
from pyglet.window import key
import random
from amnesiac.game import getGameObject
game = getGameObject()

COUNTER="nexus-count"


def init():
	pass


def main():
	model=game.model
	player=game.player
	x,y = model.x,model.y
	# crossing x=63 between y=25 and y=38
	if game.checkIntersectsRect(player.pos,(71,24,73,38)):
		game.loadLevel("$LEVEL/caves/open-air/index")
		game.setPos(7+x-71,y)

