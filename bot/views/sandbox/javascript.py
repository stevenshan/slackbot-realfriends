from io import StringIO
import sys
import os
import traceback
from timeout_decorator import timeout
import node_vm2

# plus 10 seconds because node is weird
TIME_LIMIT = int(os.environ.get("TIME_LIMIT", 1)) + 10

safe_modules = ["re", "math", "random", "time"]

class TimeLimit(Exception):
    pass

@timeout(TIME_LIMIT, use_signals=False, timeout_exception=TimeLimit)
def _execute(text):
    output = StringIO()
    sys.stdout = output
    sys.stderr = output

    try:
        node_vm2.NodeVM.code(text)
    except:
        traceback.print_exc(limit=1)

    return output.getvalue()

def execute(text):

    try:
        result = _execute(text)
    except TimeLimit:
        result = ("TimeLimit: exceeded time limit of %s seconds" %
                  TIME_LIMIT)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    return result
