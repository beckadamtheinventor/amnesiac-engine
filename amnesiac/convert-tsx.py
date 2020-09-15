
import xml.etree.ElementTree as ET
import os

if __name__=='__main__':
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} data_dir tsx_file")
        exit(1)

    fname = sys.argv[2]
    datadir = os.getcwd()+"/"+sys.argv[1]
    basepath = os.path.dirname(fname)
    scriptpath = os.path.dirname(__file__)
    ofile = scriptpath+"/tile-index.aex"

    try:
        tree = ET.parse(fname)
    except:
        print(f"Error: Could not open or could not parse file \"{fname}\".")
        exit(1)

    root = tree.getroot()
    with open(ofile,'w') as ofile:
        for child in root:
            if child.tag == "tile":
                ID = child.attrib["id"]
                for ichild in child:
                    p = "$DATA/"+os.path.relpath(os.path.abspath(basepath+"/"+ichild.attrib["source"]),datadir).replace("\\","/")
                    ofile.write(f"tex:{ID},{p}\n")
                    break
