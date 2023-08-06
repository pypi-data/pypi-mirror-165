import sys
import re
import asyncio

from io import StringIO

from firewall.core import *
from firewall.modules.iptables import *

class ManualRule(object):
    def __init__(self, table, chain, ruleargs, target):
        self.table = table
        self.chain = chain
        self.ruleargs = ruleargs
        self.target = target

rules = []


def filter_args(seq):
    for i in seq:
        if i.startswith('i:'):
            yield get_network(i[2:]).getiface()
        elif i.startswith('a:'):
            yield get_network(i[2:]).getaddr()
        elif i.startswith('m:'):
            yield get_network(i[2:]).getmask()
        elif i.startswith('b:'):
            yield get_network(i[2:]).getbcast()
        elif i.startswith('n:'):
            yield get_network(i[2:]).getnet()
        else:
            yield i

def fill_tables(filter, nat, mangle, raw):
    tbls = dict(filter = filter,
                nat = nat,
                mangle = mangle,
                raw = raw)

    for r in rules:
        try:
            ruletxt = ' '.join(filter_args(r.ruleargs))
            tbls[r.table][r.chain].add(Rule(ruletxt, r.target))
        except NetworkUnavail:
            pass
        except Exception as exc:
            print(str(exc), file=sys.stderr)

@admin_command
async def rule(source, table, chain, target, *args):
    #ruletxt = ' '.join((get_network(arg[1:]) if arg.startswith('$') else arg) for arg in args)
    rules.append(ManualRule(table, chain, args, target))
    return await reload_tables_for_cmd(source, 'ok')

def clear_config():
    del rules[:]

def init():
    pass

def cleanup():
    pass

