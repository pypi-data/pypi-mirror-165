#
# Copyright (c) 2009 Katie Rust (katie@ktpanda.org)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import

import sys
import traceback

from collections import deque

def default_error_handler(type, val, tb):
    if type == SystemExit or type == KeyboardInterrupt:
        raise type, val, tb
    
    if type != TaskAbort:
        traceback.print_exception(type, val, tb)

__all__ = ['LThread', 'Task', 'Dispatcher', 'SleepTask', 'Timeout',
           'Condition', 'Semaphore', 'StatusHolder', 'TaskAbort',
           'asyncfunc', 'asyncfuncself', 'tailcall', 'taskreturn',
           'getdispatcher', 'setdispatcher', 'current_thread',
           'LR_CALL', 'LR_EXC', 'LR_RETURN', 'LR_TAIL', 'LR_YIELD']

LR_CALL, LR_EXC, LR_RETURN, LR_TAIL, LR_YIELD = xrange(5)

tailcall = LR_TAIL
taskreturn = LR_RETURN

class TaskAbort(Exception):
    def __init__(self):
        pass

class Task(object):
    def run(self, thr, code, val):
        return code, val

    def start(self):
        thr = LThread(self)
        thr.run(LR_CALL, None)
        return thr

    def _on_yield(self):
        return LR_CALL, self
    
class Dispatcher(object):
    def set_timer(self, time, func, *args):
        pass

    def cancel_timer(self, token):
        pass

    def io_add(self, fd, read, func, *args):
        pass

    def cancel_io(self, token):
        pass

    def defer(self, func, *args):
        pass



    def loop(self):
        pass

    def quitloop(self):
        pass

_dispatcher = None
def getdispatcher():
    global _dispatcher
    if not _dispatcher:
        try:
            import lthread.glib as _glib
            _dispatcher = _glib.GLibDispatcher()
        except ImportError:
            pass
    return _dispatcher

def setdispatcher(disp):
    global _dispatcher
    _dispatcher = disp

def _asyncfunc(pass_self, genfunc):
    if hasattr(genfunc, 'is_async'):
        return genfunc
    
    fname = genfunc.__module__ + '.' + genfunc.__name__
    if genfunc.func_code.co_flags & 0x20:
        def ret(*args, **kwargs):
            af = GeneratorFrame(fname)
            if pass_self:
                args = (af,) + args
            af.gen = genfunc(*args, **kwargs)
            return af
    else:
        def ret(*args, **kwargs):
            af = SimpleFrame(genfunc, args, kwargs)
            if pass_self:
                af.args = (af,) + args
            return af
        
    ret.is_async = True
    ret.__module__ = genfunc.__module__
    ret.__name__ = genfunc.__name__
    return ret

def asyncfunc(genfunc):
    return _asyncfunc(False, genfunc)

def asyncfuncself(genfunc):
    return _asyncfunc(True, genfunc)

class LThread(list):
    def __init__(self, *istack):
        list.__init__(self, istack)
        self._join_cond = None

    def start(self):
        self.run(LR_CALL, None)
        return self
        
    def call(self, task):
        self.stack.append(task)

    def send(self, code, val):
        self.run(LR_RETURN, val)

    def abort(self):
        self.run(LR_EXC, (TaskAbort, None, None))

    @asyncfunc
    def join(self):
        if not self:
            return
        
        cond = self._join_cond
        if not cond:
            cond = self._join_cond = Condition()
            
        while self:
            yield cond.wait()

    def run(self, code, val):
        top = self[-1]

        while True:
            rval = None
            code, rval = top.run(self, code, val)
            if code == LR_YIELD:
                return

            elif code == LR_RETURN or code == LR_EXC:
                self.pop()
                if not self:
                    if self._join_cond:
                        self._join_cond.notify_all()
                    if code == LR_EXC:
                        default_error_handler(*rval)
                    return
                val = rval
                top = self[-1]

            elif code == LR_CALL:
                self.append(rval)
                val = None
                top = rval
            elif code == LR_TAIL:
                code = LR_CALL
                top = self[-1] = rval
                val = None



class SimpleFrame(Task):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self, thr, code, val):
        try:
            rval = self.func(*self.args, **self.kwargs)
            return LR_RETURN, rval

        except:
            return LR_EXC, sys.exc_info()
        
class GeneratorFrame(Task):
    def __init__(self, fname):
        self.funcname = fname

    def run(self, thr, code, val):
        #print 'DBG: run %r %r %r' % (self.funcname, code, val)
        try:
            if code == LR_EXC:
                rval = self.gen.throw(*val)
            else:
                rval = self.gen.send(val)

            if type(rval) == tuple:
                return rval

            if isinstance(rval, Task):
                return LR_CALL, rval
            
            if rval is None or isinstance(rval, (int, float, long)):
                return LR_CALL, SleepTask(rval or 0)

            return LR_EXC, (TypeError, 
                            TypeError("%s yielded object of type %s, expected Task or number" % 
                                      (self.funcname, type(rval).__name__)), None)
        except StopIteration:
            self.gen = None
            return LR_RETURN, None
        except:
            self.gen = None
            return LR_EXC, sys.exc_info()

class SleepTask(Task):
    def __init__(self, time):
        Task.__init__(self)
        self.time = time

    def _alarm(self, thread):
        self.token = None
        thread.pop()
        thread.run(LR_RETURN, None)
        return False
    
    def _cancel(self):
        if self.token is not None:
            getdispatcher().cancel_timer(self.token)
        self.token = None

    def _add(self, thr):
        self.token = getdispatcher().set_timer(self.time, self._alarm, thr)

    def run(self, thr, code, val):
        if code == LR_CALL:
            self._add(thr)
            return LR_YIELD, None
        
        self._cancel()
        return code, val


class Timeout(SleepTask):
    def __init__(self, time, subtask, exc = None):
        SleepTask.__init__(self, time)
        self.subtask = subtask
        if not exc:
            exc = IOError("operation timed out")
        self.exc = exc
        
    def _alarm(self, thread):
        self.token = None
        exc = self.exc
        thread.run(LR_EXC, (type(exc), exc, None))

    def run(self, thr, code, val):
        if code == LR_CALL:
            self._add(thr)
            return LR_CALL, self.subtask

        self._cancel()
        return code, val
    
class current_thread(Task):
    def run(self, thr, code, val):
        return LR_RETURN, thr

class ConditionWait(Task):
    def __init__(self, cond):
        Task.__init__(self)
        self.cond = cond

    def run(self, thr, code, val):
        if code == LR_CALL:
            self.thread = thr
            self.cond.add(self)
            return LR_YIELD, None

        self.thread = None
        self.cond.discard(self)
        return code, val

def _notify(tasks):
    for t in tasks:
        if t.thread:
            t.thread.run(LR_RETURN, None)

class Condition(set):
    def __init__(self):
        set.__init__(self)
    
    def notify(self):
        if self:
            task = self.pop()
            getdispatcher().defer(_notify, (task,))

    def notify_all(self):
        if self:
            getdispatcher().defer(_notify, list(self))
        
    def wait(self):
        return ConditionWait(self)

class StatusHolder(Condition):
    def __init__(self):
        Condition.__init__(self)
        self.val = None

    def setval(self, val):
        oval = self.val
        self.val = val
        if oval is None and val is not None:
            self.notify_all()

    @asyncfunc
    def wait(self):
        while self.val is None:
            yield ConditionWait(self)
        yield taskreturn, self.val
        
class Semaphore(Condition):
    def __init__(self, ival = 1):
        Condition.__init__(self)
        self.value = ival

    @asyncfunc
    def down(self):
        while self.value <= 0:
            yield ConditionWait(self)
        self.value -= 1
        yield LR_RETURN, self.value
        
    def down_nowait(self):
        self.value -= 1

    def up(self):
        oval = self.value
        self.value = oval + 1
        if oval == 0:
            self.notify()
        return self.value
    
class Queue(deque):
    def __init__(self, items, maxsize = None):
        deque.__init__(self, items)
        self._can_get = Condition()
        self._can_put = Condition()
        self._empty = Condition()
        self.maxsize = None

    @asyncfunc
    def get(self):
        while not self:
            yield self._can_get.wait()
            
        rval = self.popleft()
        if self.maxsize is not None:
            if len(self) < self.maxsize:
                self._can_put.notify()

        if not self:
            self._empty.notify_all()
            
        yield LR_RETURN, rval
    
    @asyncfunc
    def put(self, val):
        if self.maxsize is not None:
            while len(self) >= self.maxsize:
                yield self._can_put.wait()
                
        self.append(val)
        self._can_get.notify()

    @asyncfunc
    def wait(self):
        while self:
            yield self._empty.wait()

if __name__ == '__main__':
    import random
    sys.modules['lthread.core'] = sys.modules[__name__]

    tests = []
    testnames = {}
    
    def test(f):
        name = f.__name__[5:]
        tests.append(f)
        testnames[name] = f
        return f

    @asyncfunc
    def test_immediate_return():
        print "test_immediate_return called"
        return 3
        
    @asyncfunc
    def test_asyncfunc_1(spam):
        print "starting test_asyncfunc_1 spam = %s" % spam
        print "   sleeping"
        yield 2
        print "resumed test_asyncfunc_1 spam = %s" % spam
        print "   sleeping again"
        yield 3
        print "resumed test_asyncfunc_1 spam = %s" % spam
        ret = spam + " eggs"
        print "   returning %s" % ret
        yield taskreturn, ret
        print "should not happen"
        
    @asyncfunc
    def call_test(spam):
        print "starting call_test spam = %s" % spam
        print "calling test_asyncfunc_1"
        r = (yield test_asyncfunc_1(spam + " call 1"))

        print "returned %s" % r
        print "calling test_asyncfunc_1 again"
        r = (yield test_asyncfunc_1(spam + " call 2"))
        print "returned %s" % r




    
    @test
    @asyncfunc
    def test_basic():
        print "calling test_immediate_return"
        r = (yield test_immediate_return())
        print "returned %d" % r
        print "asynchronously calling call_test with spam = 'foo'"
        LThread(call_test('foo')).start()
        print "main sleeping"
        yield 1
        print "asynchronously calling call_test with spam = 'bar'"
        LThread(call_test('bar')).start()
        print "main sleeping"
        yield 12
        print "main done"
        
    @asyncfunc
    def test_tail(v):
        print "test tail: %d" % v
        yield 1
        if v < 3:
            yield tailcall, test_tail(v + 1)
        else:
            yield taskreturn, v

    @test
    @asyncfunc
    def test_tailcall():
        r = (yield test_tail(0))
        print "test_tail returned %s" % r
        
    @asyncfunc
    def test_join_1(i):
        stime = random.random() * 3 + 2
        print "thread %d starting, sleeptime = %f" % (i, stime)
        yield stime
        print "thread %d exiting" % i
        
    @test    
    @asyncfunc
    def test_join():
        threads = []
        for i in xrange(4):
            thr = LThread(test_join_1(i))
            threads.append(thr)
        for i, t in enumerate(threads):
            print "joining thread %d" % i
            yield t.join()
            print "joined thread %d" % i
        print "done"

    @asyncfunc
    def test_status_1(stat, i):
        print "test status thread %d waiting" % i
        val = (yield stat.wait())
        print "test status thread %d woke up, val = %s" % (i, val)

    @test    
    @asyncfunc
    def test_status():
        stat = StatusHolder()
        for i in xrange(4):
            thr = test_status_1(stat,i).start()
        print "sleeping"
        yield 2
        print "setting value"
        stat.setval('hello')
        yield 1
        print "done"
            
    @test    
    @asyncfunc
    def test_semaphore_1(sema, csem, i):
        print "thread %d starting" % i
        val = (yield sema.down())
        stime = random.random() * 2 + 1
        print "thread %d got semaphore, value = %d, sleeptime = %f" % \
              (i, val, stime)
        yield stime
        print "thread %d releasing semaphore" % i
        sema.up()
        csem.up()
        
    @test    
    @asyncfunc
    def test_semaphore():
        sema = Semaphore(2)
        csem = Semaphore()
        for i in xrange(6):
            csem.down_nowait()
            thr = test_semaphore_1(sema, csem, i).start()
        yield csem.down()
        print "done"

    @asyncfunc
    def test_queue_1(q, i):
        print "thread %d starting" % i
        try:
            while True:
                val = (yield q.get())
                stime = random.random() * 2 + 1
                print "thread %d got value %s, sleeptime = %f" % \
                      (i, val, stime)
                yield stime
        finally:
            print "thread %d exiting" % i
        
    @test    
    @asyncfunc
    def test_queue():
        q = Queue(['abc', '123', '456', '789', 'foo', 'bar', 'baz'])
        threads = []
        for i in xrange(3):
            threads.append(test_queue_1(q, i).start())
        print "waiting for queue to be empty"
        yield q.wait()
        print "stopping threads"
        for t in threads:
            t.abort()
        print "done"

        
    import glib, gobject
    import lthread.glib
    lthread.glib.use()

    
    if len(sys.argv) == 1:
        rtests = tests
    else:
        rtests = [testnames[i] for i in sys.argv[1:]]
        
    @asyncfunc
    def main():
        for i in rtests:
            print "starting test %s" % i.__name__[5:]
            yield i()
        
    mt = main().start()

    loop = gobject.MainLoop()
    ctx = loop.get_context()
    while mt:
        print "    --- (time passes) ---"
        ctx.iteration(True)
