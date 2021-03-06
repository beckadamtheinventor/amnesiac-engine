
from pyglet.window import key
from amnesiac.game import getGameObject

game = getGameObject()
char_map = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def init():
    if "entered_text" not in game.data.keys():
        game.data["entered_text"] = [0]*10
        game.data["text_cursor"] = 0
    else:
        old_map = game.targetMap(1)
        print_text(game.data["entered_text"],10,16)
        game.targetMap(old_map)
    if "text_cursor" not in game.data.keys():
        game.data["text_cursor"] = 0
    game.data["spacebar_pressed"] = False

def main():
    x,y = game.getPos()
    if game.keys[key.SPACE]:
        if not game.data["spacebar_pressed"]:
            game.data["spacebar_pressed"]=True
            if y<=20:
                changed=False
                pos = game.getPos()
                if game.checkIntersectsTile(pos,(13,20)):
                    game.data["entered_text"][game.data["text_cursor"]]=0
                    changed=True
                elif game.checkIntersectsTile(pos,(15,20)) and game.data["text_cursor"]>0:
                    game.data["text_cursor"]-=1
                    changed=True
                elif game.checkIntersectsTile(pos,(16,20)) and game.data["text_cursor"]<len(game.data["entered_text"])-1:
                    game.data["text_cursor"]+=1
                    changed=True
                elif game.checkIntersectsTile(pos,(17,20)):
                    game.data["entered_text"][game.data["text_cursor"]] = (game.data["entered_text"][game.data["text_cursor"]]+1)%27
                    changed=True
                elif game.checkIntersectsTile(pos,(18,20)):
                    game.data["entered_text"][game.data["text_cursor"]] = (game.data["entered_text"][game.data["text_cursor"]]-1)%27
                    changed=True
                if changed:
                    old_map = game.targetMap(0)
                    game.setTile(pos[0],pos[1]+1,18)
                    game.targetMap(1)
                    print_text(game.data["entered_text"], 10, 16)
                    game.targetMap(old_map)
    else:
        game.data["spacebar_pressed"]=False

    text = "".join([char_map[a] for a in game.data["entered_text"]])
    if text == "EXIT______":
        reset()
        game.loadLevel("$LEVEL/caves/open-air/index")
        game.setPos(43.5,32.5)



def reset():
    game.data["text_cursor"] = 0
    game.data["spacebar_pressed"] = False
    for i in range(len(game.data["entered_text"])):
        game.data["entered_text"][i] = 0

def print_text(text,x,y):
    for c in text:
        if type(c) is str:
            n = ord(c)
        else:
            n = ord(char_map[c])
        game.setTile(int(x),y,209+n-0x20)
        x+=1

