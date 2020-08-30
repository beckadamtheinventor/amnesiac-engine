
from amnesiac.build import BuildTarget

class EZ80(BuildTarget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.common_name = "eZ80"
        self.properties["blacklist"] = [
            ".py", ".pyc"
        ]

    def build(self,bin):
        self.lf = open("log.txt",'w')
        if not len(self.files.keys()):
            self.locate_sources()
        self.images = {}
        self.asm_files = {}
        self.tilemap_files = {}
        self.index_files = {}
        self.data_files = {}
        self.script_files = {}
        for file in self.files.keys():
            if self.files[file]["format"] in [".png", ".jpg", ".jpeg"]:
                self.images[file] = self.files[file]
            elif self.files[file]["format"] in [".asm", ".ez80"]:
                self.asm_files[file] = self.files[file]
            elif self.files[file]["format"] in [".csv"]:
                self.tilemap_files[file] = self.files[file]
            elif self.files[file]["format"] in [".aex"]:
                self.index_files[file] = self.files[file]
            elif self.files[file]["format"] in [".amne", ".script"]:
                self.script_files[file] = self.files[file]
            else:
                self.data_files[file] = self.files[file]
        # build graphics first
        # build tilemaps second
        # build other data third
        # build aex index files fourth
        # use convbin to build data into appvars
        # build scripts fifth
        # build assembly source files sixth
        # integrate engine source routines
        # use fasmg to build the executable
        self.lf.close()

def build(directory, bin, properties={}):
    target = EZ80(directory, properties)
    target.build(bin)

if __name__=='__main__':
    from sys import argv
    if len(argv)<3:
        print(f"Usage: {argv[0]} source_dir bin_file")
    build(argv[1],argv[2])

