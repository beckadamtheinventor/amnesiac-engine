
def setGamePath(dir):
    buildGameFolders(dir)

def buildGameFolders(dir):
    global GFX_FOLDER, GAME_FOLDER
    try:
        GAME_FOLDER = dir
    except:
        GAME_FOLDER = "data"
    GFX_FOLDER = GAME_FOLDER + "/gfx"

VERSION = 'v1.0 "Pyglet Edition'
HEX_C = "0123456789ABCDEF"


