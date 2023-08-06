
import sys
import re
import os
import time
import struct
from os.path import *

BLOCKSHIFT = 12
BLOCKSIZE = 1 << BLOCKSHIFT

def gettime():
    return int(time.time() * 1000)

def readvar(str, pos):
    ret = 0
    while True:
        rd = ord(str[pos])
        pos += 1
        ret <<= 7
        ret |= rd & 127
        if not rd & 128:
            return ret, pos

def encodev(v):
    if v < 128:
        return chr(v)
    if v < 16384:
        return chr(0x80 | ((v >> 7) & 0x7F)) + chr(v & 0x7F)
    if v < 2097152:
        return chr(0x80 | ((v >> 14) & 0x7F)) + chr(0x80 | ((v >> 7) & 0x7F)) + chr(v & 0x7F)

    r = ''
    while v:
        tv = v & 0x7F
        v >>= 7
        if r:
            tv |= 0x80
        r = chr(tv) + r
        
    return r


class Counter(object):
    def __init__(self, v=0, name=None):
        self.v = v
        self.delta = 0
        self.name = name

    def getdelta(self):
        delt = self.delta
        self.v += delt
        self.delta = 0
        return delt
        
DBG = True
MAX_TIME = 1 << 64

iotime = 0
strll = struct.Struct('>Q')
class TrafLogReader(object):
    def __init__(self, fn, ctrs=None):
        self.fn = fn
        self.f = open(fn, 'rb')
        self.lastlen = None
        self.check_update()

        self.cblock = self.nblocks
        self.blockdat = None
        self.bstime = MAX_TIME

        self.bpos = 0
        self.ltime = 0

        self.blocktimecache = {}
        #self.blocktimecache = [None] * self.nblocks
        if ctrs is None:
            ctrs = []
        self.ctrs = ctrs

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    def blocktime(self, n):
        bt = self.blocktimecache.get(n)
        if bt is not None:
            return bt

        bt = self.blocktimecache[n] = self.seekblock(n)
        return bt

    def seekblock(self, n):
        if n < 0:
            n += self.nblocks

        self.f.seek(n << BLOCKSHIFT)
        self.blockdat = b = self.f.read(BLOCKSIZE)

        self.cblock = n
        self.bstime = sttime = strll.unpack(b[:8])[0]
        self.bpos = 0

        return sttime

    def _seek_block_begin(self):
        b = self.blockdat
        ctrs = self.ctrs
        nctrs = ord(b[8])
        while len(ctrs) < nctrs:
            ctrs.append(Counter())

        pos = 9
        for i in range(nctrs):
            v = strll.unpack(b[pos : pos + 8])[0]
            ctrs[i].v = v
            pos += 8

        self.ltime = self.bstime
        self.bpos = pos

    def check_update(self):
        self.f.seek(0, 2)
        flen = self.f.tell()
        nblocks = (flen + BLOCKSIZE - 1) >> BLOCKSHIFT
        if self.lastlen is not None:
            if flen > self.lastlen:
                if self.cblock == self.nblocks - 1:
                    # if current block is last block, re-read it
                    self.seekblock(self.cblock)
        self.nblocks = nblocks
        self.lastlen = flen

    def seektime(self, t):
        #if t == self.ltime:
        #    return True

        #if DBG: print 'seektime %x' % t
        if not self.blockdat:
            self.binseek(t, 0, self.nblocks)

        elif t >= self.bstime:
            #if DBG: print '  > bstime %x' % self.bstime
            if t < self.ltime:
                #if DBG: print '  < ltime %x' % self.ltime
                self._seek_block_begin()

            if self._parse_block_fwd(t):
                return True
            #if DBG: print '  > last time in block'
            self.binseek(t, self.cblock, self.nblocks)
            
        else:
            #if DBG: print '  < bstime %x' % self.bstime
            self.binseek(t, 0, self.cblock)
            if t < self.bstime:
                #if DBG: print 'out of range 1'
                return False

        self._seek_block_begin()
        return self._parse_block_fwd(t) or self.cblock != self.nblocks - 1

    def seeknext(self):
        if not self._parse_block_fwd(None, True):
            if self.cblock == self.nblocks - 1:
                return False
            self.seekblock(self.cblock + 1)
            self._seek_block_begin()
        return True

    def seek_begin(self):
        self.seekblock(0)
        self._seek_block_begin()

    def seek_end(self):
        self.seekblock(-1)
        self._seek_block_begin()
        self._parse_block_fwd(None)
        
    def binseek(self, seektm, bsb, bse):
        #if DBG: print '    binseek seektm=%x bsb=%d bse=%d' % (seektm, bsb, bse)
        safety = 10000
        while safety:
            med = (bsb + bse) // 2
            #if DBG: print '    binseek bsb=%d bse=%d med=%d' % (bsb, bse, med)
            if bsb == bse:
                break
            
            cbt = self.blocktime(med)
            #if DBG: print '    binseek cbt=%x' % (cbt)

            if cbt <= seektm:
                if bsb == med:
                    break
                bsb = med

            else:
                if bse == med:
                    med -= 1
                    break
                bse = med

            safety -= 1

        #if DBG: print '    binseek med=%d' % (med)
        if med != self.cblock or med == self.nblocks - 1:
            self.seekblock(med)
        

    def _parse_block_fwd(self, t, next=False):
        b = self.blockdat
        nctrs = ord(b[8])
        pos = self.bpos
        ltime = ctime = self.ltime
        ln = len(b)
        ctrs = self.ctrs
        
        if len(ctrs) > nctrs:
            ctrs = ctrs[:nctrs]
        #if DBG: print '    _pbf ctime=%x pos=%d ln=%d' % (ctime, pos, ln)
        try:
            while pos < ln:
                #if DBG: print '      pos=%d' % (pos)
                td, npos = readvar(b, pos)
                #if DBG: print '      td=%d' % (td)
                if not td:
                    break
                ctime += td
                #if DBG: print '      ctime=%x' % (ctime)
                
                if t is not None and ctime > t:
                    self.bpos = pos
                    self.ltime = ltime
                    return True

                for c in ctrs:
                    cd, npos = readvar(b, npos)
                    c.v += cd
                    
                if next:
                    self.bpos = npos
                    self.ltime = ctime
                    return True

                ltime = ctime
                pos = npos
        except IndexError:
            pass

        self.bpos = pos
        self.ltime = ltime
        return False


class TrafLogWriter(object):
    def __init__(self, fn, ctrs):
        self.fn = fn
        self.f = open(fn, 'a+b', buffering=0)
        flen = self.f.tell()
        pad = BLOCKSIZE - (flen & (BLOCKSIZE - 1))
        if pad < BLOCKSIZE:
            self.f.write('\0' * pad)

        self.block_pos = BLOCKSIZE
        self.ctrs = ctrs
        self.ctime = 0

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    def write_counters(self, time=None):
        if time is None:
            time = gettime()
        timedelt = time - self.ctime
        self.ctime = time
        wdata = encodev(timedelt) + ''.join(encodev(c.getdelta()) for c in self.ctrs)
        nblockpos = self.block_pos + len(wdata)

        if nblockpos > BLOCKSIZE:
            pad = BLOCKSIZE - self.block_pos
            hdr = strll.pack(time) + chr(len(self.ctrs)) + \
                ''.join(strll.pack(c.v) for c in self.ctrs)
            wdata = ('\0' * pad) + hdr
            nblockpos = len(hdr)

        self.f.write(wdata)
        self.block_pos = nblockpos

rxtimef = re.compile(r'([0-9a-f]{16})_')
class TrafLog(object):
    def __init__(self, dir, ctrs):
        self.dir = dir
        try:
            os.makedirs(dir)
        except OSError:
            pass
        self.lastmod = None
        self.cday = None
        self.checkfiles()

        self.curidx = None
        self.curtf = None
        try:
            self.ctrs = list(ctrs)
        except TypeError:
            self.ctrs = [Counter(0) for x in range(ctrs)]

    def close(self):
        if self.curtf:
            self.curtf.close()
            self.curtf = None

    def checkfiles(self):
        lm = getmtime(self.dir)
        if lm == self.lastmod:
            return

        files = self.files = []
        for f in os.listdir(self.dir):
            m = rxtimef.match(f)
            if m:
                fn = join(self.dir, f)
                if getsize(fn) >= 16:
                    ct = int(m.group(1), 16)
                    files.append((ct, fn))
        files.sort()

    def seeknext(self):
        if self.curtf:
            if self.curtf.seeknext():
                self.ltime = self.curtf.ltime
                return True
            if self.curidx == len(self.files) - 1:
                return False
            
            self.curtf.close()
            self.curidx += 1
        else:
            self.curidx = 0
        self.curtf = TrafLogReader(self.files[self.curidx][1], self.ctrs)
        self.curtf.seek_begin()
        self.ltime = self.curtf.ltime
        return True
    
    def seektime(self, t):
        if self.curtf:
            if self.curtf.seektime(t):
                return True
            self.curtf.close()
            self.curtf = None
            self.curidx = None
        lf = None
        lidx = None
        for i, (ct, f) in enumerate(self.files):
            if ct > t:
                break
            lf = f
            lidx = i
            
        if not lf:
            return False
        
        self.curtf = TrafLogReader(lf, self.ctrs)
        self.curidx = lidx
        return self.curtf.seektime(t)

    def seek_end(self):
        self.seektime(MAX_TIME)

    def genfn(self, tm):
        tstr = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(tm / 1000))
        return '%016x_%s' % (tm, tstr)

    def write_counters(self, time=None):
        if time is None:
            time = gettime()
        day = time / 86400000
        if self.curtf is None or day != self.cday:
            self.cday = day
            if self.curtf:
                self.curtf.close()
            newfn = self.genfn(time)
            self.curtf = TrafLogWriter(join(self.dir, newfn), self.ctrs)
        self.curtf.write_counters(time)
        

def test1():
    tstlogf = 'traflog'
    
    TMUL = 5000
    c1 = Counter(15)
    c2 = Counter(63)
    print('writing...')

    tw = TrafLog(tstlogf, [c1, c2])
    for j in range(100000):
        tw.write_counters(j * TMUL)
        c1.delta = 0x100
        c2.delta = 0x1000
    tw.close()

    print('reading...')
    maxtime = TMUL * 100000
    tr = TrafLog(tstlogf, 2)

    st = time.time()
    ct = 0
    while True:
        if not tr.seektime(ct):
            break
        rtime = ct & ~0xFFFFFF
        crc = ct / TMUL
        c1b = 15 + crc * 0x100
        c2b = 63 + crc * 0x1000
        c1q = tr.ctrs[0].v
        c2q = tr.ctrs[1].v
        if c1b != c1q or c2b != c2q:
            print('xxx %x' % ct)
            print('%016x %016x' % (c1b, c1q))
            print('%016x %016x' % (c2b, c2q))
        ct += TMUL
    et = time.time()
    print('%x %.15f %.15f' % (ct, et - st, iotime))
    return 
    while True:
        st = time.time()
        trytime = random.randrange(0, maxtime)
        #trytime = 0
        tr.seektime(trytime)
        rtime = trytime & ~0xFFFFFF
        crc = trytime / TMUL
        c1b = 15 + crc * 0x100
        c2b = 63 + crc * 0x1000
        c1q = tr.ctrs[0].v
        c2q = tr.ctrs[1].v
        et = time.time()
        print('%x %.15f %.15f' % (ct, et - st, iotime))
        print('%016x %016x' % (c1b, c1q))
        print('%016x %016x' % (c2b, c2q))
        if c1b != c1q or c2b != c2q:
            print(trytime)
            break
        print()

def test2():
    tstlogf = 'traflog'

    tw = TrafLog(tstlogf, 5)
    ctrs = tw.ctrs

    tcnt = 0

    samples = []
    print('writing ...')
    ct = gettime()
    nextsample = random.randrange(20, 200)
    ctdelta = 0
    while len(samples) < 200:
        tcnt += 1
        ct += ctdelta
        ctdelta = random.randrange(300, 10000)
        for c in ctrs:
            c.delta = random.randrange(0, 10000000)
        tw.write_counters(ct)
        nextsample -= 1
        if nextsample == 0:
            samples.append((ct, ct + ctdelta, [c.v for c in ctrs]))
            nextsample = random.randrange(20, 100)
    tw.close()
    print('wrote %d entries' % tcnt)
    
    tr = TrafLog(tstlogf, 5)
    bt = time.time()
    print('reading sequential ...')
    i = 0
    j = 0
    tstnext = None
    while tr.seeknext():
        j += 1
        #if j < 10 or j % 10000 == 0:
        #    print j, tr.ltime
        if i < len(samples) and tr.ltime == samples[i][0]:
            ct, nct, ctrs = samples[i]
            i += 1
            tstnext = nct
            tcv = [c.v for c in tr.ctrs]
            if tcv != ctrs:
                print('!!!!! %d %r %r' % (ct, tcv, ctrs))
        elif tstnext is not None:
            if tr.ltime != tstnext:
                print('!!!!! %d %d %d %r %r' % (tr.ltime, tstnext, ct, tcv, ctrs))
            tstnext = None
    
    et = time.time()
    print('read %d sequential log entries in %.5fs' % (j, et - bt))
    
    print('reading ...')
    random.shuffle(samples)
    #samples = [random.choice(samples)]
    tr.seektime(0)


    bt = time.time()
    for ct, nct, ctrs in samples:
        tsttime = random.randrange(ct, nct)
        tr.seektime(tsttime)
        tcv = [c.v for c in tr.ctrs]
        if tcv != ctrs:
            print('!!!!! %d %r %r' % (tsttime, tcv, ctrs))
        #print 'ok %d' % tsttime
        #else:
        #    print '!!!!! %d %r %r' % (tsttime, tcv, ctrs)
    et = time.time()
    print('read %d random samples in %.5fs' % (len(samples), et - bt))

            
def main():
    if len(sys.argv) > 1:
        dir = sys.argv[1]
        tr = TrafLog(dir, 0)
        while tr.seeknext():
            tcv = [c.v for c in tr.ctrs]
            print('%d %r' % (tr.ltime, tcv))
    else:
        test2()
            

if __name__ == '__main__':
    import random
    try:
        main()
    except KeyboardInterrupt:
        print('interrupted')
