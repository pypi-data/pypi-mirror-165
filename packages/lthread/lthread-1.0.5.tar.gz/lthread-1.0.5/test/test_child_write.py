import sys
import traceback
from lthread import *
import lthread.subprocess as sp
getdispatcher()

@asyncfunc
def main():
    proc = sp.ChildProcess('cat', mode = sp.M_STDIN)
    try:
        for i in xrange(32):
            yield proc.tochild.write('foobar\n')
        proc.tochild.close()
    except (IOError, OSError):
        traceback.print_exc()
    yield proc.wait()
    getdispatcher().quitloop()
        
main().start()
try:
    getdispatcher().loop()
except KeyboardInterrupt:
    pass



