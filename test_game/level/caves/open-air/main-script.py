
from pyglet.window import key

def main(game):
	model=game.model
	player=game.player
	x,y = model.x,model.y
	#crossing x=63 between y=25 and y=38
	if y>=24 and y<38 and x<7:
		game.loadLevel("$LEVEL/caves/main/index")
		game.setPos(71+x-7,y)
	#y=31 between x=29 and x=30
	elif y>=30 and y<=32.5 and x>=43 and x<=44:
		if game.keys[key.SPACE]:
			game.loadLevel("$LEVEL/caves/main/index")
	# exit between x=47 and x=56
	elif y<=2 and x>=47 and x<=56:
		game.loadLevel("$LEVEL/index/index")
		game.setPos(x+16-47,y+30-2)