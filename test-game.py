#!/usr/bin/python3
if __name__=='__main__':
    import os
    from amnesiac.engine import RunEngine
    RunEngine("test_game", os.path.dirname(__file__))

