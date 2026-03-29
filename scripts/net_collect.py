import ctypes
import signal
import threading
import argparse
import psutil
import sys
import getpass

from copy import deepcopy
from time import sleep





# This is a Python 3 demo of how to interact with the Nethogs library via Python. The Nethogs
# library operates via a callback. The callback implemented here just formats the data it receives
# and prints it to stdout. This must be run as root (`sudo python3 python-wrapper.py`).
# By Philip Semanchuk (psemanchuk@caktusgroup.com) November 2016
# Copyright waived; released into public domain as is.

# The code is multi-threaded to allow it to respond to SIGTERM and SIGINT (Ctrl+C).  In single-
# threaded mode, while waiting in the Nethogs monitor loop, this Python code won't receive Ctrl+C
# until network activity occurs and the callback is executed. By using 2 threads, we can have the
# main thread listen for SIGINT while the secondary thread is blocked in the monitor loop.

#######################
# BEGIN CONFIGURATION #
#######################

# You can use this to monitor only certain devices, like:
# device_names = ['enp4s0', 'docker0']
device_names = []

# LIBRARY_NAME has to be exact, although it doesn't need to include the full path.
# The version tagged as 0.8.7-44-g0fe341e that is installed in this container.

LIBRARY_NAME = 'libnethogs.so.0.8.6'

# EXPERIMENTAL: Optionally, specify a capture filter in pcap format (same as
# used by tcpdump(1)) or None. See `man pcap-filter` for full information.
# Note that this feature is EXPERIMENTAL (in libnethogs) and may be removed or
# changed in an incompatible way in a future release.
# example:
# FILTER = 'port 80 or port 8080 or port 443'
FILTER = None

#####################
# END CONFIGURATION #
#####################

# Here are some definitions from libnethogs.h
# https://github.com/raboof/nethogs/blob/master/src/libnethogs.h
# Possible actions are NETHOGS_APP_ACTION_SET & NETHOGS_APP_ACTION_REMOVE
# Action REMOVE is sent when nethogs decides a connection or a process has died. There are two
# timeouts defined, PROCESSTIMEOUT (150 seconds) and CONNTIMEOUT (50 seconds). AFAICT, the latter
# trumps the former so we see a REMOVE action after ~45-50 seconds of inactivity.
class Action():
    SET = 1
    REMOVE = 2

    MAP = {SET: 'SET', REMOVE: 'REMOVE'}

class LoopStatus():
    """Return codes from nethogsmonitor_loop()"""
    OK = 0
    FAILURE = 1
    NO_DEVICE = 2

    MAP = {OK: 'OK', FAILURE: 'FAILURE', NO_DEVICE: 'NO_DEVICE'}

# The sent/received KB/sec values are averaged over 5 seconds; see PERIOD in nethogs.h.
# https://github.com/raboof/nethogs/blob/master/src/nethogs.h#L43
# sent_bytes and recv_bytes are a running total
class NethogsMonitorRecord(ctypes.Structure):
    """ctypes version of the struct of the same name from libnethogs.h"""
    _fields_ = (('record_id', ctypes.c_int),
                ('name', ctypes.c_char_p),
                ('pid', ctypes.c_int),
                ('uid', ctypes.c_uint32),
                ('device_name', ctypes.c_char_p),
                ('sent_bytes', ctypes.c_uint64),
                ('recv_bytes', ctypes.c_uint64),
                ('sent_kbs', ctypes.c_float),
                ('recv_kbs', ctypes.c_float),
                )


def signal_handler(signal, frame):
    print('SIGINT received; requesting exit from monitor loop and program')
    lib.nethogsmonitor_breakloop()
    exit(0)


def dev_args(devnames):
    """
    Return the appropriate ctypes arguments for a device name list, to pass
    to libnethogs ``nethogsmonitor_loop_devices``. The return value is a
    2-tuple of devc (``ctypes.c_int``) and devicenames (``ctypes.POINTER``)
    to an array of ``ctypes.c_char``).

    :param devnames: list of device names to monitor
    :type devnames: list
    :return: 2-tuple of devc, devicenames ctypes arguments
    :rtype: tuple
    """
    devc = len(devnames)
    devnames_type = ctypes.c_char_p * devc
    devnames_arg = devnames_type()
    for idx, val in enumerate(devnames):
        devnames_arg[idx] = (val + chr(0)).encode('ascii')
    return ctypes.c_int(devc), ctypes.cast(
        devnames_arg, ctypes.POINTER(ctypes.c_char_p)
    )


def run_monitor_loop(lib, devnames):
    # Create a type for my callback func. The callback func returns void (None), and accepts as
    # params an int and a pointer to a NethogsMonitorRecord instance.
    # The params and return type of the callback function are mandated by nethogsmonitor_loop().
    # See libnethogs.h.
    CALLBACK_FUNC_TYPE = ctypes.CFUNCTYPE(
        ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(NethogsMonitorRecord)
    )

    filter_arg = FILTER
    if filter_arg is not None:
        filter_arg = ctypes.c_char_p(filter_arg.encode('ascii'))

    if len(devnames) < 1:
        # monitor all devices
        rc = lib.nethogsmonitor_loop(
            CALLBACK_FUNC_TYPE(network_activity_callback),
            filter_arg
        )
    else:
        devc, devicenames = dev_args(devnames)
        rc = lib.nethogsmonitor_loop_devices(
            CALLBACK_FUNC_TYPE(network_activity_callback),
            filter_arg,
            devc,
            devicenames,
            ctypes.c_bool(False)
        )

    if rc != LoopStatus.OK:
        print('nethogsmonitor_loop returned {}'.format(LoopStatus.MAP[rc]))
    else:
        print('exiting monitor loop')

## callback function that I did some modifications
def network_activity_callback(action, data):
    global procs
    #print(datetime.datetime.now().strftime('@%H:%M:%S.%f'))

    # Action type is either SET or REMOVE. I have never seen nethogs send an unknown action
    # type, and I don't expect it to do so.
    action_type = Action.MAP.get(action, 'Unknown')
    pid = data.contents.pid
    key = str(pid)+str(data.contents.name)
    if key in procs:
        procs[key].data_sent = data.contents.sent_bytes
        procs[key].data_recv = data.contents.recv_bytes
    else:
        procs[key] = ProcessNetworkData(pid, data.contents.name)
        procs[key].name = data.contents.name
        procs[key].pid = data.contents.pid
        procs[key].data_sent = data.contents.sent_bytes
        procs[key].data_recv = data.contents.recv_bytes
    
        
        '''
        try:
            procs[pid].name = data.contents.name
            procs[pid].pid = data.contents.pid
            procs[pid].data_sent = data.contents.sent_bytes
            procs[pid].data_recv = data.contents.recv_bytes
        except:
            print(f'impossible to create process data to {pid}')
        '''
     
    
    '''print('Action: {}'.format(action_type))
    print('Record id: {}'.format(data.contents.record_id))
    print('Name: {}'.format(data.contents.name))
    print('PID: {}'.format(data.contents.pid))
    print('UID: {}'.format(data.contents.uid))
    print('Device name: {}'.format(data.contents.device_name.decode('ascii')))
    print('Sent/Recv bytes: {} / {}'.format(data.contents.sent_bytes, data.contents.recv_bytes))
    print('Sent/Recv kbs: {} / {}'.format(data.contents.sent_kbs, data.contents.recv_kbs))
    print('-' * 30)'''


# class used to store network data

class ProcessNetworkData:
    def __init__(self, pid: int, name: str):
        self.pid: int = pid
        self.name: str  = name
        self.data_sent: int = 0
        self.data_recv: int = 0
    
    def save_network(self, filename: str, header=False) -> bool:
        try:
            with open(filename,'a') as f:
                if header:
                    f.write('Sent \t Recv\n')
                f.write('{sent}\t{recv}\n'.format(sent=self.data_sent,
                                                  recv=self.data_recv))
            return True
        except:
            return False
    
    def __repr__(self):
        return "(pid={0}; name={1};  data_sent={2}; data_recv={3}".format(
            self.pid, self.name, self.data_sent, self.data_recv
        )

    def __str__(self):
        return self.__repr__()


procs: dict[int, ProcessNetworkData] =  {}


#############       Main begins here      ##############

parser = argparse.ArgumentParser(description='collect the network statistics of each process while \
                                 monitored_name still running (must run as sudo)')

parser.add_argument('monitored_name', type=str, default='a.out',
                    help='Process name that is used as criteria stop (while one program with this name \
                        still running, the monitor keep tracking all process network usage)')
parser.add_argument('-o', '--output', dest='out_file', type=str, default='output.txt',
                    help='output filename to network transfer (one mesure by time)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                    help='enable prints in stdout')
parser.add_argument('-i','--interval-time', dest='interval_time', type=float, default=0.5,
                    help='time between measures')


args=parser.parse_args()


monitored_name: str = args.monitored_name
out_file: str = args.out_file
verbose: bool = args.verbose
interval_time = args.interval_time

me = getpass.getuser()

if verbose:
    print(args)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

lib = ctypes.CDLL(LIBRARY_NAME)

monitor_thread = threading.Thread(
    target=run_monitor_loop, args=(lib, device_names,)
)

#procs is a dict with pids as keys and DataProcess class (declared here) as values

monitored_pids = {}
lock_dict: threading.Lock = threading.Lock()


#wait until process start
if verbose:
    print(f'waiting for a process with name {monitored_name} starts...')

while monitored_pids == {}:
    sleep(interval_time)
    for p in psutil.process_iter():
        try:
            if p.name() == monitored_name:
                monitored_pids[p.pid] = True
        except:
            print(f'error in process {p.pid}', file=sys.stderr)
            

print(f"process {monitored_name} START!")

monitor_thread.start()

while monitored_pids != {}:
    monitor_thread.join(interval_time)
    for p in psutil.process_iter():
        if verbose:
            print(p)
        try:
            if (p.name() == monitored_name) and not (p.pid in monitored_pids):
                monitored_pids[p.pid] = True
        except:
            print("impossible to get information about process:", p.pid)
    pop_vals = []
    for p in monitored_pids:
        if not psutil.pid_exists(p):
            pop_vals.append(p)
    for p in pop_vals:
        monitored_pids.pop(p)
    if verbose:
        print(procs)
            
lib.nethogsmonitor_breakloop()

p:ProcessNetworkData

with open(out_file,'w') as f:
    f.write('pid\tname\tdata sent\tdata recv\n')
    for key in procs:
        p=procs[key]
        f.write(f'{p.pid}\t{p.name}\t{p.data_sent}\t{p.data_recv}\n')
    