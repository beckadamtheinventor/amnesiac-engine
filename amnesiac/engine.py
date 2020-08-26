#!/usr/bin/python3

def RunEngine(path):
    """Start the engine, loading game from path."""
    import pyglet
    from amnesiac.globs import VERSION, setGamePath
    setGamePath(path)
    from amnesiac.window import Window
    win = Window(15 * 32, 15 * 32, caption="Amnesiac Engine " + VERSION, resizable=False)
    pyglet.app.run()
