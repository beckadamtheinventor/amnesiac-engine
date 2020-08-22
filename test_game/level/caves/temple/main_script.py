
from pyglet.window import key


def init(game):
    if "entered_text" not in game.data.keys():
        game.data["entered_text"] = [0]*10
        game.data["text_cursor"] = 0
    else:
        old_map = game.targetMap(1)
        print_text(game,game.data["entered_text"],10,16)
        game.targetMap(old_map)
    if "text_cursor" not in game.data.keys():
        game.data["text_cursor"] = 0
    game.data["spacebar_pressed"] = False

def main(game):
    x,y = game.getPos()
    if game.keys[key.SPACE]:
        if not game.data["spacebar_pressed"]:
            game.data["spacebar_pressed"]=True
            if y<=20:
                old_map = game.targetMap(1)
                changed=False
                if int(x)==13:
                    game.data["entered_text"][game.data["text_cursor"]]=0
                    changed=True
                elif int(x)==15 and game.data["text_cursor"]>0:
                    game.data["text_cursor"]-=1
                    changed=True
                elif int(x)==16 and game.data["text_cursor"]<len(game.data["entered_text"])-1:
                    game.data["text_cursor"]+=1
                    changed=True
                elif int(x)==17:
                    game.data["entered_text"][game.data["text_cursor"]] = (game.data["entered_text"][game.data["text_cursor"]]+1)%27
                    changed=True
                elif int(x)==18:
                    game.data["entered_text"][game.data["text_cursor"]] = (game.data["entered_text"][game.data["text_cursor"]]-1)%27
                    changed=True
                if changed:
                    print_text(game, game.data["entered_text"], 10, 16)
                game.targetMap(old_map)
    else:
        game.data["spacebar_pressed"]=False


def print_text(game,text,x,y):
    char_map = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(10):
        game.setTile(x+i,y,0)
    for c in text:
        if type(c) is str:
            n = ord(c)
        else:
            n = ord(char_map[c])
        game.setTile(int(x),y,209+n-0x20)
        x+=1

