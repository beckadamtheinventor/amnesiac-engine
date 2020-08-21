
from pyglet.window import key

class Ghost:
	def __init__(self):
		self.x=self.y=0
		self.spr=None
		self.img=None
		self.atlas=None
	def update(self,vx,vy):
		m=-1
		if vx==0:
			if vy>0: m=0
			elif vy<0: m=1
		elif vy==0:
			if vx>0: m=3
			elif vx<0: m=4
		self.x+=vx
		self.y+=vy
		if m!=-1:
			self.img=self.atlas[m]

	def draw(self):
		if self.spr is not None:
			self.spr.x=self.x
			self.spr.y=self.y
			self.spr.image=self.img
			self.spr.draw()

def init(game):
	model=game.model
	player=game.player
	keys=game.keys
	mx,my = model.x,model.y
	game.vars["ghost"]=ghost=Ghost()
	ghost.x=x
	ghost.y=y
	ghost.atlas=[model.get_tex("data/gfx/entity/ghost-"+f+".png") for f in ["up","down","left","right"]]
	ghost.spr = pyglet.sprite.Sprite(None)
	ghost.spr.scale=2

def update(game):
	vx=vy=0
	model=game.model
	x=model.x - ghost.x
	y=model.y - ghost-y
	if x>0: x=1
	elif x<0: x=-1
	if y>0: y=1
	elif y<0: y=-1
	ghost=game.vars["ghost"]
	ghost.update(x,y)

def draw(game):
	ghost.draw()

