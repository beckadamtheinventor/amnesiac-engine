
GAME_FOLDER = None
GFX_FOLDER = None

def buildGameFolders(dir):
    try:
        GAME_FOLDER = dir
    except:
        GAME_FOLDER = "data"
    GFX_FOLDER = GAME_FOLDER + "/gfx"

VERSION = 'v1.0 "Pyglet Edition'
HEX_C = "0123456789ABCDEF"


