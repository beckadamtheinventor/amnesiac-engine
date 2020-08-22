
from amnesiac.globs import *

def pathrep(p):
    """
    Converts "$" directives into paths.
    Currently supports $GFX, $LEVEL, and $DATA; corresponding to game_dir/gfx, game_dir/level, and game_dir
    :param p: path to convert.
    """
    return p.replace("$GFX", GFX_FOLDER).replace("$DATA", GAME_FOLDER).replace("$LEVEL", GAME_FOLDER + "/level")

