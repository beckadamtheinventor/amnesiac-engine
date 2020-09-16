
from amnesiac.build import BuildTarget
from random import randrange
import os.path

class EZ80(BuildTarget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.common_name = "eZ80"
        self.properties["blacklist"] = [
            ".py", ".pyc"
        ]
        self.load_cache()
        if "unique_name" not in self.properties.keys():
            self.properties["unique_name"] = "".join([chr(randrange(0x41,0x5A)) for _ in range(7)])
        self.properties["tile_appvar"] = "Y" + self.properties["unique_name"]
        self.properties["gfx_appvar"] = "Z" + self.properties["unique_name"]
        self.save_cache()

    def build(self, bin):
        from sys import stdout
        os.chdir(self.directory)
        try:
            os.makedirs("ez80-bin")
        except IOError:
            pass
        self.lf = open("log.txt",'w')
        self.log("searching for sources...")
        if not len(self.files.keys()):
            self.locate_sources()
        self.index_files = {}
        for file in self.files.keys():
            if self.files[file]["format"] in [".aex"]:
                self.index_files[file] = self.files[file]


        # build index files
        self.levels = []
        for fname in self.index_files.keys():
            self._cur_level = {"maps":[], "sprites":[], "scripts":[]}
            self.levels.append(self._cur_level)
            self._load_index(fname)

        self.script_files = []
        self.images = []
        self.tilemap_files = []
        self.data_files = []
        for lvl in self.levels:
            for map in lvl["maps"]:
                if map not in self.tilemap_files:
                    self.tilemap_files.append(map)
            for sprite in lvl["sprites"]:
                if sprite not in self.images:
                    self.images.append(sprite)
            for script in lvl["scripts"]:
                if script not in self.script_files:
                    self.script_files.append(script)

        # build graphics
        self.log("building sprites...")
        img_list = "\n        - ".join([path[1:] for path in self.images])
        with open("convimg.yaml",'w') as f:
            f.write(f"""
converts:
    - name: myimages
      palette: xlibc
      images:
        - {img_list}

outputs:
    - type: appvar
      converts:
        - myimages
      name: {self.properties["gfx_appvar"]}
      directory: {self.directory}/ez80-bin
      archived: true
      compress: zx7
""")
        os.system("convimg")

        # build tilemaps
        self.log("building tilemaps...")
        self.tile_dict = {}
        tile_num = 0
        defined_tiles = []
        for tfname in self.tilemap_files:
            self.log(f"Scanning {tfname}")
            try:
                with open(tfname) as f:
                    data = [[int(c) for c in s.split(",")] for s in f.read().splitlines()]
            except IOError:
                self.log(f"Failed to open {tfname}")
                continue
            for row in data:
                for c in row:
                    if c not in defined_tiles:
                        self.tile_dict[c] = tile_num
                        defined_tiles.append(c)
                        tile_num += 1
        if len(self.tile_dict.keys())>256:
            self.error(f"ez80 builds only support up to 256 unique tiles at this time. {str(len(self.tile_dict.keys()))} are in use.")
        self.map_output = [0,0]*len(self.tilemap_files)
        tnum = 0
        tdict = {}
        for tfname in self.tilemap_files:
            self.log(f"Building {tfname}")
            try:
                with open(tfname) as f:
                    data = [[int(c) for c in s.split(",")] for s in f.read().splitlines()]
            except IOError:
                self.log(f"Failed to open {tfname}")
                continue
            tdict[tfname] = tnum
            w = len(data[0]); h = len(data)
            self.map_output[tnum*2] = len(self.map_output)%256
            self.map_output[tnum*2+1] = (len(self.map_output)//256)%256
            self.map_output.extend([w,h])
            tnum+=1
            map = []
            for row in data:
                for c in row:
                    map.append(self.tile_dict[c])
            self.map_output.extend(self.zx7_Compress(map))
        with open("tilemaps.bin","wb") as f:
            f.write(bytes(self.map_output))

        os.system(f"convbin -i tilemaps.bin -o ez80-bin/{self.properties['tile_appvar']}.8xv -j bin -k 8xv \
-n {self.properties['tile_appvar']}")

        os.remove("tilemaps.bin")
        #os.remove("convimg.yaml")
        os.remove("temp.bin")
        os.remove("temp_output.bin")

        # build other data

        # build scripts
        for script in self.script_files:
            ext = os.path.splitext(script)[1]
            if ext in [".script", ".amne"]:
                self._build_script(script)
        # build assembly source files
        self._script_data = []
        for script in self.script_files:
            ext = os.path.splitext(script)[1]
            if ext in [".asm", ".ez80"]:
                try:
                    with open(script) as f:
                        data = f.read()
                except IOError:
                    continue
                self._script_data.append(data)
        try:
            with open("ez80-build/obj/asm-scripts.asm",'w') as f:
                f.write("\n\n\n".join(self._script_data))
        except IOError:
            self.log("Failed to write asm object: ez80-build/obj/asm-scripts.asm")
            self.lf.close()
            return

        # integrate engine source routines
        import git
        git.Git(self.directory).clone("")


        # use fasmg to build the executable
        os.system(f"fasmg ez80-build/obj/main.asm ez80-build/X{self.properties['unique_name']}.8xp")
        self.lf.close()

    def _build_script(self, fname):
        pass

    def _load_index(self,fname):
        try:
            with open(fname) as f:
                data = f.read().splitlines()
        except IOError:
            return

        self._cur_target = "default"
        self._cur_path = ""
        self._prev_line = "#"
        for line in data:
            if not line.startswith("#"):
                if line.startswith(" ") or line.startswith("\t"):
                    self._load_index_line(line[1:])
                else:
                    self._load_index_line(line)

    def _load_index_line(self,line):
        if len(line.split(":",maxsplit=1))==2:
            if line.startswith("index:"):
                self._load_index(self.pathrep(self._cur_path + "/" + line[5:]))
            elif line.startswith("target:"):
                self._cur_target = line[7:].lower()
            elif line.startswith("path:"):
                self._cur_path = self.pathrep(line[5:])
            elif line.startswith("map:"):
                self._cur_level["maps"].append(self.pathrep(self._cur_path + "/" + line[4:]))
            elif line.startswith("tex:"):
                self._cur_level["sprites"].append(self.pathrep(self._cur_path + "/" + line[4:].split(",",maxsplit=1)[1]))
        else:
            self._prev_line = line

    def zx7_Compress(self,data):
        with open("temp.bin",'wb') as f:
            f.write(bytes(data))
        os.system("convbin -i temp.bin -o temp_output.bin -j bin -k bin -c zx7")
        with open("temp_output.bin",'rb') as f:
            return list(f.read())

    def _zx7_Compress(self,data):
        self.zoutput = []
        self.input_index = 1
        self.output_index = 0
        self.bit_index = 0
        self.bit_mask = 0x80
        self._write_byte(data[0])
        while self.input_index<len(data):
            search_index = 0
            best_len = 0; best_index = 0; best_cost = 0xFFFFFF
            while self.input_index + search_index > 0:
                search_index -= 1
                if data[self.input_index] == data[self.input_index + search_index]:
                    search_len = 0
                    while search_index + search_len < 0:
                        search_len+=1
                        if data[self.input_index + search_len] != data[self.input_index + search_index + search_len]:
                            break
                    cost = self._get_cost(search_len, -search_index)
                    if cost<best_cost:
                        best_cost = cost
                        best_len = search_len
                        best_index = search_index
            if best_cost < best_len*9:
                self._write_bit(1)
                i = 2
                while i <= best_len:
                    i *= 2
                    self._write_bit(0)
                while i > 0:
                    i //= 2
                    self._write_bit(best_len & i)


    def _get_cost(Len, index):
        a = 13 if index>128 else 9
        a += 1
        while Len > 1:
            a += 2
            Len //= 2
        return a

    def _write_byte(self,byte):
        self.zoutput.append(byte)
        self.output_index+=1

    def _write_bit(self,bit):
        self.zoutput[self.bit_index] |= self.bit_mask
        self.bit_mask//=2
        if not self.bit_mask:
            self.bit_mask = 0x80
            self.bit_index = self.output_index
            self.output_index += 1


def build(directory, bin, properties={}):
    target = EZ80(directory, properties)
    target.build(bin)

if __name__=='__main__':
    from sys import argv
    if len(argv)<3:
        print(f"Usage: {argv[0]} source_dir bin_file")
        exit(1)
    build(argv[1],argv[2])

