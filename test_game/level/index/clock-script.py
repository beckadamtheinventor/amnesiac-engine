
from pyglet.window import key
import time,math


def init(game):
	pass

def main(game):
	model=game.model
	player=game.player
	keys=game.keys
	x,y = model.x,model.y
	model.targetMap(1)

	def rebased(l,offset):
		o=[]
		for s in l:
			o.append([ord(c)+offset for c in s])
		return o

	month_strings = rebased([" JAN"," FEB"," MAR"," APR"," MAY","JUNE","JULY"," AUG","SEPT"," OCT"," NOV"," DEC"],209-0x20)
	wday_strings = rebased([" MON","TUES"," WED"," THU"," FRI"," SAT"," SUN"],209-0x20)
	
	

	TIME=time.time()
	GMTIME=time.gmtime(TIME)
	YEAR=GMTIME[0]
	MONTH=GMTIME[1]
	DAY=GMTIME[2]
	HOUR=(GMTIME[3]%12) + 1
	APM=GMTIME[3]//12
	MINUTE=GMTIME[4]
	SECOND=GMTIME[5]
	WDAY=GMTIME[6]

	#row to start the time/date info at
	y = 4
	#zero character sprite
	zero = 225

	model.setTile(14,y+1,zero+(SECOND%10))
	model.setTile(13,y+1,zero+(SECOND//10))

	model.setTile(11,y+1,zero+(MINUTE%10))
	model.setTile(10,y+1,zero+(MINUTE//10))

	model.setTile(11,y,zero+(HOUR%10))
	model.setTile(10,y,zero+(HOUR//10))

	if APM: model.setTile(12,y,242) #A
	else: model.setTile(12,y,257) #P
	model.setTile(13,y,254) #M

	XX=16
	for c in wday_strings[WDAY-1]:
		model.setTile(XX,y,c)
		XX+=1

	XX=22
	for c in month_strings[MONTH-1]:
		model.setTile(XX,y,c)
		XX+=1

	MLT=1
	for XX in range(19,17,-1):
		model.setTile(XX,y+1,zero+(DAY//MLT)%10)
		MLT*=10

	MLT=1
	for XX in range(25,21,-1):
		model.setTile(XX,y+1,zero+((YEAR//MLT)%10))
		MLT*=10

