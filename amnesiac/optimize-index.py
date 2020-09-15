
_used_sprite_ids = []
_used_sprites = []

def optimize_index(fname):
    try:
        with open(fname) as f:
            data = f.read().splitlines()
    except IOError:
        return False
    output = []
    for line in data:
        if line.startswith("#"):
            output.append(line)
        elif line.startswith(" "):
            output.append(" "+optimize_line(line.lstrip(" \t")))
        elif line.startswith("\t"):
            output.append("\n"+optimize_line(line.lstrip(" \t")))
        else:
            output.append(optimize_line(line))
    with open(fname,"w") as f:
        f.write("\n".join(output))
    return True

def optimize_line(line):
    if line.startswith("map:"):
        try:
            with open(line[4:]) as f:
                map = [[int(n) for n in l.split(",")] for l in f.read().splitlines()]
        except IOError:
            return "## "+line
        for row in map:
            for col in row:
                if col not in _used_sprite_ids:
                    _used_sprite_ids.append(col)
    elif line.startswith("tex:"):
        _used_sprites.append(line[4:].split(",",maxsplit=1))
        return line


if __name__=='__main__':
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} index.aex")
        exit(1)
    for fname in sys.argv[1:]:
        optimize_index(fname)
