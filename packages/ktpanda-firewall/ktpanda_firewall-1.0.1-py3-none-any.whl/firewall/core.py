import sys
import re
import traceback
import asyncio
import inspect

import types

import os

from collections import deque
from .config import Config

from pathlib import Path

from firewall import util, command

public = util.public(globals())

modules = {}

SOURCE_USER, SOURCE_ADMIN, SOURCE_CONFIG = range(3)
MODULE_PREFIX = 'firewall.modules.'

__commands__ = {}

class Command(object):
    public = True
    def __init__(self, func, admin):
        self.func = func
        self.admin = admin

    async def call(self, source, *args, **kwargs):
        if self.admin and source == SOURCE_USER:
            return (command.ERR_ACCESS_DENIED, 'access denied')
        return await self.func(source, *args, **kwargs)
    
def _command(func, admin):
    mod = sys.modules[func.__module__]
    try:
        cmd_dict = mod.__commands__
    except:
        cmd_dict = mod.__commands__ = {}
        
    name = func.__name__
    if name.startswith('command_'):
        name = name[8:]

    cmd_dict[name] = Command(func, admin)
    return func

@public
def user_command(func):
    return _command(func, False)

@public
def admin_command(func):
    return _command(func, True)

@public
def hook(f):
    def hookfunc(mod, called, q, args, kwargs):
        return f(*args, **kwargs)
    hookfunc.__name__ = f.__name__
    return hookfunc
    
@public
def after(*deps):
    def ret(f):
        f.deps = deps
        return f
    return ret

async def _callhook(mods, hookname, args, kwargs):
    called = set()
    q = deque(iter(mods.items()))
    while q:
        name, mod = q.popleft()
        called.add(name)
        
        try:
            func = getattr(mod, hookname)
        except AttributeError:
            continue
        
        task = None
        deps = getattr(func, 'deps', None)
        if deps:
            for dep in deps:
                if dep in mods and not dep in called:
                    q.append((name, mod))
                    break
            else:
                task = func(*args, **kwargs)

        task = func(*args, **kwargs)

        if inspect.isawaitable(task):
            await task

@public
def callhook(name, *args, **kwargs):
    return _callhook(modules, name, args, kwargs)


def modmtime(module):
    mfil = module.__file__
    return Path(mfil).stat().st_mtime

def do_import(name):
    mod = __import__(name)
    for c in name.split('.')[1:]:
        mod = getattr(mod, c)
    return mod

@public
def insert_module(name, log=True):
    modname = MODULE_PREFIX + name
    if name in modules:
        return modules[name]
    
    loaded_already = (modname in sys.modules)
        
    try:
        module = do_import(modname)
        module.__modtime__ = modmtime(module)

        module.init()
        modules[name] = module
        if log:
            print('module %s initialized' % name, file=sys.stderr)
    except:
        if not loaded_already and modname in sys.modules:
            del sys.modules[modname]
        raise
    return module
    
@public
def remove_module(mod):
    modname = mod.__name__
    name = modname.split('.')[-1]
    

    if name in modules or modules[name] != mod:
        raise ValueError("unknown module")

    mod.cleanup()
    if name in modules:
        del modules[name]

    if modname in sys.modules:
        del sys.modules[modname]

@public
def reload_module(mod):
    name = mod.split('.')[-1]
    remove_module(mod)
    insert_module(name, log = False)
    print('module %s reloaded' % name, file=sys.stderr)
    
def check_reload(module, force = False):
    modtime = modmtime(module)
    omodtime = module.__modtime__
    if force or modtime > omodtime:
        return reload_module(module)
    
    return module


@user_command
def lsmod(source):
    return (command.RESP_OK, '\n'.join(iter(modules.keys())))

def command_handler(source):
    async def handle_command(args):
        modname, funcnm, args = command.split_mod_func(args)

        if modname == 'core':
            dct = __commands__
        else:
            try:
                dct = modules[modname].__commands__
            except (KeyError, AttributeError):
                return (command.ERR_INVALID_MODULE, 'invalid module: %s' % modname)

        try:
            func = dct[funcnm]
        except KeyError:
            return (command.ERR_INVALID_MODULE, 'invalid function: %s.%s' % (modname, funcnm))
            
                
        return await func.call(source, *args)
    return handle_command

user_command_handler = command_handler(SOURCE_USER)
admin_command_handler = command_handler(SOURCE_ADMIN)
config_command_handler = command_handler(SOURCE_CONFIG)


def gen_config_files(path):
    if path.is_dir():
        for f in path.iterdir():
            if f.name.startswith('.') or f.suffix != '.conf':
                continue
            
            yield f
    else:
        yield path

@public
async def reload_config(forcemods = []):
    if forcemods:
        if forcemods[0] == 'all':
            forcemods = list(modules.keys())
            
        for m in forcemods:
            remove_module(modules[m])

    await callhook('clear_config')
    seen_mods = set()

    cfg = Config()

    curmod = 'core'
    
    current_mods = set(modules.keys())
    for fn in gen_config_files(Path(_config_file_name)):
        for fname, line, cmd in cfg.parse_with_include(fn):
            try:
                nm = cmd[0]
                if nm == '[':
                    if len(cmd) != 3 or cmd[2] != ']':
                        raise ValueError('invalid section header')
                    curmod = cmd[1]
                    if curmod != 'core':
                        seen_mods.add(curmod)
                        if not curmod in modules:
                            insert_module(curmod)
                else:
                    modlst = nm.split('.', 1)
                    if len(modlst) == 1:
                        module = curmod
                        func = modlst[0]
                    else:
                        module, func = modlst
                    await config_command_handler([module, func] + cmd[1:])
            except Exception as exc:
                traceback.print_exc()
                
    dead_mods = current_mods - seen_mods
    for m in dead_mods:
        try:
            remove_module(modules[m])
        except KeyError:
            pass

    for m in modules.values():
        m.__dict__.update(modules)
    
    return await callhook('config_loaded')
    
@admin_command
async def command_reload(source, *forcemods):
    await reload_config(forcemods)
    return (command.RESP_OK, 'config reloaded')


async def run_server(server):
    async with server:
        await server.serve_forever()

async def run(config, asockpath, usockpath, notify=None):
    global _config_file_name, _config
    _config_file_name = config

    servers = []
    
    servers.append(await command.command_server(asockpath, admin_command_handler, 0o600))
    if usockpath:
        servers.append(await command.command_server(usockpath, user_command_handler, 0o666))

    if notify:
        notify()

    await reload_config()


    
    await asyncio.gather(*[run_server(server) for server in servers])

util.update(globals())
if __name__ == '__main__':
    sys.modules['firewall.core'] = sys.modules[__name__]
    mydir = Path(__file__).parent

    init(mydir / 'config', mydir / 'control', mydir / 'ucontrol')
    
