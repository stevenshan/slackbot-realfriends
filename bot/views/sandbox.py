from io import StringIO
import sys
import os
import traceback
import signal

RECURSION_LIMIT = int(os.environ.get("RECURSION_LIMIT", 50))
TIME_LIMIT = int(os.environ.get("TIME_LIMIT", 1))

environment = {
    "abs": abs,
    "delattr": delattr,
    "hash": hash,
    "set": set,
    "all": all,
    "dict": dict,
    "help": help,
    "min": min,
    "setattr": setattr,
    "any": any,
    "dir": dir,
    "hex": hex,
    "next": next,
    "slice": slice,
    "ascii": ascii,
    "divmod": divmod,
    "id": id,
    "object": object,
    "sorted": sorted,
    "bin": bin,
    "enumerate": enumerate,
    "oct": oct,
    "staticmethod": staticmethod,
    "bool": bool,
    "int": int,
    "str": str,
    "isinstance": isinstance,
    "ord": ord,
    "sum": sum,
    "bytearray": bytearray,
    "filter": filter,
    "issubclass": issubclass,
    "pow": pow,
    "super": super,
    "bytes": bytes,
    "float": float,
    "iter": iter,
    "print": print,
    "tuple": tuple,
    "callable": callable,
    "format": format,
    "len": len,
    "property": property,
    "type": type,
    "chr": chr,
    "frozenset": frozenset,
    "list": list,
    "range": range,
    "vars": vars,
    "classmethod": classmethod,
    "getattr": getattr,
    "locals": locals,
    "repr": repr,
    "zip": zip,
    "globals": globals,
    "map": map,
    "reversed": reversed,
    "complex": complex,
    "hasattr": hasattr,
    "max": max,
    "round": round,
}

def safe_import(__import__, module_whitelist):
    def _safe_import(module_name, globals={},
                     locals={}, fromlist=[], level=-1):
        if module_name in module_whitelist:
            return __import__(
                module_name,
                globals,
                locals,
                fromlist,
                level
            )
        else:
            raise ImportError("Cannot import %s" % module_name)
    return _safe_import

safe_modules = ["re", "math", "random", "time"]

class TimeLimit(Exception):
    pass

def execute(text):
    output = StringIO()

    _recursionLimit = sys.getrecursionlimit()
    sys.setrecursionlimit(RECURSION_LIMIT)

    def signal_handler(signum, frame):
        raise TimeLimit("Exceeded maximum time limit of %s second(s)" %
                        TIME_LIMIT)

    sys.stdout = output
    sys.stderr = output

    try:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(TIME_LIMIT)

        _environment = dict(environment)
        _environment["__builtins__"] = {
            "__import__": safe_import(__import__, safe_modules)
        }
        exec(text, _environment)
    except:
        traceback.print_exc(limit=5)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    sys.setrecursionlimit(_recursionLimit)

    return output.getvalue()
