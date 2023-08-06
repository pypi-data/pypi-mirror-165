import sys
import re
import array
import struct
import traceback
import asyncio
import subprocess

import os
import socket
import fcntl

from io import StringIO

from firewall import util, command
from firewall.core import *

public = util.public(globals())

networks = {}
_iptables_running = False

addrstruct = struct.Struct(">I")

class NetworkUnavail(Exception):
    pass
public(NetworkUnavail)


@public
def pack_addr(str):
    if str is None:
        return None
    try:
        return addrstruct.unpack(socket.inet_aton(str))[0] 
    except socket.error:
        return 0

@public
def unpack_addr(addr):
    return '.'.join(str((addr >> i) & 255) for i in range(24, -8, -8))

def _get_iface_info(iface, ctl):
    buf = bytearray(40)
    iface = bytes(iface, 'utf-8')
    buf[:len(iface)] = iface
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        saddr = None
        try:
            fd = s.fileno()
            res = fcntl.ioctl(fd, ctl, buf)
            return struct.unpack_from(">I", buf, 20)[0]
        except OSError:
            raise NetworkUnavail(iface) from None

class Network(object):
    public = True
    def __init__(self, iface=None):
        self.iface = iface

    def _getaddr(self):
        pass

    def _getmask(self):
        pass

    def getaddr(self):
        return unpack_addr(self._getaddr())

    def getmask(self):
        return unpack_addr(self._getmask())

    def getnetaddr(self):
        addr = self._getaddr()
        mask = self._getmask()
        return unpack_addr(addr & mask)

    def getbcastaddr(self):
        addr = self._getaddr()
        mask = self._getmask()
        return unpack_addr(addr | ~mask)

    def getnet(self):
        addr = self._getaddr()
        mask = self._getmask()
        return '%s/%s' % (unpack_addr(addr & mask), unpack_addr(mask))

    def getiface(self):
        return (self.iface or '<none>')
    
class StaticNetwork(Network):
    public = True
    def __init__(self, addr, mask, iface=None):
        Network.__init__(self, iface)
        self.addr = addr
        self.mask = mask
        
    def _getaddr(self):
        return self.addr
    
    def _getmask(self):
        return self.mask

SIOCGIFADDR = 0x8915
SIOCGIFNETMASK = 0x891b

class NetInterface(Network):
    public = True
    def __init__(self, iface):
        Network.__init__(self, iface)

    def _getaddr(self):
        return _get_iface_info(self.iface, SIOCGIFADDR)
        
    def _getmask(self):
        return _get_iface_info(self.iface, SIOCGIFNETMASK)

@public
def parse_mask(mstr):
    try:
        nbits = int(mstr)
        if nbits <= 32:
            return 0xffffffff << (32 - nbits)
    except ValueError:
        pass

    return pack_addr(str)

@public
def parse_network(str):
    if str.startswith('@'):
        return NetInterface(str[1:])
    
    lst = str.split('/', 2)
    addr = pack_addr(lst[0])
    if len(lst) == 1:
        mask = 0xffffffff
    else:
        mask = parse_mask(lst[1])
        
    if len(lst) == 3:
        iface = lst[2]
    else:
        iface = None
    return StaticNetwork(addr, mask, iface)

@public
def get_network(nm):
    try:
        return networks[nm]
    except KeyError:
        return parse_network(nm)
    
@public
def get_network_list(str):
    return [get_network(nm) for nm in str.split(' ') if nm]

@public
def parsetime(t):
    lst = t.split(':',2)
    secs = 0.0
    for s in lst:
        secs *= 60
        if s:
            secs += float(s)
    return secs
    
class Rule(object):
    public = True
    def __init__(self, match='', action=''):
        self.match = match
        self.action = action

    def format(self):
        return '-j %s %s'%(self.action, self.match)

class Chain(object):
    public = True
    def __init__(self, name, policy='-'):
        self.name = name
        self.policy = policy
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

    def clear(self):
        self.rules = []

    def format(self):
        return ''.join('-A %s %s\n'%(self.name, r.format()) for r in self.rules)

class Table(object):
    public = True
    def __init__(self, name):
        self.name = name
        self.chains = {}

    def __getitem__(self, item):
        try:
            return self.chains[item]
        except KeyError:
            ret = Chain(item)
            self.chains[item] = ret
            return ret
        
    def __setitem__(self, item, value):
        self.chains[item] = value

    def format(self):
        lins = ['*%s\n' % self.name]
        
        for k, v in self.chains.items():
            lins.append(':%s %s [0:0]\n'%(k, v.policy))
        
        for k, v in self.chains.items():
            lins.append(v.format())
        lins.append('COMMIT\n')
        return ''.join(lins)

_reload_task = None

@public
async def reload_tables():
    global _reload_task
    initial_task = _reload_task

    if initial_task is not None and not initial_task.done():
        try:
            await initial_task
        except Exception:
            pass

    if initial_task is _reload_task:
        _reload_task = asyncio.create_task(_reload_tables())

    return await _reload_task

@public
async def _reload_tables():
    raw = Table('raw')
    raw['PREROUTING'] = Chain('PREROUTING', 'ACCEPT')
    raw['OUTPUT'] = Chain('OUTPUT', 'ACCEPT')

    filter = Table('filter')
    filterin = filter['INPUT'] = Chain('INPUT', 'ACCEPT')
    filterout = filter['OUTPUT'] = Chain('OUTPUT', 'ACCEPT')
    filterfwd = filter['FORWARD'] = Chain('FORWARD', 'ACCEPT')

    mangle = Table('mangle')
    mangle['INPUT'] = Chain('INPUT', 'ACCEPT')
    mangle['OUTPUT'] = Chain('OUTPUT', 'ACCEPT')
    mangle['FORWARD'] = Chain('FORWARD', 'ACCEPT')
    mangle['POSTROUTING'] = Chain('POSTROUTING', 'ACCEPT')
    mangle['PREROUTING'] = Chain('PREROUTING', 'ACCEPT')

    nat = Table('nat')
    natout = nat['OUTPUT'] = Chain('OUTPUT', 'ACCEPT')
    natpost = nat['POSTROUTING'] = Chain('POSTROUTING', 'ACCEPT')
    natpre = nat['PREROUTING'] = Chain('PREROUTING', 'ACCEPT')

    await callhook('fill_tables', filter, nat, mangle, raw)

    txt = raw.format() + mangle.format() + filter.format() + nat.format()

    try:
        proc = await asyncio.create_subprocess_exec(iptables_bin, stdin=subprocess.PIPE)
        await proc.communicate(txt.encode('utf8'))
        ret = await proc.wait()
    except (IOError, OSError):
        traceback.print_exc()
        ret = 1

    if ret:
        print("iptables-restore exited with code %d" % ret, file=sys.stderr)
    else:
        print("iptables loaded successfully", file=sys.stderr)

    return ret

@public
async def reload_tables_for_cmd(source, stxt):
    if source != SOURCE_CONFIG:
        stat = await reload_tables()
        if not stat:
            return (command.RESP_OK, stxt)
        else:
            return (stat, 'iptables error')

    return (command.RESP_OK, stxt)

def clear_config():
    global iptables_bin
    iptables_bin = '/sbin/iptables-restore'
    networks.clear()


@admin_command
async def command_reload(source):
    return await reload_tables_for_cmd(source, 'iptables loaded successfully')

@admin_command
async def command_network(source, name, val):
    networks[name] = get_network(val)
    return (command.RESP_OK, 'network defined')

@admin_command
async def command_iptables_bin(source, bin):
    global iptables_bin
    iptables_bin = bin
    
    return await reload_tables_for_cmd(source, 'ok')

@user_command
def listnets(source):
    ret = StringIO()
    for k, v in networks.items():
        print('%s = %s %s %s' % (k.ljust(15), v.getiface().ljust(8), v.getaddr().ljust(20), v.getnet()), file=ret)
    return (0, ret.getvalue())

async def config_loaded():
    return await reload_tables()

def init():
    clear_config()

def cleanup():
    pass

util.update(globals())
