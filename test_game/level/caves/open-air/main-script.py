
from pyglet.window import key
from amnesiac.game import getGameObject
game = getGameObject()

def main():
	model=game.model
	player=game.player
	x,y = model.x,model.y
	#crossing x=63 between y=25 and y=38
	if game.checkIntersectsRect(player.pos,(7,24,9,38)):
		game.loadLevel("$LEVEL/caves/main/index")
		game.setPos(71+x-7,y)
	#y=31 between x=29 and x=30
	elif game.checkIntersectsRect(player.pos,(43,32,44,33)):
		if game.keys[key.SPACE]:
			game.loadLevel("$LEVEL/caves/temple/index")
			game.setPos(15.5,60.5)
	# exit between x=47 and x=56
	elif game.checkIntersectsRect(player.pos,(47,1,57,2)):
		game.loadLevel("$LEVEL/index/index")
		game.setPos(x+16-47,y+30-2)
