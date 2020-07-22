#!/usr/bin/python3
import os,sys,math,pyglet,importlib.util,json
from pyglet.window import key
from pyglet.gl import *

VERSION = 'v1.0 "Pyglet Edition"'
HEX_C = "0123456789ABCDEF"

class Game:
	def __init__(self,model,player,keys,window):
		self.model=model
		self.player=player
		self.keys=keys
		self.window=window
		self.vars={}
		self.data=None
		self._stack=[]
		self._data={}
	def push(self,val):
		self._stack.append(self.data)
		self.data=val
	def pop(self):
		self.data=self._stack.pop(-1)
	def load_level(self,fname):
		self.model.load_level(fname)
		self.model.enter_level(self.player)
		self.player.level=fname
	def set_pos(self,x,y):
		self.player.move(x,y)
		self.model.set_pos(x,y)
	def set_tile(self,x,y,tile):
		return self.model.setTile(x,y,tile)
	def get_tile(self,x,y):
		return self.model.getTile(x,y)
	def create_entity(self,fname):
		ent=Entity(Script(fname),game=self)
		self.model.add_entity(ent)
		return ent
	def destroy_entity(self,entity):
		self.model.remove_entity(entity)
		del entity

class Script:
	def __init__(self,fname):
		self.fname=fname
		self.sfile="saves/save/"+self.fname+"/save.json"
		spec = importlib.util.spec_from_file_location("*", fname)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		self.module=module
		try:
			os.makedirs(self.sfile.rsplit("/",maxsplit=1)[0])
		except:
			pass
		try:
			with open(self.sfile) as f:
				self.data=json.load(f)
		except:
			self.data={}
	def run_init(self,game):
		game._data[self.fname]=self.data
		self.run_func("init",game)
	def run_main(self,game):
		self.run_func("main",game)
	def run_draw(self,game):
		self.run_func("draw",game)
	def run_save(self,game):
		self.run_func("save",game)
		with open(self.sfile,'w') as f:
			json.dump(self.data,f)
	def run_func(self,func,game):
		game.push(game._data[self.fname])
		if hasattr(self.module,func):
			getattr(self.module,func)(game)
		game.pop()

class Entity:
	def __init__(self,script,x=0,y=0,game=None):
		self.x=x; self.y=y
		self.script=script
		if game is not None:
			self.init(game)
	def create(self,x,y):
		e=Entity(self.script,x,y)
		e.init()
	def init(self,game,x,y):
		script.run_init(game)
	def run(self,game):
		script.run_main(game)
	def draw(self,game):
		script.run_draw(game)

class Player:
	def __init__(self):
		self.pos = [0,0]
		self.movement = [0,0]
		self.speed = 1/8

	def update(self,dt,keys):
		vx=vy=0
		if keys[key.W]: vy-=self.speed
		if keys[key.S]: vy+=self.speed
		if keys[key.A]: vx-=self.speed
		if keys[key.D]: vx+=self.speed
		return vx,vy

	def move(self,x,y):
		self.pos = x,y

	def loadgame(self,fname="saves/save/save"):
		self.pos = [0,0]
		self.level = "data/level/nexus/index"
		self.has_loaded_level=False

		try:
			with open(fname) as f:
				data = f.read().splitlines()
			for line in data:
				if line.startswith("pos:"):
					self.pos = [float(n) for n in line[4:].split(",")]
				elif line.startswith("level:"):
					self.level = line[6:]
				elif line.startswith("has_loaded_level:"):
					if line[17:].startswith("true"):
						self.has_loaded_level=True
		except:
			pass

	def savegame(self,fname="saves/save/save"):
		try:
			os.mkdir(fname.rsplit("/",maxsplit=1)[0])
		except:
			pass
		with open(fname,"w") as f:
			f.write("pos:"+",".join([str(n) for n in self.pos])+"\nlevel:"+self.level+"\nhas_loaded_level:true")


class Model:
	def __init__(self,level=None):
		self.batch = [pyglet.graphics.Batch() for N in range(8)]
		self.none_tex = self.get_tex("data/gfx/tex/tex_None.png")
		self.none_tileset = {"-1":self.none_tex}
		self.sprites = [pyglet.sprite.Sprite(self.none_tex,batch=self.batch[N//(25*25)],x=-1000,y=-1000) for N in range(25*25*8)]
		self.x=self.y=0
		self.level_name=level
		self.drawPlayer=True
		self.playeratlas=[]
		self.scripts=[]
		self.entities=[]
		try:
			for s in ["down","up","left","right"]:
				self.playeratlas.append(self.get_tex("data/gfx/player-"+s+".png"))
			self.playersprite=pyglet.sprite.Sprite(self.playeratlas[0],x=32*7,y=32*7)
			self.playersprite.scale=1
		except:
			pass

		self.solids = []

	def set_game(self,game):
		self.game=game
	
	def set_pos(self,x,y):
		self.x=x; self.y=y

	def add_entity(self,ent):
		self.entities.append(ent)

	def remove_entity(self,ent):
		self.entities.remove(ent)

	def exit_level(self):
		for script in self.scripts:
			script.run_save(self.game)
		try:
			del self.tileset
			del self.level
		except:
			pass

	def enter_level(self,player):
		if player.has_loaded_level:
			self.x,self.y = player.pos
		else:
			self.x,self.y = self.level["start"]
		for script in self.scripts:
			script.run_init(self.game)

	def load_level(self,fname):
		try: self.exit_level()
		except: pass
		self.tileset=self.none_tileset
		self.level={"list":[]}
		p=""
		with open(fname) as f:
			data = f.read().splitlines()
		for line in data:
			if line.startswith("map:"):
				with open(p+line[4:]) as f:
					level={}
					level["area"] = m = [[int(c) for c in l.split(",")] for l in f.read().splitlines()]
					level["height"] = len(m)
					level["width"] = len(m[0])
					self.level["list"].append(level)
			elif line.startswith("tex:"):
				w=line[4:].split(",",maxsplit=1)
				self.tileset[w[0]] = self.get_tex(p+w[1])
			elif line.startswith("start:"):
				c=line[6:].split(",")
				self.level["start"] = [int(c[0]),int(c[1])]
			elif line.startswith("path:"):
				p=line[5:]+"/"
			elif line.startswith("script:"):
				self.scripts.append(Script(p+line[7:]))
			elif line.startswith("solid:"):
				for w in line[6:].split(","):
					self.solids.append(int(w))

	def update(self,vx,vy,keys):
		x=vx+self.x; y=vy+self.y
		m=-1
		if vx>0: m=3
		elif vx<0: m=2
		elif vy>0: m=0
		elif vy<0: m=1
		if m!=-1:
			self.playersprite.image = self.playeratlas[m]
		
		if not self.checkColided(vx,vy):
			self.x,self.y = x,y
		self.tryRunScript(x,y,keys)
	
	def checkColided(self,vx,vy):
		self.targetMap(0)
		X,Y=self.x+vx+.5,self.y+vy+.5
		t=self.getTile(X,Y)
		if t in self.solids or t is None:
			return True
		t=self.getTile(X,Y+.5)
		if t in self.solids or t is None:
			return True
		return False


	def getTile(self,x,y):
		if int(x) in range(self.curlevel["width"]) and int(y) in range(self.curlevel["height"]):
			return self.curlevel["area"][int(y)][int(x)]
		return None

	def setTile(self,x,y,tile):
		if int(x) in range(self.curlevel["width"]) and int(y) in range(self.curlevel["height"]):
			self.curlevel["area"][int(y)][int(x)]=tile
			return True
		return False

	def targetMap(self,mapno):
		self.curlevel=self.level["list"][mapno]

	def tryRunScript(self,x,y,keys):
		xx=int(x); yy=int(y)
		for script in self.scripts:
			script.run_main(self.game)


	def get_tex(self,fname):
		try:
			tex = pyglet.image.load(fname).get_mipmapped_texture()
		except:
			tex = pyglet.image.load("data/gfx/tex/tex_None.png").get_mipmapped_texture()
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
		return tex


	def draw(self):
		self.size_x,self.size_y=self.game.window.get_size()
		self.scale=min(self.size_x,self.size_y)//15
		self.get_tiles([self.x,self.y])
		for i in range(len(self.level["list"])):
			self.batch[i].draw()
		if self.drawPlayer:
			self.playersprite.x = self.size_x/2 - 16
			self.playersprite.y = self.size_y/2 - 16
			self.playersprite.draw()
		for entity in self.entities:
			entity.draw()

	def get_tiles(self,pos):
		x=int(pos[0]); y=int(pos[1])
		fx=(self.x-int(self.x))*self.scale
		fy=-((self.y-1)-int(self.y))*self.scale
		offset=i=0
		for m in self.level["list"]:
			Y = 20*self.scale
			for iy in range(y-12,y+13):
				X=-5*self.scale
				for ix in range(x-12,x+13):
					spr=self.sprites[i]
					tn=-1
					if iy in range(m["height"]) and ix in range(m["width"]):
						tn = int(m["area"][iy][ix])
					if tn!=-1:
						spr.image = self.tileset[str(tn)]
						spr.update(scale=self.scale/32,x=X-fx,y=Y-fy)
					else:
						spr.update(x=-1000,y=-1000)
					X+=self.scale; i+=1
				Y-=self.scale


class Window(pyglet.window.Window):
	def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2])
	def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
	def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()
	def set2d(self): self.Projection(); gluOrtho2D(0,self.width,0,self.height); self.Model()
	#def set3d(self): self.Projection(); gluPerspective(80,self.width/self.height,0.05,1000); self.Model()
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)

		self.set_icon(pyglet.image.load("data/gfx/icon.png"))
		self.player = Player()
		self.player.loadgame()
		self.model = Model(self.player.level)
		self.game=Game(self.model,self.player,self.keys,self)
		self.model.set_game(self.game)
		self.game.load_level(self.player.level)

	def update(self,dt):
		x,y=self.player.update(dt,self.keys)
		self.model.update(x,y,self.keys)
		self.player.move(self.model.x,self.model.y)

	def on_draw(self):
		self.set2d()
		self.clear()
		self.model.draw()

	def on_close(self):
		self.model.exit_level()
		self.player.savegame()
		super().on_close()



if __name__=='__main__':
	win = Window(15*32,15*32,caption="Amnesiac Engine "+VERSION,resizable=False)
	pyglet.app.run()
