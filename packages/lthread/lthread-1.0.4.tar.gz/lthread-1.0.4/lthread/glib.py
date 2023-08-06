from __future__ import absolute_import

try:
    import glib
except ImportError:
    import gobject
    glib = gobject

from lthread.core import *

def _idlefunc(func, args):
    func(*args)
    return False

def io_cb(source, condition, func, args):
    func(*args)
    return False

class GLibDispatcher(Dispatcher):
    def __init__(self):
        pass

    def set_timer(self, time, func, *args):
        return glib.timeout_add(int(time * 1000), func, *args)
        
    def io_add(self, fd, read, func, *args):
        mode = ((glib.IO_IN if read else
                 glib.IO_OUT) |
                glib.IO_ERR |
                glib.IO_HUP)
        return glib.io_add_watch(fd, mode, io_cb, func, args)


    def cancel_io(self, token):
        glib.source_remove(token)

    def cancel_timer(self, token):
        glib.source_remove(token)

    def defer(self, func, *args):
        glib.idle_add(_idlefunc, func, args)

    def loop(self):
        self.mloop = glib.MainLoop()
        self.mloop.run()
        
    def quitloop(self):
        self.mloop.quit()

def use():
    setdispatcher(GLibDispatcher())
