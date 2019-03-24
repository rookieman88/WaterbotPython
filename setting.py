import datetime

class Settings:
    def __init__(self):
        self.token = "token"
        self.prefix = "~"
        self.log_file = "msg_log.rtl"
        self.actvity_log_file = "actvity_log.rtl"
        self.owner_id = "417571990820618250"
        self.online_notice_channel = "528463466231627786"
        self.err_log_channel = "id"
        self.version = "2"
        self.copy = "© %s Team." % datetime.datetime.now().year
        self.embed_color = 0xb2ebf4
        self.error_embed_color = 0xb2ebf4
        self.hangul_clock_upload = "url"



# ------ 이 아래는 건들지 마세요 ----- #

import ctypes

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

    def __init__(self):
        # have to initialize this to the size of MEMORYSTATUSEX
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()
