import re
from os.path import join, dirname, abspath

from firewall import util

public = util.public(globals())

_uescre = re.compile(r'\\(.)', re.S)

_uesctbl = dict(n = '\n', t = '\t')
_uesctbl['\n'] = ''
@public
def uescape(c):
    chr = c.group(1)
    if chr in _uesctbl:
        return _uesctbl[chr]
    return chr

_escre=re.compile(r'["\n\t\\]')
_esctbl = {'\n': 'n', '\t': 't'}
@public
def escape(c):
    chr = c.group(0)
    if chr in _esctbl:
        return "\\" + _esctbl[chr]
    return "\\" + chr


(WHITESPACE, CHAR, STRING, WORD) = range(4)

class Tokenizer(object):
    def __init__(self, strm):
        self.strm = strm
        
        self.buf = ''
        self.buflen = 0
        self.bufidx = 0
        self.lineno = 1
        
    wordchars = set('abcdefghijklmnopqrstuvwxyz'
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    '0123456789~@%^_+-=\\/:?*.,')
    
    wschars = set(" \t\r")

    def _getmore(self):
        ndat = self.strm.read(2048)
        if not ndat:
            return False
        
        self.buf = self.buf[self.bufidx:] + ndat
        self.bufidx = 0
        self.buflen = len(self.buf)
        return True

    def _read_while(self, func, sofs = 0, eofs = 0):
        src = self.buf
        len = self.buflen
        end = start = self.bufidx
        line = self.lineno

        lc = None
        while True:
            end += 1
            if end >= len:
                if not self._getmore(): break
                end = len - start; start = 0
                src = self.buf; len = self.buflen
                
            c = src[end]
                
                
            if lc == '\\' or func(c):
                lc = c
            else:
                break

            if c == '\n':
                line += 1

        ret = self.buf[start + sofs: end]
        self.bufidx = end + eofs
        self.lineno = line
        return ret
    
    def _handle_word(self):
        wordchars = self.wordchars
        ret = self._read_while(lambda c: c in wordchars)
        return WORD, _uescre.sub(uescape, ret)

    def _handle_dquot(self):
        ret = self._read_while(lambda c: c != '"', 1, 1)
        return STRING, _uescre.sub(uescape, ret)
    
    def _handle_squot(self):
        ret = self._read_while(lambda c: c != "'", 1, 1)
        return STRING, ret
    
    def _handle_comment(self):
        self._read_while(lambda c: c != '\n')
        return CHAR, '\n'

    def _handle_newline(self):
        self.bufidx += 1
        self.lineno += 1
        return CHAR, '\n'

    def _handle_whitespace(self):
        wschars = self.wschars
        self._read_while(lambda c: c in wschars)
        return WHITESPACE, ''

    def _handle_default(self):
        idx = self.bufidx
        self.bufidx = idx + 1
        return CHAR, self.buf[idx]

    def __iter__(self):
        handlers = self.handlers
        while True:
            if self.bufidx >= self.buflen:
                if not self._getmore():
                    break
            c = self.buf[self.bufidx]
            typ, val = handlers[ord(c)](self)
            if typ != WHITESPACE:
                yield typ, val

        
    handlers = [_handle_default] * 256
    for z in wordchars:
        handlers[ord(z)] = _handle_word
        
    for z in wschars:
        handlers[ord(z)] = _handle_whitespace
        
    del z
    
    handlers[ord('\n')] = _handle_newline
    handlers[ord('"')] = _handle_dquot
    handlers[ord("'")] = _handle_squot
    handlers[ord('#')] = _handle_comment

class Config(object):
    public = True
    
    def __init__(self):
        self.seen = set()

    def parse_file(self, path):
        path = path.resolve()
        if path in self.seen:
            return
        
        self.seen.add(path)
        
        with path.open('r', encoding='utf8') as fp:
            yield from self._parse_file(path, fp)

    def _parse_file(self, path, fp):
        brace_lvl = 0
        ccmd = []
        cmd_lineno = None
        tk = Tokenizer(fp)
        for typ, val in tk:
            #print typ, repr(val)
            if typ == CHAR:
                if brace_lvl == 0 and (val == '\n' or val == ';'):
                    if ccmd:
                        yield path, cmd_lineno, ccmd
                        ccmd = []
                    cmd_lineno = None
                    continue
                
                if val == '{':
                    brace_lvl += 1
                elif val == '}':
                    if brace_lvl > 0:
                        brace_lvl -= 1
            elif typ == WORD:
                if val == '\n':
                    continue
                
            if cmd_lineno is None:
                cmd_lineno = tk.lineno
            ccmd.append(val)

        if ccmd:
            yield filname, cmd_lineno, ccmd
                
    def parse_with_include(self, path):
        for cmd in self.parse_file(path):
            args = cmd[2]
            if len(args) >= 2 and args[0] == 'require':
                nfil = path.parent / args[1]
                yield from self.parse_with_include(nfil)
            else:
                yield cmd
                
    def reset(self):
        self.seen.clear()

util.update(globals())

if __name__ == '__main__':
    import sys
    cfg = Config()
    for fn, line, cmd in cfg.parse_with_include(sys.argv[1]):
        print(fn, line, cmd)



