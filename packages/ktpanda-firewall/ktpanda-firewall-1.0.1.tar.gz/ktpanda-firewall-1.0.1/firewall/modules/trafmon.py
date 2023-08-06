import sys
import time
import os
import re
import asyncio

import random
import socket

from os.path import getmtime, dirname, join, abspath

from io import StringIO

from firewall import traflog
from firewall.core import *
from firewall.modules.iptables import *
from firewall.modules.manual import filter_args

class IptCounter(object):
    def __init__(self, ctrs, ruleargs):
        self.lastv = 0
        self.ctrs = ctrs
        self.ruleargs = ruleargs

    def update(self, nv):
        delta = nv - self.lastv
        if delta < 0:
            delta = nv
        #if delta > 3000000 * 5:
        #    print 'big delta! %d %d %d' % (delta, nv, self.lastv)
        self.lastv = nv
        for ctr in self.ctrs:
            ctr.delta += delta

CHAINBASE = "LOG_"
class TrafMon(object):
    def __init__(self):
        self.logdir = '/var/log/traflog'
        self.iptables_bin = '/sbin/iptables'
        self.interval = 5
        self.counters = {}
        self.iptctrs = []
        self.chainname = None
        self._update_task = None
        self._run_task = None
        
    def addcounter(self, name, ctrnames):
        path = join(self.logdir, name)
        ctr = traflog.TrafLog(path, len(ctrnames))
        ctr.seek_end()
        ctr.close()
        
        self.counters[name] = ctr

    async def _update_counters(self):
        if not self.chainname:
            return

        #print 'updating from %s' % (self.chainname)
        proc = await asyncio.create_subprocess_exec(self.iptables_bin, '-L', self.chainname, '-nxv', stdout=subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        ret = await proc.wait()

        lines = stdout.decode('utf8', 'ignore').splitlines()

        iptitr = iter(self.iptctrs)
        for ln in lines:
            m = rxbcount.match(ln)
            if m:
                try:
                    nxt = next(iptitr)
                    nxt.update(int(m.group(1)))
                except StopIteration:
                    pass
                
        ctime = traflog.gettime()
        for ctr in self.counters.values():
            ctr.write_counters(ctime)
        #print 'done updating'
        
    async def update_counters(self):
        #print 'starting update'
        if not self._update_task or self._update_task.done():
            self._update_task = asyncio.create_task(self._update_counters())
            
        #print 'waiting for update'
        await self._update_task
        #print 'done waiting'

    
    def new_chain(self):
        for i in self.iptctrs:
            i.lastv = 0
        ccn = self.chainname
        ncn = CHAINBASE + '%08X' % random.randrange(0, 1<<32)
        self.chainname = ncn
        #print 'new chain: %s -> %s' % (ccn, ncn)
        return ncn
        

    async def _run_update(self):
        while True:
            await self.update_counters()
            await asyncio.sleep(self.interval)

    def start(self):
        if not self._run_task:
            self._run_task = asyncio.create_task(self._run_update())
        
    def stop(self):
        if self._run_task:
            self._run_task.cancel()
            self._run_task = None
        
        for ctr in self.counters.values():
            ctr.close()
            
rxbcount = re.compile(r'\s*\d+\s+(\d+)')

monitor = TrafMon()
old_monitor = None

@admin_command
async def command_interval(source, tstr):
    monitor.interval = int(tstr)
    return (0, 'ok')

@admin_command
async def command_iptables_bin(source, tstr):
    monitor.iptables_bin = tstr
    return (0, 'ok')

@admin_command
async def command_logdir(source, tstr):
    monitor.logdir = tstr
    return (0, 'ok')

@admin_command
async def command_counter(source, name, *ctrnames):
    monitor.addcounter(name, ctrnames)
    return (0, 'ok')

@admin_command
async def command_rule(source, *args):
    itr = iter(args)
    ctrs = []
    for r in itr:
        if r == '--':
            break
        ctr, s, rn = r.partition('.')
        if s:
            rn = int(rn)
        else:
            ctr = r
            rn = 0
        ctrs.append(monitor.counters[ctr].ctrs[rn])
    
    monitor.iptctrs.append(IptCounter(ctrs, list(itr)))
    return (0, 'ok')

@asyncfunc
async def fill_tables(filter, nat, mangle, raw):
    await monitor.update_counters()
    chain = monitor.new_chain()
    
    filter_log = filter[chain]
    
    for iptc in monitor.iptctrs:
        ruletxt = ' '.join(filter_args(iptc.ruleargs))
        filter_log.add(Rule(ruletxt, 'NOOP'))
        
    noop = filter['NOOP']
    filter['INPUT'].add(Rule('', chain))
    filter['OUTPUT'].add(Rule('', chain))
    filter['FORWARD'].add(Rule('', chain))
    #raw['PREROUTING'].add(Rule('-p tcp -m tcp --dport 22 --tcp-flags SYN,RST,ACK SYN', CHAINNAME))

def init():
    pass

def cleanup():
    monitor.stop()
    
async def clear_config():
    global monitor, old_monitor
    await monitor.update_counters()
    
    monitor.stop()

    old_monitor = monitor
    monitor = TrafMon()
    
def config_loaded():
    global old_monitor
    monitor.start()

    old_monitor = None

