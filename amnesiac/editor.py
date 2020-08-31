
import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
from amnesiac.globs import *
from amnesiac.build import BuildTarget


class EditorObject:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self._associations = {}

    def associate(self, routine, button, modifiers):
        self._associations[str(button)+"+"+str(modifiers)] = routine

    def click(self, x, y, button, modifiers):
        k = str(button) + "+" + str(modifiers)
        if k in self._associations.keys():
            self._associations[k](x, y)

    def drag(self, x, y, dx, dy, button, modifiers):
        k = str(button) + "+" + str(modifiers)
        if k in self._associations.keys():
            self._associations[k](x, y, dx, dy)

    def is_hovered(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class EditorContext:
    def __init__(self):
        self._objects = []

    def __iter__(self):
        for obj in self._objects:
            yield obj

    def add_object(self, obj):
        self._objects.append(obj)


class EditorModel:
    def __init__(self, directory):
        self.batch = pyglet.graphics.Batch()
        self.context = EditorContext()
        self.builder = BuildTarget(directory)
        self.directory = directory
        button1 = EditorObject(0, 0, 200, 200)
        button1.associate(self.build, mouse.LEFT, 0)
        self.context.add_object(button1)

    def build(self, x, y):
        self.builder.build(self.directory)

    def draw(self):
        self.batch.draw()

    def click(self, x, y, button, modifiers):
        for obj in self.context:
            if obj.is_hovered(x, y):
                obj.click(x, y, button, modifiers)


class EditorWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = EditorModel(GAME_FOLDER)

    def on_draw(self):
        self.model.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass


if __name__ == '__main__':
    from os import getcwd
    setGamePath(getcwd())
    win = EditorWindow(640, 480, f"Amnesiac Editor {VERSION}")
    pyglet.app.run()
