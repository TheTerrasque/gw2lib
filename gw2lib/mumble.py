import ctypes
import mmap
import socket, struct
import json
from common import Struct

class Link(ctypes.Structure):
    _fields_ = [
        ("uiVersion",       ctypes.c_uint32),
        ("uiTick",          ctypes.c_ulong),
        ("fAvatarPosition", ctypes.c_float * 3),
        ("fAvatarFront",    ctypes.c_float * 3),
        ("fAvatarTop",      ctypes.c_float * 3),
        ("name",            ctypes.c_wchar * 256),
        ("fCameraPosition", ctypes.c_float * 3),
        ("fCameraFront",    ctypes.c_float * 3),
        ("fCameraTop",      ctypes.c_float * 3),
        ("identity",        ctypes.c_wchar * 256),
        ("context_len",     ctypes.c_uint32),
        ("context",         ctypes.c_uint32 * (256/4)), # is actually 256 bytes of whatever
        ("description",     ctypes.c_wchar * 2048)

    ]

def Unpack(ctype, buf):
    cstring = ctypes.create_string_buffer(buf)
    ctype_instance = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(ctype)).contents
    return ctype_instance

def get_memfile():
    return mmap.mmap(-1, ctypes.sizeof(Link), "MumbleLink")

def get_data(memfile):
    memfile.seek(0)
    data = memfile.read(ctypes.sizeof(Link))
    result = Unpack(Link, data)
    return result

def ip_from_long(long):
    return socket.inet_ntoa(struct.pack('<L', long))

class Vector3(object):
    def __init__(self, data):
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]
        
    def __repr__(self):
        return "[%s,%s,%s]" % (self.x, self.y, self.z)
    
class GW2MumbleData(object):
    def __init__(self):
        self.memfile = get_memfile()
        self.update()
  
    def update(self):
        self.data = get_data(self.memfile)
        if self.data.identity:
            e = json.loads(self.data.identity)
            self.identity=Struct(**e)
        else:
            self.identity = None
        e = {
            "server_ip": ip_from_long(self.data.context[1]),
            #"world_id": self.data.context[9],
            "client_build": self.data.context[11],
            "player_position": Vector3(self.data.fAvatarPosition),
            "player_direction": Vector3(self.data.fAvatarFront),
            "camera_position": Vector3(self.data.fCameraPosition),
            "camera_direction": Vector3(self.data.fCameraPosition),
        }
        self.extra = Struct(**e)
