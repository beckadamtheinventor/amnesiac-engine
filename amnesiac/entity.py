

class Entity:
    def __init__(self, script, x=0, y=0):
        self.x = x
        self.y = y
        self.script = script
        self.script.run_init()

    def create(self, x, y):
        return Entity(self.script, x, y)

    def update(self):
        self.script.run_main()

    def draw(self):
        self.script.run_draw()
