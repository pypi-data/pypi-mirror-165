import sys
import traceback
import time
import socket
import asyncio

from io import BytesIO, StringIO


def httptime(tm = None):
    if tm is None:
        tm = time.time()
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(tm))

def msgpage(txt, extra=''):
    return '<html><head><title>%s</title></head><body>\n<h1>%s</h1>\n%s\n</body></html>'%(txt, txt, extra)

# Bare minimal http server.
# I use this instead of BaseHTTPServer because BaseHTTPServer does not
# support async I/O.

class HTTPRequest(object):
    def __init__(self, reader, writer):
        self.uri = ''
        self.headers_in = {}
        self.headers_out = {}
        self.body_buf = BytesIO()
        self.status = 200
        self.msg = 'OK'
        self.headers_out['content-type'] = 'text/html'
        self.reader = reader
        self.writer = writer
        
    def write(self, data):
        if isinstance(data, str):
            data = data.encode('utf8')
        self.body_buf.write(data)
        
    async def simpleerror(self, status, msg):
        self.write(msgpage(msg))
        return await self.send_response(status, msg)
        
    async def send_response(self, status=None, msg=None):
        response = StringIO()
        if status is None:
            status = self.status
        if msg is None:
            msg = self.msg

        body = self.body_buf.getvalue()
        self.putheader('date', httptime())
        self.putheader('content-length', str(len(body)))

        self.writer.write(('HTTP/1.1 %03d %s\r\n' % (status, msg)).encode('ascii'))
        
        for k, v in self.headers_out.items():
            k = k.title()
            lst = v.split('\n')
            for i in lst:
                self.writer.write(('%s: %s\r\n' % (k, i)).encode('utf8'))
        
        self.writer.write(b'\r\n')
        self.writer.write(body)
        await self.writer.drain()
        self.writer.close()
        await self.writer.wait_closed()

    def nocache(self):
        self.headers_out['cache-control'] = 'no-cache'
        self.headers_out['pragma'] = 'no-cache'
        self.headers_out['expires'] = httptime()
        
    def getheader(self, hdr, default=''):
        return self.headers_in.get(hdr, default)

    def putheader(self, hdr, value):
        self.headers_out[hdr] = value

    def getpeername(self):
        return self.writer.get_extra_info('peername')
    
    def redirect(self, loc, perm = False):
        self.putheader('location', loc)
        self.write(msgpage('Detour', '<a href="%s">linky</a>' % loc))
        return self.send_response((301 if perm else 302), 'Taking a detour')

async def handle_request(reader, writer, processor):
    req = HTTPRequest(reader, writer)

    reqline = (await reader.readline()).decode('utf8', 'ignore').rstrip('\r\n')
    reqd = reqline.split(' ')
    if len(reqd) != 3:
        return await req.simpleerror(400, 'Bad request')
    
    method = reqd[0]
    if method != 'GET':
        return await req.simpleerror(400, 'Unsupported method')
    
    req.uri = reqd[1]

    while True:
        reqline = (await reader.readline()).decode('utf8', 'ignore').rstrip('\r\n')
        if not reqline:
            break
        lst = reqline.split(':', 1)
        if len(lst) != 2:
            yield req.simpleerror(400, 'Malformed header')
            return
        req.headers_in[lst[0].lower()] = lst[1].strip()
        
    try:    
        await processor(req)
    except Exception as exc:
        req.write(msgpage('Sorry'))
        # Run it asynchronously so we can propagate the error
        asyncio.create_task(req.send_response(500, 'error'))
        raise
    
async def http_server(addr, taskfunc):
    return await asyncio.start_server(lambda reader, writer: handle_request(reader, writer, taskfunc), host=addr[0], port=addr[1])
    
