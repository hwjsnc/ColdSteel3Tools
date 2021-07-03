#!/usr/bin/env python3
# use as: packCLI.py action installpath projectname [modulelist [...]]
# where action is "pack" or "unpack"

import sys
from unpacker.unpacker import unpack
from packer.packer import pack

action, path, projectName, *moduleList = sys.argv[1:]

if action == "unpack":
    f = unpack
elif action == "pack":
    f = pack
else:
    raise RuntimeError(f"invalid action: {action}")

if moduleList:
    f(path, projectName, moduleList=moduleList)
else:
    f(path, projectName)
