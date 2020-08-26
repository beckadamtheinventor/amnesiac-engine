
import os
if __name__=='__main__':
    try:
        os.system("python setup.py build")
    except:
        pass
    os.system(f"pip install {os.path.dirname(__file__)}")
