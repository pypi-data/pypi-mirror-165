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

from lthread.core import *
import re
import traceback

import sys
import os
import fcntl
import socket

from collections import deque

from errno import EWOULDBLOCK, EINTR, EINPROGRESS

try:
    import ssl
    SSLError = ssl.SSLError
except ImportError:
    ssl = None
    class SSLError(Exception):
        pass


__all__ = ['AsyncFile', 'asyncfile', 'socket_server',
           'tcp_server', 'unix_server', 'IOTask']

class IOTask(Task):
    def __init__(self, fd, read, blocking, func = None, *args):
        Task.__init__(self)
        self.fd = fd
        self.blocking = blocking
        self.read = read

        self.func = func
        self.args = args

    def cancel(self):
        if self.token is not None:
            getdispatcher().cancel_io(self.token)
        self.token = None

    def add(self, thr):
        self.token = getdispatcher().io_add(self.fd, self.read,
                                            self._return, thr)
        return LR_YIELD, None

    def _return(self, thread):
        self.token = None
        thread.run(LR_CALL, None)
    
    def run(self, thr, code, val):
        if code == LR_EXC:
            self.cancel()
            return code, val

        if self.blocking:
            self.blocking = False
            return self.add(thr)

        try:
            data = self.func(*self.args)
            self.token = None
            return LR_RETURN, data
        
        except (os.error, socket.error), why:
            if why[0] in (EWOULDBLOCK, EINTR, EINPROGRESS):
                return self.add(thr)
            return LR_EXC, sys.exc_info()
            
        except:
            return LR_EXC, sys.exc_info()


class FDWrapper(object):
    def __init__(self, fd):
        self.fd = fd
        
    def setblocking(self, block):
        if self.fd == -1:
            return
        
        flags = fcntl.fcntl(self.fd, fcntl.F_GETFL, 0)
        if block:
            flags = flags | os.O_NONBLOCK
        else:
            flags = flags & ~os.O_NONBLOCK
            
        fcntl.fcntl(self.fd, fcntl.F_SETFL, flags)
        
    def read(self, n):
        if self.fd == -1:
            return ''
        return os.read(self.fd, n)
    
    def write(self, d):
        if self.fd == -1:
            return 0
        return os.write(self.fd, d)

    def close(self):
        if self.fd == -1:
            return
        os.close(self.fd)
        self.fd = -1

    def __del__(self):
        self.close()
        
def rdfunc(file):
    if hasattr(file, 'read'):
        return file.read

    if hasattr(file, 'recv'):
        return file.recv

    
def wrfunc(file):
    if hasattr(file, 'write'):
        return file.write

    if hasattr(file, 'send'):
        return file.send

def findfirst(str, args):
    minidx = None
    minstr = None
    for i in args:
        idx = str.find(i)
        if idx != -1:
            if minidx is None or idx < minidx:
                minidx = idx
                minstr = i
    return minidx, minstr

nlre = re.compile(r'\r?\n', re.S)
class AsyncFile(object):
    def __init__(self, file, maxbuffer = None, nonblock = True):
        self.file = file
        self.maxbuffer = maxbuffer
        self.nonblock = nonblock
        self._last_line_term = ''
        self.write_buffer = deque()
        self.write_task = None
        self.write_error = None

        if isinstance(file, int):
            self.fd = file
            self.file = FDWrapper(file)
        else:
            self.file = file
            self.fd = file.fileno()

        self.rdbuf = ""
        self._read = rdfunc(self.file)
        self._write = wrfunc(self.file)
        if nonblock:
            self.file.setblocking(False)

    def _wait(self, read, func = None, *args):
        return IOTask(self.fd, read, not self.nonblock, func, *args)

    def waitread(self):
        return self._wait(True)
    
    def waitwrite(self):
        return self._wait(False)

    def raw_read(self, n):
        return self._wait(True, self._read, n)

    def raw_write(self, data):
        return self._wait(False, self._write, data)

    def accept(self):
        return self._wait(True, self.file.accept)

    def sendto(self, *args):
        return self._wait(False, self.file.sendto, *args)

    def connect(self, *args):
        return self._wait(False, self.file.connect, *args)

    def recvfrom(self, *args):
        return self._wait(True, self.file.recvfrom, *args)

    def close(self):
        if self.write_buffer:
            self.write_buffer.clear()
        self.file.close()

    def __getattr__(self, attr):
        return getattr(self.file, attr)

    @asyncfunc
    def _write_buffer(self):
        writebuf = self.write_buffer
        
        while writebuf:
            data = writebuf.popleft()
            if data is None:
                self.close()
                break
            
            if isinstance(data, StatusHolder):
                data.setval(True)
                continue

            if self.write_error:
                continue

            try:
                remain = len(data)
                while remain > 0:
                    n = (yield self.raw_write(data))
                    #if n == 0:
                    #    raise OSError('Broken pipe')
                    data = data[n:]
                    remain -= n
                    
            except (socket.error, IOError, OSError), err:
                self.write_buffer = None
                self.write_error = err
                

    def _start_write(self):
        if not self.write_task:
            self.write_task = self._write_buffer().start()

    def push(self, *vals):
        if self.write_error:
            raise self.write_error

        self.write_buffer.extend(vals)
        self._start_write()

    @asyncfunc
    def write(self, *data):
        if self.write_error:
            raise self.write_error

        self.write_buffer.extend(data)

        cond = StatusHolder()
        self.write_buffer.append(cond)
        self._start_write()
        yield cond.wait()

        if self.write_error:
            raise self.write_error
        
    @asyncfunc
    def wait_and_close(self):
        if self.write_task:
            yield self.write_task.join()
        self.close()

        if self.write_error:
            raise self.write_error

    writeall = write

    @asyncfunc
    def sync(self):
        if self.write_error:
            raise self.write_error

        if not self.write_buffer:
            return

        cond = Condition()
        self.write_buffer.append(cond)
        self._start_write()
        yield tailcall, cond.wait()
        
    @asyncfunc
    def read(self, n):
        ret = self.rdbuf[:n]
        self.rdbuf = self.rdbuf[n:]
        n -= len(ret)
        if n == 0:
            yield taskreturn, ret
        rdat = (yield self.raw_read(n))
        
        yield taskreturn, ret + rdat

    @asyncfunc
    def readall(self, n):
        ret = ""
        while n:
            dat = (yield self.read(n))
            if not dat:
                yield taskreturn, ret
            n -= len(dat) 
            ret += dat
        yield taskreturn, ret

    @asyncfunc
    def read_until(self, rx, maxmatch = None, maxbuffer = None):
        buf = self.rdbuf
        spos = 0
        search = rx.search
        while True:
            m = search(buf, spos)
            if m:
                b, e = m.span()
                data       = buf[  : b]
                term       = buf[b : e]
                self.rdbuf = buf[e :  ]
                yield taskreturn, (data, term)

            if maxmatch:
                spos = len(buf) - maxmatch
                if spos < 0: spos = 0

            if maxbuffer is not None:
                toread = maxbuffer - len(buf)
                if toread <= 0:
                    break
                dat = (yield self.raw_read(toread))
            else:
                dat = (yield self.raw_read(1024))
                
            if not dat:
                break

            buf += dat
            
        self.rdbuf = ""
        yield taskreturn, (buf, None)

    @asyncfunc
    def readline(self, include_nl = False, max = None):
        line, term = (yield self.read_until(nlre, 2, max))
        if include_nl:
            yield taskreturn, line + (term or '')
        else:
            yield taskreturn, (line if line or term is not None else None)

def asyncfile(fil, *args, **kwargs):
    if fil is None:
        return None
    
    if isinstance(fil, AsyncFile):
        return fil
    return AsyncFile(fil, *args, **kwargs)

@asyncfunc
def socket_server(sock, handler):
    sock.listen(5) 
    asock = asyncfile(sock)
    try:
        while True:
            csock, addr = (yield asock.accept())
            handler(asyncfile(csock), addr).start()
    finally:
        sock.close()
    
@asyncfunc
def tcp_server(addr, port, handler):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((addr, port))
    yield tailcall, socket_server(sock, handler)

@asyncfunc
def unix_server(path, mode, handler):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.unlink(path)
    except OSError:
        pass
    oldmask = os.umask(0777 ^ mode)
    try:
        sock.bind(path)
    finally:
        os.umask(oldmask)
    yield tailcall, socket_server(sock, handler)

if __name__ == '__main__':
    import sys
    sys.modules['lthread.io'] = sys.modules[__name__]

    @asyncfunc
    def handle_client(sock, addr):
        print "connection from %s:%d" % addr
        sock.push('Hello!\r\n')
        while True:
            line = (yield sock.readline())
            if line is None:
                break
            print "command from client: %s" % line
            sock.push('You typed %r.\r\n' % line)
            if line == 'quit':
                break
        sock.push('Bye.\r\n')
        yield sock.wait_and_close()
        print "client %s:%d disconnected" % addr
            

    tcp_server('', 9999, handle_client).start()


    try:
        getdispatcher().loop()
    except KeyboardInterrupt:
        pass
