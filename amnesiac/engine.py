#!/usr/bin/python3

def RunEngine(path, base_path):
    """Start the engine, loading game from path."""
    import pyglet
    from amnesiac.globs import VERSION, setGamePath
    from os.path import dirname,relpath
    if not len(base_path):
        setGamePath("./"+path)
    else:
        setGamePath(base_path+"/"+path)
    from amnesiac.window import Window
    win = Window(15 * 32, 15 * 32, caption="Amnesiac Engine " + VERSION, resizable=False)
    pyglet.app.run()

