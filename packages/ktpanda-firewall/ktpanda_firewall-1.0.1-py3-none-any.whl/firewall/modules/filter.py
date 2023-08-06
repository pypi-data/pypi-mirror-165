import sys
import re
import asyncio

from io import StringIO

from firewall.core import *
from firewall.modules.iptables import *

pinholes = {}
protect = {}

class Pinhole(object):
    def __init__(self, rulesrc, proto='', portrange='', source='', interface=''):
        self.rulesrc = rulesrc

        if (portrange and not proto) or proto == 't':
            proto = 'tcp'
        elif proto == 'u':
            proto = 'udp'

        self.proto = proto
        self.portrange = portrange
        self.source = source
        self.interface = interface
        self.active = True

    def ident(self):
        return (self.proto, self.portrange, self.source, self.interface)

    def __str__(self):
        return ':'.join(self.ident())

    def genrule(self):
        if self.proto:
            ruletxt = '-m %s -p %s' % (self.proto, self.proto)
        else:
            ruletxt = ''

        if self.portrange:
            lst = self.portrange.split('-')
            if len(lst) == 1:
                ruletxt += ' --dport %s' % lst[0]
            else:
                ruletxt += ' --dport %s:%s' % (lst[0], lst[1])

        if self.source:
            ruletxt += ' --source %s' % get_network(self.source).getnet()

        if self.interface:
            ruletxt += ' --in-interface %s' % get_network(self.interface).getiface()

        return Rule(ruletxt, 'RETURN')

class Protect(object):
    def __init__(self, rulesrc, ifaces, nets):
        self.rulesrc = rulesrc
        self.ifaces = tuple(sorted(ifaces))
        self.nets = nets

    def ident(self):
        return self.ifaces

    def gen_table_name(self):
        return 'from_' + '_'.join(self.ifaces)

def fill_tables(filter, nat, mangle, raw):
    filterin = filter['INPUT']
    filterout = filter['OUTPUT']
    filterfwd = filter['FORWARD']
    servers = filter['SERVERS']

    rawpre = raw['PREROUTING']

    filterin.add(Rule('-p tcp -m tcp --tcp-flags SYN,RST,ACK SYN', 'SERVERS'))
    filterin.add(Rule('-p udp -m udp -m conntrack --ctstate NEW', 'SERVERS'))

    servers.add(Rule('-i lo', "RETURN"))

    for p in list(pinholes.values()):
        if p.active:
            try:
                servers.add(p.genrule())
            except NetworkUnavail as e:
                pass
                #print >> sys.stderr, "interface not found: %s" % e

    for p in list(protect.values()):
        tblname = p.gen_table_name()
        tbl = raw[tblname]
        for iface in p.ifaces:
            try:
                rawpre.add(Rule('--in-interface %s' % get_network(iface).getiface(), tblname))
            except NetworkUnavail as e:
                pass
                #print >> sys.stderr, "interface not found: %s" % e

        tbl.add(Rule('-m conntrack --ctstate ESTABLISHED', 'RETURN'))
        for net in p.nets:
            try:
                tbl.add(Rule('--destination %s' % get_network(net).getnet(), 'DROP'))
            except NetworkUnavail as e:
                pass
                #print >> sys.stderr, "interface not found: %s" % e
    servers.add(Rule('', 'DROP'))

@admin_command
async def pin(source, *args):
    added = []
    for v in args:
        lst = v.split(':')
        ph = Pinhole(source, *lst)
        ph = pinholes.setdefault(ph.ident(), ph)
        added.append(str(ph))

    return await reload_tables_for_cmd(source, 'added pinholes: %s' % ','.join(added))

@admin_command
async def rmpin(source, *args):
    deleted = []
    for v in args:
        v = str.split(':')
        ph = Pinhole(source, *args)
        try:
            del pinholes[ph.ident()]
            deleted.append(str(ph))
        except KeyError:
            pass


    return await reload_tables_for_cmd(source, 'deleted pinholes: %s' % ','.join(deleted))

@admin_command
async def flushtemp(source):
    deleted = []
    for k, ph in list(pinholes.items()):
        if ph.source == SOURCE_ADMIN:
            del pinholes[k]
            deleted.append(str(ph))
    return await reload_tables_for_cmd(source, 'deleted pinholes: %s' % ','.join(deleted))


@admin_command
async def lspin(source):
    txt = StringIO()
    for k, ph in list(pinholes.items()):

        txt.write('%s/%s' % (ph.portrange or '<any>', ph.proto or '<any>'))
        if ph.interface:
            txt.write(', from iface %s' % ph.interface)

        if ph.source:
            txt.write(', from source %s' % ph.source)
        txt.write('\n')
    return (0, txt.getvalue())

@admin_command
async def command_protect(source, *args):
    ifaces = []
    nets = []
    i = iter(args)
    for v in i:
        if v == 'from':
            break
        nets.append(v)
    for v in i:
        ifaces.append(v)

    prot = Protect(source, ifaces, [])
    prot = protect.setdefault(prot.ident, prot)
    prot.nets.extend(nets)

    return await reload_tables_for_cmd(source, 'added protect')

def clear_config():
    protect.clear()
    for k, ph in list(pinholes.items()):
        if ph.source == SOURCE_CONFIG:
            del pinholes[k]

def cleanup():
    pass

def init():
    pass
