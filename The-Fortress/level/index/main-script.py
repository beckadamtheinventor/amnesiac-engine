
def init(game):
	if "intro_counter" not in game.data:
		game.data["intro_counter"]=0
	game.data["enter_cutscene"]=True

def main(game):
	counter=game.data["intro_counter"]
	if game.data["enter_cutscene"]:
		game.model.enterCutscene(drawPlayer=False)
		game.data["enter_cutscene"]=False
	elif counter==0:
		game.setPos(0,10)
	else:
		game.model.exitCutscene()
	game.data["intro_counter"]=counter+1
