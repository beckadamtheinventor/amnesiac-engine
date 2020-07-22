
from pyglet.window import key

def main(game):
	model=game.model
	player=game.player
	x,y = model.x,model.y
	#crossing x=63 between y=25 and y=38
	if y>=24 and y<38 and x<7:
		game.load_level("data/level/caves/main/index")
		game.set_pos(71,y)
	#y=31 between x=29 and x=30
	elif y>=30 and y<=32.5 and x>=43 and x<=44:
		if game.keys[key.SPACE]:
			game.load_level("data/level/caves/main/index")
