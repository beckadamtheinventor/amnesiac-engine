
def setGamePath(dir):
    buildGameFolders(dir)

def buildGameFolders(dir):
    global GFX_FOLDER, GAME_FOLDER
    GAME_FOLDER = dir
    GFX_FOLDER = GAME_FOLDER + "/gfx"

VERSION = 'v1.0 "Pyglet Edition'
HEX_C = "0123456789ABCDEF"


