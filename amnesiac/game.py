

game = None

class Game:
    """
    Main engine interface class.
    Initialized internally.
    User scripts can access the main instance of this class with the following:
        from amnesiac.game import game
    """

    def __init__(self, model, player, keys, window):
        """
        Only should be used internally. Initializes engine interface object.
        """
        self.model = model
        self.player = player
        self.keys = keys
        self.window = window
        self.vars = {}
        self.data = None
        self.entities = {}
        self.dt = 0
        self._stack = []
        self._data = {}

    def push(self, val):
        """
        pushes game.data to internal game data stack and set game.data to val.
        :param val: dictionary object to set game.data with.
        :return: old game.data.
        """
        self._stack.append(self.data)
        self.data = val
        return self._stack[-1]

    def pop(self):
        """
        restore game.data from internal game data stack.
        :return: old game.data
        """
        rv = self.data
        self.data = self._stack.pop(-1)
        return rv

    def loadLevel(self, fname):
        """
        Load a level from a level index file and start it.
        :param fname: level index file to load level from.
        :return: old level name
        """
        oname = self.player.level
        self.model.load_level(fname)
        self.model.enter_level(self.player)
        self.player.level = fname
        return oname

    def setPos(self, x, y):
        """
        Set player position in current level.
        :param x: new player x.
        :param y: new player y.
        :return: tuple of old player coordinates.
        """
        ox, oy = self.player.pos
        self.player.move(x, y)
        self.model.setPos(x, y)
        return (ox, oy)

    def getPos(self):
        """
        Get player position.
        :return: tuple of player coordinates.
        """
        x, y = self.player.pos
        return (x, y)

    def setTile(self, x, y, tile):
        """
        Set a tile in the currently targeted tilemap.
        :param x: x position of tile in currently targeted tilemap.
        :param y: y position of tile in currently targeted tilemap.
        :param tile: tile ID to set to.
        :return: True if success, False if position is outside the tilemap.
        """
        return self.model.setTile(x, y, tile)

    def getTile(self, x, y):
        """
        Get a tile in the currently tageted tilemap
        :param x: x position of tile in currently targeted tilemap.
        :param y: y position of tile in currently targeted tilemap.
        :return: tile ID of tile at (x,y) in currently targeted tilemap, or None if position is outside the tilemap.
        """
        return self.model.getTile(x, y)

    def loadEntity(self, fname, id=0):
        """
        Find an entity or create one if it does not exist. Use this to create entities instead of Game.createEntity.
        :param fname: entity script file.
        :param id: entity ID.
        :return: existing or new entity object.
        """
        name = fname + "/." + str(id)
        if name not in self.entities.keys():
            return self.createEntity(fname, id)
        return self.entities[name]

    def createEntity(self, fname, id=0):
        """
        Create an entity from an entity script file and an ID.
        :param fname: entity script file.
        :param id: entity ID.
        :return: new entity object.
        """
        name = fname + "/." + str(id)
        ent = Entity(Script(fname), game=self)
        self.entities[name] = ent
        self.model.add_entity(ent)
        return ent

    def destroyEntity(self, fname, id=0):
        """
        Delete an entity.
        :param fname: entity script file.
        :param id: entity ID.
        :return: True if success, otherwise False.
        """
        name = fname + "/." + str(id)
        if name in self.entities.keys():
            self.model.remove_entity(self.entities[name])
            del self.entities[name]
            return True
        return False

    def setTileRenderMode(self):
        """
        Set engine render mode to tile-based. Default.
        :return: old render mode.
        """
        rv = self.model.renderMode
        self.model.renderMode = 0
        return rv

    def setImageRenderMode(self):
        """
        Set engine render mode to image-based. Useful for cutscenes.
        :return: old render mode.
        """
        rv = self.model.renderMode
        self.model.renderMode = 1
        return rv

    def setNoRenderMode(self):
        """
        Set engine render mode to manual only. The engine will only draw entities and manually configured sprites. Useful for menus.
        :return: old render mode.
        """
        rv = self.model.renderMode
        self.model.renderMode = 2
        return rv

    def getTileRenderMode(self):
        """
        Test engine render mode is set to tile mode.
        :return: True if engine render mode is set to tile mode.
        """
        return (self.model.renderMode == 0)

    def getImageRenderMode(self):
        """
        Test engine render mode is set to image mode.
        :return: True if engine render mode is set to image mode.
        """
        return (self.model.renderMode == 1)

    def getNoRenderMode(self):
        """
        Test engine render mode is set to manual mode.
        :return: True if engine render mode is set to manual mode.
        """
        return (self.model.renderMode == 2)

    def setImageRenderImage(self, fname=None, x=0, y=0):
        """
        Set image to be rendered in image render mode.
        :param fname: image file or image/sprite object to draw.
        :param x: x position to draw the image at.
        :param y: y position to draw the image at.
        :return: Old image object
        """
        return self.model.setImage(fname, x, y)

    def enterCutscene(self, drawplayer=False, lockplayer=True):
        """
        Enter a cutscene, saving current configuration.
        :param drawplayer: Boolean of whether to draw the player.
        :param lockplayer: Boolean of whether to allow the player to move.
        :return: How many cutscenes are active or paused.
        """
        return self.model.enterCutscene(drawplayer, lockplayer)

    def exitCutscene(self):
        """
        Exit a cutscene, restoring previous cutscene/state.
        :return: How many cutscenes remain active or paused.
        """
        return self.model.exitCutscene()

    def drawSprite(self, img, x=0, y=0, scale_x=None, scale_y=None):
        """
        Draw a sprite. Sprites are drawn in the order they are defined, and are drawn upon the next engine draw frame.
        :param img: Image file or image/sprite object to draw.
        :param x: x position on screen to draw the sprite at.
        :param y: y position on screen to draw the sprite at.
        :param scale_x: x scale of drawn sprite
        :param scale_y: y scale of drawn sprite
        :return: How many sprites will be drawn next frame.
        """
        if scale_y is None:
            if scale_x is not None:
                self.model.draw_item_scale(scale_x)
        elif scale_x is not None:
            self.model.draw_item_scale(scale_x, scale_y)
        if type(img) is str:
            img = self.model.get_tex(pathrep(img))
        return self.model.draw_sprite(img, x, y)

    def targetMap(self,mapno=0):
        """
        Target a tilemap layer for editing. This allows for levels to have multiple map layers, all editable.
        :param mapno: Tilemap layer to direct subsequent calls to getTile, setTile, etc.
        :return: previously targetted map
        """
        return self.model.targetMap(mapno)

    def setKeyHandler(self,key,func):
        self.model.setKeyHandler(key,func)


def makeGameObject(model, player, keys, window):
    game = Game(model, player, keys, window)

