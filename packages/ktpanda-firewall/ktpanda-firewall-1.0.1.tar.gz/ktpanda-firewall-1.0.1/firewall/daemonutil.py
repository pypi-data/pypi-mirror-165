import sys
import os
import signal
import syslog
import time
import traceback
from optparse import OptionParser
from os.path import *

__all__ = ['options', 'log', 'init_options', 'init_daemon', 'cleanup']

options = OptionParser()
_got_signal = False

debug = None
info = None
err = None

def readpid(pidf, daemon):
    daemon = realpath(daemon)
    try:
        pid = int(file(pidf, 'r').readline().strip())
        #print(pid, f)
        cmdline = file('/proc/%d/cmdline' % pid, 'r').read().split('\0')
        for p in cmdline[:3]:
            if realpath(p) == daemon:
                return pid
    except Exception:
        pass
    return 0

pidf = None
    
def exitsig(sig, frame):
    global _got_signal
    if not _got_signal:
        _got_signal = True
        raise KeyboardInterrupt

def init_options():
    options.add_option("-p", "--pidfile", action="store", 
                       dest="pidfile", metavar="FILE",
                       help="write daemon process ID to a file")

    options.add_option("-l", "--logfile", action="store", 
                       dest="logfile", metavar="FILE",
                       help="redirect output to log file")

    options.add_option("-d", "--daemonize", action="store_true",
                       dest="daemon", default=False,
                       help="detach from parent")

    return options

class SyslogFile(object):
    def __init__(self, name, level=syslog.LOG_INFO, backfile=None):
        self.name = name
        self.level = level
        self.backfile = backfile
        self.lbuf = ''

    def write(self, dat):
        #ostdout.write('%r\n' % dat)
        bf = self.backfile
        ctime = time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(time.time()))
        prefix = '%s %s: ' % (ctime, self.name)
        bfil = self.backfile
        
        buf = self.lbuf + dat
        lines = buf.split('\n')
        for l in lines[:-1]:
            syslog.syslog(self.level, l)
            if bf:
                bf.write(prefix + l + '\n')
        self.lbuf = lines[-1]
        if bf:
            bf.flush()

    def flush(self): pass
    def close(self): pass
    def seek(self, *args): raise NotImplementedError()
    def read(self, *args): return ''

class DummyFile(object):
    def write(self, *args): pass
    def flush(self): pass
    def close(self): pass

def daemonize():
    """Makes the process into a daemon. Forks twice (to detach from
    the parent process), then calls setsid(). Closes sys.stdin,
    and redirects sys.stdout and sys.stderr to logfile, or to a dummy
    file if logfile is None.
    """

    global _logf
    
    if os.fork() != 0: os._exit(0)
    if os.fork() != 0: os._exit(0)
    os.setsid()


def write_pidfile(pidfile):
    global pidf
    try:
        pf = open(pidfile, 'w')
        pf.write('%d\n' % os.getpid())
        pf.close()
        pidf = pidfile
    except Exception:
        traceback.print_exc()
        pass
    
def init_logging(name, logfile = None, close_out = True):
    global debug, info, err
    syslog.openlog(name, syslog.LOG_NDELAY | syslog.LOG_PID,
                   syslog.LOG_DAEMON)

    if close_out:
        sys.stdout.close()
        sys.stderr.close()
        sys.stdin.close()

        logfil = None
    else:
        logfil = sys.stdout

    if logfile:
        try:
            logfil = open(logfile, "a")
        except IOError as e:
            print(('could not open logfile: %s' % e))

            
    debug = SyslogFile(name, syslog.LOG_DEBUG, logfil)
    info = SyslogFile(name, syslog.LOG_INFO, logfil)
    err = SyslogFile(name, syslog.LOG_ERR, logfil)

    sys.stdout = debug
    sys.stderr = info
    
def init_signals():
    signal.signal(signal.SIGINT, exitsig)
    signal.signal(signal.SIGTERM, exitsig)
    
def init_daemon(name, opts=None):
    if opts is None:
        opts, args = options.parse_args()

    if opts.daemon:
        daemonize()

    init_logging(name, opts.logfile, opts.daemon)
    
    if opts.pidfile:
        write_pidfile(opts.pidfile)
        
    init_signals()
    
def cleanup():
    if pidf:
        try:
            os.unlink(pidf)
        except Exception:
            pass
