from ctypes import *
import socket
from sys import platform

__all__ = ['NetAddr',
           'getifaddrs', 'addr_to_long', 'long_to_addr']
 
class ifaddrs_ifa_ifu(Union):
    _fields_ = [ 
        ("ifu_broadaddr", c_void_p),
        ("ifu_dstaddr",   c_void_p)  
        ]
    
class ifaddrs(Structure):
    _fields_ = [
        ("ifa_next",    c_void_p),
        ("ifa_name",    c_char_p),
        ("ifa_flags",   c_uint),
        ("ifa_addr",    c_void_p),
        ("ifa_netmask", c_void_p),
        ("ifa_ifu",     ifaddrs_ifa_ifu),
        ("ifa_data",    c_void_p)
        ]
class sockaddr(Structure):
    _fields_ = [
        ("sa_family", c_uint16),
        ("sa_data",   (c_uint8 * 14) ) 
        ]

class in_addr(Union):
    _fields_ = [
        ("s_addrstr",  (c_char * 4) ),
        ("s_addr", c_uint32),
    ]
    
class sockaddr_in(Structure):
    _fields_ = [
        ("sin_family", c_short),
        ("sin_port",   c_ushort),
        ("sin_addr",   in_addr),
        ("sin_zero",   (c_char * 8) ), # padding
        ]
    
class in6_addr(Union):
    _fields_ = [
        ("s6_addr",  (c_uint8 * 16) ),
        ("s6_addrstr", (c_char * 16) ),
        ]
    
class sockaddr_in6(Structure):
        _fields_ = [
            ("sin6_family",   c_short),
            ("sin6_port",     c_ushort),
            ("sin6_flowinfo", c_uint32),
            ("sin6_addr",     in6_addr),
            ("sin6_scope_id", c_uint32),
        ]

class NetAddr(object):
    def __init__(self, iface=None, family=0, addr=0, mask=0, scope=0):
        self.family = family
        
        self.iface = iface
        
        if isinstance(addr, str):
            addr = addr_to_long(self.family, addr)
            
        if isinstance(mask, str):
            mask = addr_to_long(self.family, mask)
        
        self.addr = addr
        self.mask = mask
        bits = 128
        while bits and not (mask & 1):
            bits -= 1
            mask >>= 1
        self.bits = bits
        self.scope = scope

    def getaddr(self):
        return long_to_addr(self.family, self.addr)

    def getmask(self):
        return long_to_addr(self.family, self.mask)

    def getnetaddr(self):
        return long_to_addr(self.family, self.addr & self.mask)

    def getbcastaddr(self):
        return long_to_addr(self.family, self.addr | ~self.mask)

    def getnet(self):
        return '%s/%d' % (long_to_addr(self.family, self.addr & self.mask), self.bits)

    def getiface(self):
        return (self.iface or '<none>')

    def copy(self, iface=None, addr=None, mask=None, scope=None):
        if iface is None:
            iface = self.iface
        if addr is None:
            addr = self.addr
        if mask is None:
            mask = self.mask
        if scope is None:
            scope = self.scope
        return NetAddr(iface, self.family, addr, mask, scope)

    def __repr__(self):
        return 'NetAddr(%r, %d, %r, %r, %r)' % (self.iface, self.family, self.getaddr(), self.getmask(), self.scope)

def pstr_to_long(s):
    addr = 0
    for c in str(s):
        addr <<= 8
        addr += ord(c)
    return addr

def addr_to_long(family, str):
    try:
        paddr = socket.inet_pton(family, str)
    except socket.error:
        raise ValueError('invalid IP address: %r' % str)
    return pstr_to_long(paddr)

def long_to_addr(family, addr):
    bits = 32
    if family == socket.AF_INET6:
        bits = 128
    paddr = ''.join(chr((addr >> i) & 255) for i in range(bits - 8, -8, -8))
    #print family, addr, repr(paddr)
    return socket.inet_ntop(family, paddr)


def get_raw_data(cto):
    return string_at(addressof(cto), sizeof(cto))
    

libc = CDLL("libc.so.6")

def getifaddrs():
    ptr = c_void_p(None)
    if libc.getifaddrs(pointer(ptr)):
        return
    
    ifa = ifaddrs.from_address(ptr.value)
    result = {}
 
    while True:
        name = ifa.ifa_name

        iface = result.get(name)
        if iface is None:
            iface = result[name] = []
        if ifa.ifa_addr:
            sa = sockaddr.from_address(ifa.ifa_addr)
            family = sa.sa_family
             
        addrobj = None
 
        if family == socket.AF_INET:
            addr = 0
            netmask = 0
            
            if ifa.ifa_addr is not None:
                si = sockaddr_in.from_address(ifa.ifa_addr)
                addr = pstr_to_long(get_raw_data(si.sin_addr))
                
            if ifa.ifa_netmask is not None:
                si = sockaddr_in.from_address(ifa.ifa_netmask)
                netmask = pstr_to_long(get_raw_data(si.sin_addr))
            addrobj = NetAddr(name, socket.AF_INET, addr, netmask)
                
        elif family == socket.AF_INET6:
            addr = 0
            netmask = 0
            scope = 0
            if ifa.ifa_addr is not None:
                si = sockaddr_in6.from_address(ifa.ifa_addr)
                addr = pstr_to_long(get_raw_data(si.sin6_addr.s6_addr))
                
                if (addr >> 112) & 0xff80 == 0xfe80:
                    scope = si.sin6_scope_id
                    
            if ifa.ifa_netmask is not None:
                si = sockaddr_in6.from_address(ifa.ifa_netmask)
                netmask = pstr_to_long(get_raw_data(si.sin6_addr.s6_addr))
 
            addrobj = NetAddr(name, socket.AF_INET6, addr, netmask, scope)
 
        if addrobj:
            iface.append(addrobj)
 
        if ifa.ifa_next:
            ifa = ifaddrs.from_address(ifa.ifa_next)
        else:
            break
 
    libc.freeifaddrs(ptr)
    return result

if __name__ == '__main__':
    print(getifaddrs())
