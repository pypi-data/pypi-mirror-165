import sys
import time
import os
import re
import asyncio

import socket

from os.path import getmtime, dirname, join, abspath

from io import StringIO

from firewall.core import *
from firewall.modules.iptables import *

class Options(object):
    def __init__(self):
        self.failcnt = 4
        self.bantime = 30 * 60
        self.exempt_addrs = []

CHAINNAME = "SSHkill"

options = Options()
old_options = None
failcnt = {}
bantimers = {}

class BanTimer(object):
    def __init__(self, btime, addr):
        self.addr = addr
        self.endtime = time.time() + btime
        self.time = btime
        self.task = asyncio.create_task(self.unban_timer())
        
        if addr in failcnt:
            del failcnt[addr]
        
    async def unban_timer(self):
        await asyncio.sleep(self.time)
        print("SSH ban expired for address %s" % self.addr, file=sys.stderr)
        try:
            del bantimers[self.addr]
        except KeyError:
            pass
        return await reload_tables()
        
    def cancel(self):
        self.task.cancel()

def ban(addr):
    #reset the counter
    bantimers[addr] = BanTimer(options.bantime, addr)

    asyncio.create_task(reload_tables())

def badlogin(addr):
    iaddr = iptables.pack_addr(addr)
    for ex in options.exempt_addrs:
        try:
            net = get_network(ex)
            a = net._getaddr()
            m = net._getmask()
            if iaddr & m == a & m:
                return
        except NetworkUnavail:
            pass

    if addr in bantimers:
        # Address already banned -- this can happen since sshd gives
        # the user three tries before disconnecting, and the filter
        # only stops new connections.
        return
    
    cnt = failcnt.get(addr, 0)
    cnt += 1
    failcnt[addr] = cnt
    
    if cnt >= options.failcnt:
        print("%d failed logins from %s, banning for %d seconds" % (cnt, addr, options.bantime), file=sys.stderr)
        ban(addr)
    else:
        print('%d out of %d failed logins from %s' % (cnt, options.failcnt, addr), file=sys.stderr)

def goodlogin(addr):
    reload = False
    try:
        del bantimers[addr]
        reload = True
    except KeyError:
        pass
    
    try:
        del failcnt[addr]
    except KeyError:
        pass

    if reload:
        reload_tables().start()

def fill_tables(filter, nat, mangle, raw):
    filter_sshkill = filter[CHAINNAME]
    #raw_sshkill = raw[CHAINNAME]
    
    for tmr in bantimers.keys():
        filter_sshkill.add(Rule('-p tcp -s %s' % tmr, 'DROP'))

    filter['INPUT'].add(Rule('-p tcp -m tcp --dport 22 --tcp-flags SYN,RST,ACK SYN', CHAINNAME))
    #raw['PREROUTING'].add(Rule('-p tcp -m tcp --dport 22 --tcp-flags SYN,RST,ACK SYN', CHAINNAME))

@admin_command
async def command_bantime(source, tstr):
    options.bantime = parsetime(tstr)
    return (0, 'ok')

@admin_command
async def command_exempt(source, *addrs):
    options.exempt_addrs.extend(addrs)
    return (0, 'ok')

@admin_command
async def command_failcnt(source, n):
    options.failcnt = int(n)
    return (0, 'ok')

@admin_command
async def command_badlogin(source, addr, user):
    badlogin(addr)
    return (0, 'ok')
    
@admin_command
async def command_goodlogin(source, addr, user):
    goodlogin(addr)
    return (0, 'ok')

@admin_command
async def command_force(source, addr, timestr):
    bantime = parsetime(timestr)
    print('SSH ban forced for %s, %d seconds' % (addr, bantime), file=sys.stderr)
    try:
        bantimers[addr].cancel()
    except KeyError:
        pass
    
    bantimers[addr] = BanTimer(bantime, addr)
    return await reload_tables_for_cmd(source, 'ban successfully added')

@admin_command
async def command_cancel(cmd, addr):
    try:
        bantimers[addr].cancel()
        del bantimers[addr]
        print("SSH ban canceled for address %s" % addr, file=sys.stderr)
        return await reload_tables_for_cmd(source, 'ban canceled')
    except KeyError:
        return (2, 'address was not banned')
    
@user_command
async def command_list(source):
    ctime = time.time()
    resp = StringIO()
    for v in list(bantimers.values()):
        resp.write('%s\t%d\n'%(v.addr, int(v.endtime - ctime)))

    return (0, resp.getvalue())
    
@admin_command    
async def command_clear(source):
    print('SSH bans cleared', file=sys.stderr)
    for v in list(bantimers.values()):
        v.cancel()
        
    bantimers.clear()
    failcnt.clear()
    return await reload_tables_for_cmd(source, 'bans cleared')


def init():
    clear_config()

def cleanup():
    for v in list(bantimers.values()):
        v.cancel()
        
    bantimers.clear()

def clear_config():
    global options, old_options
    old_options = options
    options = Options()

def config_loaded():
    global old_options
    old_options = None

