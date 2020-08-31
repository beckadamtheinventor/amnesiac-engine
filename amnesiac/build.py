
import os,sys
from amnesiac.util import fwalk


class BuildTarget:
    def __init__(self,directory,properties={}):
        self.common_name = "Python+Pyglet"
        self.properties = properties
        self.directory = directory
        self.files = {}

    def error(self,*args,**kwargs):
        self.log("Error:\n", *args, f"\nBuild of {self.directory} for target {self.common_name} failed.", **kwargs)
        exit(1)

    def log(self,*args,**kwargs):
        stdout = sys.stdout
        sys.stdout = self.lf
        print(*args,**kwargs)
        sys.stdout = stdout
        print(*args,**kwargs)

    def locate_sources(self,directory=None):
        if directory is None:
            directory = self.directory
        for file in fwalk(directory):
            if "blacklist" in self.properties:
                if os.path.splitext(file)[1] in self.properties["blacklist"]:
                    self.log(f"Warning: Ignoring blacklisted source type for build target {self.common_name}: {file}")
            if "whitelist" in self.properties:
                if os.path.splitext(file)[1] not in self.properties["whitelist"]:
                    self.log(f"Warning: Ignoring non-whitelisted source type for build target {self.common_name}: {file}")
            self.files[file] = {"file":file, "name":os.path.splitext(file)[0], "format":os.path.splitext(file)[1]}
        return self.files

    def build(self, bin):
        self.lf = open("log.txt", 'w')
        from zipfile import ZipFile
        from shutil import copytree
        if not len(self.files.keys()):
            self.locate_sources()
        if os.path.splitext(bin)[1] == '.zip':
            with ZipFile(bin,"w") as f:
                for file in self.files:
                    f.write(file)
        else:
            copytree(self.directory,bin+"/data")
            with open(bin+"/launch.py","w") as f:
                f.write(f"""
if __name__=='__main__':
    from os.path import dirname
    from amnesiac.engine import RunEngine
    RunEngine(dirname(__file__)+"/{bin}")
""")
        self.lf.close()


def BuildPython(directory, bin, properties={}):
    target = BuildTarget(directory, properties)
    target.build(bin)


if __name__=='__main__':
    from sys import argv
    if len(argv)<3:
        print(f"Usage: {argv[0]} source_dir bin_file")
        exit(1)
    BuildPython(argv[1],argv[2])
