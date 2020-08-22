

def init():
	if "passed_intro" in game.data:
		if game.data["passed_intro"]:
			return
	game.enterCutscene(drawplayer=True)

	game.data["frame_counter"]=0
	game.data["passed_intro"]=False


def main():
	if not game.data["passed_intro"]:
		entity = game.loadEntity("$LEVEL/chapter-1/intro_entity.py")
		counter = game.data["frame_counter"]
		if int(counter) >= 100:
			game.setTileRenderMode()
			game.data["passed_intro"] = True
			game.exitCutscene()
			return
		elif int(counter) >= 80:
			pass

		game.data["frame_counter"] = counter+game.dt
