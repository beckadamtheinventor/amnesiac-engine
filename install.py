
import os
if __name__=='__main__':
    try:
        os.system("python setup.py build")
    except:
        pass
    f = os.path.dirname(__file__)
    if not len(f):
        f = "."
    os.system(f"pip install {f}")
