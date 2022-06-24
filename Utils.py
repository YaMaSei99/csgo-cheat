import pymem
import re

def get_sig(handle, moduleName, pattern, extra = 0, offset = 0, b_relative = True):
    module = pymem.process.module_from_name(handle.process_handle, moduleName)
    bytes = handle.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    absolute = handle.read_int(module.lpBaseOfDll + match + offset) + extra
    relative = handle.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(relative) if b_relative else "0x{:X}".format(absolute)