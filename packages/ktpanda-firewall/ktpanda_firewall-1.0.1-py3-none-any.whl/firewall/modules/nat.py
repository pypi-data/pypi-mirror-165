import sys
import re
import asyncio

from io import StringIO

from firewall.core import *
from firewall.modules.iptables import *

nat_nets = []
forward = []
public_iface = None
enable_dnat_loopback = False

class NatForward(object):
    def __init__(self, toaddr, sport, dport = None, nports = 1, proto='tcp'):
        if dport is None:
            dport = sport

        self.toaddr = toaddr
        self.proto = proto
        self.sport = sport
        self.dport = dport
        self.nports = nports

    def gen_rule(self, snataddr=None):
        if self.nports == 1:
            oport = str(self.sport)
            toport = str(self.dport)
        else:
            oport = '%d:%d' % (self.sport, self.sport + self.nports - 1)
            toport = '%d-%d' % (self.dport, self.dport + self.nports - 1)
        if snataddr:
            ruletxt = '-p %s -d %s --dport %s --to-source %s' % (self.proto, self.toaddr, toport.replace('-', ':'), snataddr)
            return Rule(ruletxt, 'SNAT')
        else:
            ruletxt = '-p %s --dport %s --to-destination %s:%s' % (self.proto, oport, self.toaddr, toport)
            return Rule(ruletxt, 'DNAT')

def fill_tables(filter, nat, mangle, raw):
    if not public_iface:
        return
    try:
        pubnet = get_network(public_iface)
        pubaddr = pubnet.getaddr()
    except NetworkUnavail as e:
        print("public interface not found: %s" % e, file=sys.stderr)
        return

    natout = nat['OUTPUT']
    natpost = nat['POSTROUTING']
    natpre = nat['PREROUTING']

    natmasq = nat['MASQ']

    portforward = nat['PORTFORWARD']

    natpre.add(Rule('--destination %s' % pubaddr, 'PORTFORWARD'))
    natout.add(Rule('--destination %s' % pubaddr, 'PORTFORWARD'))

    for f in forward:
        natmasq.add(f.gen_rule(pubaddr))

    for n in nat_nets:
        try:
            net = get_network(n).getnet()
            natmasq.add(Rule('--destination %s' % net, 'RETURN'))
            if enable_dnat_loopback:
                natpost.add(Rule('--source %s' % (net), 'MASQ'))
            else:
                natpost.add(Rule('--source %s --out-interface %s' % (net, pubnet.iface), 'MASQ'))
        except NetworkUnavail as e:
            pass
            #print >> sys.stderr, "interface not found: %s" % e

    natmasq.add(Rule('--to-source %s' % pubaddr, 'SNAT'))

    for f in forward:
        portforward.add(f.gen_rule())

def clear_config():
    global public_iface, enable_dnat_loopback
    public_iface = None
    enable_dnat_loopback = False
    del nat_nets[:]
    del forward[:]

@admin_command
async def masqnet(source, *args):
    for n in args:
        nat_nets.append(n)
    return await reload_tables_for_cmd(source, 'ok')

@admin_command
async def masqto(source, net):
    global public_iface
    public_iface = net
    return await reload_tables_for_cmd(source, 'ok')

@admin_command
async def fwd(source, addr, port, toport, nports, proto='tcp'):
    port = int(port)
    toport = int(toport)
    nports = int(nports)
    forward.append(NatForward(addr, port, toport, nports, proto))
    return await reload_tables_for_cmd(source, 'ok')

@admin_command
async def dnat_loopback(source, enable):
    global enable_dnat_loopback
    enable_dnat_loopback = enable.lower() in ('yes', 'true', '1')
    return await reload_tables_for_cmd(source, 'ok')

def init():
    pass

def cleanup():
    pass
