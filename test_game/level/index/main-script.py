
from pyglet.window import key
from amnesiac.game import getGameObject
game = getGameObject()

def main():
	model=game.model
	player=game.player
	keys=game.keys
	x,y = model.x,model.y
	if game.checkIntersectsRect(player.pos,(21,5,26,9)):
		if "counter1" in game.data.keys():
			counter=game.data["counter1"]
		else: counter=0
		counter+=1
		if counter>=60*20: #20 seconds
			model.targetMap(1)
			i=counter-60*20
			for X in range(22,26):
				if i>=60:
					game.setTile(X,7,246)
					i-=60
			if counter>=60*30:
				for X in range(22,26):
					game.setTile(X,7,-1)
		game.data["counter1"]=counter
	else:
		game.data["counter1"]=0

	if y>30:
		game.loadLevel("$LEVEL/caves/open-air/index")
		# exit between x=16 and x=25, enter between x=47 and x=56
		game.setPos(x+48-16,y+2-30)
