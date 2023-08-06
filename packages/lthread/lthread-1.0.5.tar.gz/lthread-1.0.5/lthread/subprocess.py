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
from lthread.io import *

import os
import signal
import traceback
import errno

__all__ = ['ChildProcess', 'M_STDIN', 'M_STDOUT', 'M_STDERR',
           'M_STDOUTERR', 'M_STDIN_NULL', 'M_STDOUT_NULL',
           'M_STDERR_NULL','M_ALL_NULL' ]

children = {}
stillborn_status = {}
def sigcld(*args):
    while True:
        try:
            pid, stat = os.waitpid(-1, os.WNOHANG)
        except OSError, err:
            if err[0] == errno.ECHILD:
                break
        if pid == 0:
            break
        
        if pid in children:
            getdispatcher().defer(children[pid]._closed, stat)
        else:
            stillborn_status[pid] = stat
    
    set_handler()

    
def set_handler():
    signal.signal(signal.SIGCLD, sigcld)


SIGTERM = signal.SIGTERM
try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except (AttributeError, ValueError):
    MAXFD = 256

M_STDIN = 1
M_STDOUT = 2
M_STDERR = 4
M_STDOUTERR = 8
M_STDIN_NULL = 16
M_STDOUT_NULL = 32
M_STDERR_NULL = 64
M_ALL_NULL = (M_STDIN_NULL | M_STDOUT_NULL | M_STDERR_NULL)
M_SETPGID = 128

# From popen2.py, modified to support tracking children

class ChildProcess(object):
    sts = -1                    # Child not completed yet

    def __init__(self, cmd, mode = 0, bufsize=-1, pre_exec=None):
        """The parameter 'cmd' is the shell command to execute in a
        sub-process.  On UNIX, 'cmd' may be a sequence, in which case arguments
        will be passed directly to the program without shell intervention (as
        with os.spawnv()).  If 'cmd' is a string it will be passed to the shell
        (as with os.system()). If the 'bufsize' parameter is
        specified, it specifies the size of the I/O buffers to/from the child
        process."""

        set_handler()
        self.exit_status = StatusHolder()

        self.cmd = cmd

        if mode & M_STDOUTERR:
            mode &= ~M_STDERR

        if mode & M_STDIN:
            p2cread, p2cwrite = os.pipe()

        if mode & M_STDOUT or mode & M_STDOUTERR:
            c2pread, c2pwrite = os.pipe()
            
        if mode & M_STDERR:
            errout, errin = os.pipe()
            
        self.pid = os.fork()
            
        if self.pid == 0:
            # Child
            if mode & M_SETPGID:
                os.setpgrp()
            nullfd = -1
            close_null = False
            if mode & M_ALL_NULL:
                try:
                    nullfd = os.open(os.devnull, os.O_RDWR)
                    close_null = True
                except OSError:
                    pass
            
            if mode & M_STDIN:
                os.dup2(p2cread, 0)

            if mode & M_STDOUT:
                os.dup2(c2pwrite, 1)

            if mode & M_STDERR:
                os.dup2(errin, 2)

            if mode & M_STDOUTERR:
                os.dup2(c2pwrite, 1)
                os.dup2(c2pwrite, 2)

            minfd = 3
            if nullfd != -1:
                if mode & M_STDIN_NULL:
                    os.dup2(nullfd, 0)
                    
                if mode & M_STDOUT_NULL:
                    os.dup2(nullfd, 1)

                if mode & M_STDERR_NULL:
                    os.dup2(nullfd, 2)

            if close_null:
                try:
                    os.close(nullfd)
                except OSError:
                    pass
                    
                    
            for i in xrange(minfd, MAXFD):
                try:
                    os.close(i)
                except OSError:
                    pass
            if pre_exec:
                pre_exec()
            self._run_child(cmd)

        if mode & M_STDIN:
            os.close(p2cread)
            self.tochild = asyncfile(p2cwrite, bufsize, False)
        else:
            self.tochild = None

        if mode & M_STDOUT or mode & M_STDOUTERR:
            os.close(c2pwrite)
            self.fromchild = asyncfile(c2pread, bufsize, False)
        else:
            self.fromchild = None
            
        if mode & M_STDERR:
            os.close(errin)
            self.childerr = asyncfile(errout, bufsize, False)
        else:
            self.childerr = None

        children[self.pid] = self
        
        # It's possible that the child process could die before we get
        # a chance to record it.
        if self.pid in stillborn_status:
            stat = stillborn_status[self.pid]
            del stillborn_status[self.pid]
            self._closed(stat)
        
    def _closed(self, status):
        self.sts = status
        if self.pid in children:
            del children[self.pid]

        self.exit_status.setval(status)
        
    def _run_child(self, cmd):
        if isinstance(cmd, basestring):
            cmd = ['/bin/sh', '-c', cmd]

        try:
            os.execvp(cmd[0], cmd)
        finally:
            os._exit(42)
        
    def signal(self, sig = SIGTERM):
        os.kill(self.pid, sig)
        
    def signal_group(self, sig = SIGTERM):
        os.kill(-self.pid, sig)

    def wait(self):
        return self.exit_status.wait()

    def poll(self):
        """Return the exit status of the child process if it has finished,
        or -1 if it hasn't finished yet."""
        if self.sts < 0:
            try:
                pid, sts = os.waitpid(self.pid, os.WNOHANG)
                # pid will be 0 if self.pid hasn't terminated
                if pid == self.pid:
                    self.sts = sts
            except os.error:
                pass
        return self.sts

    def wait_blocking(self):
        """Wait for and return the exit status of the child process."""
        if self.sts < 0:
            pid, sts = os.waitpid(self.pid, 0)

            # This used to be a test, but it is believed to be
            # always true, so I changed it to an assertion - mvl
            assert pid == self.pid
            self.sts = sts
        return self.sts

if __name__ == '__main__':
    import sys
    sys.modules['lthread.subprocess'] = sys.modules[__name__]

    @asyncfunc
    def run_cmd(cmd):
        print "running command %r" % cmd
        cp = ChildProcess(cmd)
        stat = (yield cp.wait())
        print "%r finished, status = %d" % (cmd, os.WEXITSTATUS(stat))


    @asyncfunc
    def main():
        threads = []
        threads.append(run_cmd('echo "hello"; sleep 2; echo "bye"').start())
        threads.append(run_cmd('echo "hello 2"; sleep 1; echo "bye 2"').start())
        for t in threads:
            yield t.join()
        getdispatcher().quitloop()
        
    main().start()
    try:
        getdispatcher().loop()
    except KeyboardInterrupt:
        pass
