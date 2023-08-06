import traceback
import struct
import os
import socket
import asyncio

from .util import Result

RESP_OK = 0
ERR_UNKNOWN_EXCEPTION = 257
ERR_MALFORMED_COMMAND = 258
ERR_INVALID_MODULE = 259
ERR_INVALID_FUNCTION = 260
ERR_COMMAND_LOST = 261
ERR_ACCESS_DENIED = 262

def split_mod_func(args):
    modfunc = args[0].split('.', 1)
    module = modfunc[0]
    if len(modfunc) == 1:
        func = args[1]
        args = args[2:]
    else:
        func = modfunc[1]
        args = args[1:]
    return module, func, args

async def command_handler(writer, tag, args, handler):
    try:
        code, text = (await handler(args))
    except Exception as exc:
        code = ERR_UNKNOWN_EXCEPTION
        text = traceback.format_exc()
        
    data = text.encode('utf8')
    writer.write(struct.pack(">IIH", tag, code, len(data)) + data)
    asyncio.create_task(writer.drain())

async def command_conn(reader, writer, handler):
    try:
        while True:
            dat = await reader.readexactly(4)
            if len(dat) < 4:
                break
        
            tag, = struct.unpack(">I", dat)
            args = []
            while True:
                dat = await reader.readexactly(2)
                ln, = struct.unpack(">H", dat)
                if ln == 65535:
                    break
            
                dat = await reader.readexactly(ln)
                args.append(dat.decode('utf8', 'ignore'))
            
            asyncio.create_task(command_handler(writer, tag, args, handler))
    except asyncio.IncompleteReadError:
        pass
    finally:
        writer.close()

async def command_server(path, handler, mode):
    try:
        os.unlink(path)
    except:
        pass

    server = await asyncio.start_unix_server(lambda reader, writer: command_conn(reader, writer, handler), path)
    os.chmod(path, mode)
    return server

class Client:
    def __init__(self, path):
        self.path = path
        self.reader = None
        self.writer = None
        self.readtask = None
        self.next_tag = 42
        self.pending_commands = {}

    async def connect(self):
        self.reader, self.writer = await asyncio.open_unix_connection(self.path)

        self._resp_header = None

        self.readtask = asyncio.create_task(self.read_responses())

    async def read_responses(self):
        while True:
            try:
                dat = await self.reader.readexactly(10)
            except (asyncio.IncompleteReadError, asyncio.CancelledError):
                break

            tag, status, leng = struct.unpack(">IIH", dat)
            if leng:
                try:
                    stxt = await self.reader.readexactly(leng)
                except (asyncio.IncompleteReadError, asyncio.CancelledError):
                    break
            else:
                stxt = ""

            try:
                event = self.pending_commands[tag]
                del self.pending_commands[tag]
            except KeyError:
                continue

            event.set((status, stxt.decode('utf8', 'ignore')))

    async def send_command(self, *args):
        tag = self.next_tag
        self.next_tag += 1

        cmdcond = Result()
        self.pending_commands[tag] = cmdcond

        args = [arg.encode('utf8') for arg in args]
        
        data = (struct.pack(">I", tag) + b''.join(struct.pack(">H", len(s)) + s for s in args) +
               struct.pack(">H", 65535))

        self.writer.write(data)

        return await cmdcond.wait()
        
    def close(self):
        if self.readtask:
            self.readtask.cancel()

        self.readtask = None
        self.writer.close()
        self.reader = None
        self.writer = None
        self.socket = None
        
    def has_pending(self):
        return bool(self.pending_commands)
    
