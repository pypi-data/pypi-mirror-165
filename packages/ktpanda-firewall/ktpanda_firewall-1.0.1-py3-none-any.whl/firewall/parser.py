import sys
import re
import socket
from firewall import util
from firewall.getifaddrs import *

public = util.public(globals())

class Token(object):
    def __init__(self, pat):
        self.rx = re.compile(pat)
        
    def match(self, txt, pos):
        m = self.rx.match(txt, pos)
        if m:
            return self.getval(m), m.end()
        return None, None

    def getval(self, m):
        grp = m.groups()
        if grp:
            return grp[0]
    def __repr__(self):
        return '<tk /%s/>' % self.rx.pattern
public(Token)


class AddrExpr(object):
    def eval(self, ctx):
        pass
    
    def filter(self, ctx, addr):
        for myaddr in self.eval(ctx):
            if myaddr.family == addr.family:
                mask = myaddr.mask
                if myaddr.addr & mask == addr.addr & mask:
                    return True
        return False
    
    def get_iface(self, ctx):
        l = self.eval(ctx)
        if l:
            return l[0].iface or None
        else:
            return None

class AddrLiteral(AddrExpr):
    def __init__(self, v):
        self.v = v

    def eval(self, ctx):
        return [self.v]

    def __repr__(self):
        return '%s/%d' % (self.v.getaddr(), self.v.bits)

class AliasExpr(AddrExpr):
    def __init__(self, name):
        self.name = name

    def eval(self, ctx):
        try:
            a = ctx.getalias(self.name)
        except KeyError:
            return []
        return a.eval(ctx)

    def filter(self, ctx, addr):
        try:
            a = ctx.getalias(self.name)
        except KeyError:
            return False
        return a.filter(ctx, addr)
    
    def __repr__(self):
        return self.name
    
class IfaceExpr(AddrExpr):
    def __init__(self, name, mask=None):
        self.name = name
        self.mask = None

    def getaddrs(self):
        if self.mask is None:
            return ctx.getifaceaddrs(self.name)
        addrs = [a.copy() for a in ctx.getifaceaddrs(self.name)]
        for a in addrs:
            a.mask = self.mask

    def eval(self, ctx):
        return ctx.getifaceaddrs(self.name)

    def __repr__(self):
        return '@' + self.name
    
class BinOp(AddrExpr):
    rtassoc = False
    postop = False
    prec = 3
    op = 'null'
    def __init__(self, l, r=None):
        self.l = l
        self.r = r

    def __repr__(self):
        if self.postop:
            return '(%r %s)' % (self.l, self.op)
        else:
            return '(%r %s %r)' % (self.l, self.op, self.r)

nullop = BinOp(None)
nullop.prec = -1

class SetInterface(AddrExpr):
    postop = True
    prec = 0
    def __init__(self, iface, l=None):
        self.l = l
        self.iface = iface
    def __repr__(self):
        return '(%r @%s)' % (self.l, self.iface)

    def eval(self, ctx):
        return [a.copy(iface=self.iface) for a in self.l.eval(ctx)]

    def __call__(self, l, r):
        return SetInterface(self.iface, l)
    
    def get_iface(self, ctx):
        return self.iface
class LogOr(BinOp):
    prec = 1
    op = '|'

    def eval(self, ctx):
        return self.l.eval(ctx) + self.r.eval(ctx)

    def filter(self, ctx, addr):
        return self.l.filter(ctx, addr) or self.r.filter(ctx, addr)

    
class Merge(LogOr):
    prec = 3
    op = '+'

    def eval(self, ctx):
        aa = self.l.eval(ctx)
        ba = self.r.eval(ctx)
        ret = []
        for a in aa:
            for b in ba:
                if a.family != b.family:
                    continue
                na = (a.addr & a.mask) | (b.addr & ~a.mask)
                ret.append(NetAddr(a.iface, a.family, na, a.mask | b.mask, a.scope))
        return ret

class LogAnd(LogOr):
    rtassoc = True
    prec = 2
    op = '&'
    def eval(self, ctx):
        return [a for a in self.l.eval(ctx) if self.r.filter(ctx, a)]

    def filter(self, ctx, addr):
        return self.l.filter(ctx, addr) and self.r.filter(ctx, addr)

class Bracket(LogAnd):
    rtassoc = False
    postop = True
    def __init__(self, r):
        self.l = nullop
        self.r = r
    
    def __call__(self, l, r):
        return LogAnd(l, self.r)

class LogNot(LogOr):
    op = '!'
    def eval(self, ctx):
        return self.l.eval(ctx)

    def filter(self, ctx, addr):
        return not self.l.filter(ctx, addr)

    def __repr__(self):
        return '(%s%r)' % (self.op, self.l)


tkiface = Token(r'\s*@\s*([_a-zA-Z][-a-zA-Z0-9]*\+?)')
tkalias = Token(r'\s*([_a-zA-Z][-a-zA-Z0-9]*)')

# _not_ meant to check for valid address!
tkipv6 = Token(r'\s*([0-9a-fA-F]*:[0-9a-fA-F:.]+)')
tkipv4 = Token(r'\s*([0-9.]+)')
tkchar = Token(r'\s*([,\|&\[\]\(\)\!+])')
tknetmask = Token(r'\s*/\s*(\d+)')

class AddrParser(object):
    maxlvl = 3
    
    def __init__(self, txt, pos=0):
        self.txt = txt
        self.pos = pos
        self.lpos = None

    def read(self, *types):
        self.lpos = self.pos
        for tk in types:
            v, e = tk.match(self.txt, self.pos)
            if e is not None:
                self.pos = e
                return tk, v
        return None, None

    def back(self):
        self.pos = self.lpos

    def isend(self):
        return self.pos >= len(self.txt)

    def error(self):
        #print 'error at %d %r' % (self.pos, self.txt[self.pos:])
        raise ValueError('invalid expression')

    def getalias(self, alias):
        try:
            return self.aliases[alias]
        except KeyError:
            raise NetworkUnavail

    def make_addr(self, family, val, size):
        mask = (1 << size) - 1
        tk, v = self.read(tknetmask)
        if v:
            mask &= ~((1 << (size - int(v))) - 1)
        else:
            self.back()
        
        return AddrLiteral(NetAddr('', family, val, mask, 0))

    def rest(self):
        return self.txt[self.pos:]
    
    def read_op(self):
        tk, v = self.read(tkchar, tkiface)
        if tk is None:
            return nullop
        
        if tk == tkchar:
            if v == '|' or v == ',':
                return LogOr
            if v == '&':
                return LogAnd
            if v == '+':
                return Merge
            if v == '[':
                self.back()
                l = self.parse_atom()
                return Bracket(l)
        elif tk == tkiface:
            return SetInterface(v)
        return nullop
    
    def parse_atom(self):
        tk, v = self.read(tkipv6, tkalias, tkiface, tkipv4, tkchar)
        if tk == tkalias:
            return AliasExpr(v)
        if tk == tkiface:
            return IfaceExpr(v)
        if tk == tkipv4:
            dots = v.count('.')
            if dots > 3:
                self.error()
            elif dots < 3:
                v += '.0' * (3 - dots)
            return self.make_addr(socket.AF_INET, v, 32)
        if tk == tkipv6:
            return self.make_addr(socket.AF_INET6, v, 128)
        if tk == tkchar:
            if v == '!':
                return LogNot(self.parse_atom())
            if v == '(' or v == '[':
                e = self.parse_expr()
                tk, nv = self.read(tkchar)
                if (v == '(' and nv != ')') or (v == '[' and nv != ']'):
                    self.error()
                return e
        self.error()
        
    def parse_expr(self, minlvl=0, maxlvl=None):
        if maxlvl is None:
            maxlvl = self.maxlvl

        clr = None, None, None
        maxlvl -= minlvl
        stk = [clr] * (maxlvl)
        clvl = maxlvl
        lf = self.parse_atom()

        ret = prev = op = lastop = None
        while True:
            if op:
                if prev and op.rtassoc and prev.r:
                    prev.r = op(prev.r, ret)
                    prev = prev.r
                else:
                    prev = lf = op(lf, ret)

            op = lastop or self.read_op()
            rt_prec = op.prec - minlvl
            if rt_prec != clvl:
                if clvl:
                    lastop = op
                    ret = lf
                    clvl -= 1
                    prev, op, lf = stk[clvl]
                    if not lf:
                        lf = ret
                    stk[clvl] = clr
                    continue
                else:
                    self.back()
                    #self.pos = self.op_start
                    return lf
            lastop = None
            
            if op.postop:
                ret = None
                clvl = maxlvl
                continue
            if clvl == maxlvl:
                ret = self.parse_atom()
            else:
                stk[clvl] = prev, op, lf
                prev = op = None
                lf = self.parse_atom()
                clvl = maxlvl
                continue
public(AddrParser)

class EvalContext(object):
    def __init__(self):
        self.aliases = {}
        self.ifaces = {}

    def getalias(self, name):
        return self.aliases[name]

    def getifaceaddrs(self, name):
        return self.ifaces[name]

    def updateifaces(self):
        self.ifaces = getifaddrs()
public(EvalContext)
