import psutil
import argparse
import getpass
import sys

from time import sleep

class DataProcess:
    def __init__(self, psutil_process: psutil.Process):
        self.ps: psutil.Process = psutil_process
        self.mem_usage: list[int] = []
        self.cpu_usage: list[float] = []
        self.cpu_times: psutil._pslinux.pcputimes = None

    def update_ps(self):
        try:
            self.ps.name()
        except:
            print(f"error: process {self.ps.name} does not exists")

    def insert_cpu_usage(self, verbose=False):
        usage = self.ps.cpu_percent()
        if verbose:
            print(f'inserting {usage} into usage list of {self.ps.name()}')
        self.cpu_usage.append(usage)
        times = self.ps.cpu_times()
        if verbose:
            print(f'inserting cpu times: {times} of {self.ps.name()}')
        self.cpu_times = times
    
    def insert_mem_usage(self, verbose=False):
        mem_info = self.ps.memory_full_info()
        if verbose:
            print(f"updating memory with value {mem_info} of {self.ps.name()}")
        mem = {}
        mem['uss'] = mem_info.uss
        mem['rss'] = mem_info.rss
        mem['vms'] = mem_info.vms
        mem['data'] = mem_info.data
        self.mem_usage.append(mem)


    def save_cpu_usage(self, filename: str, verbose=False, header=False) -> bool:
        try:
            if verbose:
                print(f'saving cpu usage for process {self.ps.pid}')
            with open(f'{filename}-CPU_PERCENT-{self.ps.pid}.txt','a') as f:
                if header:
                    f.write('cpu %\n')
                for i in range(len(self.cpu_usage)):
                    u = self.cpu_usage[i]
                    f.write(f'{u}\n')
            self.cpu_usage = []
            return True
        except:
            print(f'error saving cpu usage for pid: {self.ps.pid}',file=sys.stderr)
            return False

    def save_times(self, filename: str, verbose=False, header=True):
        with open(f'{filename}-TIMES-{self.ps.pid}.txt','w') as f:
            times=self.cpu_times
            if header:
                f.write('User\tSystem\tChildren User\tChildren System\tIO wait\n')
            f.write('{user}\t{system}\t{c_user}\t{c_system}\t{io}\n'.format(
                user=times.user, system=times.system, c_user=times.children_user,
                c_system=times.children_system, io=times.iowait)
            )
    
    def save_mem_usage(self, filename: str, verbose=False, header=False) -> bool:
        try:
            if verbose:
                print(f'saving memory usage for process {self.ps.pid}')
            
            with open(f'{filename}-{self.ps.pid}.txt','a') as f:
                if header:
                    f.write('uss\trss\tvms\tdata\n')
                for m in self.mem_usage:
                    f.write("{uss}\t{rss}\t{vms}\t{data}\n".format(
                        uss=m['uss'],rss=m['rss'],vms=m['vms'],data=m['data'])
                    )
            self.mem_usage = []
            return True
        except:
            print(f'error saving memory consumption for pid: {self.ps.pid}',file=sys.stderr)
            return False
    
    def __repr__(self):
        return "(pid={0}; name={1}; mem={2}; usage={3}".format(
            self.ps.pid, self.ps.name(), self.mem_usage, self.cpu_usage
        )

    def __str__(self):
        return self.__repr__()


class ProcessorMonitor:
    def __init__(self):
        self.m = []
    
    def __len__(self):
        return len(self.m)

    def insert_measure(self, m:list[psutil._pslinux.scputimes]):
        self.m.append(m)
    
    def save_measures(self, filename: str, verbose: bool = False, header: bool = False):
        if verbose:
            print(f'saving system cpu usage')
        ncpus = len(self.m[0])
        header_cpu = [header for _ in range(ncpus)]
        if len(self.m) > 0:
            print(self.m)
            for measure in self.m:
                for cpu_id in range(len(measure)):
                    with open(f'{filename}-SystemCPU-{cpu_id}.txt','a') as f:
                        if header_cpu[cpu_id]:
                            f.write('User\tNice\tSystem\tIdle\
                                    \tio wait\tHardware Interrupts (irq)\tSoftware Interrupts (softirq)\t\
                                    Steal by other OSs\tGuest\tGuest Nice\n')
                            header_cpu[cpu_id] = False
                        cpu_measure = measure[cpu_id]
                        f.write("{user}\t{nice}\t{system}\t{idle}\t{iowait}\t{irq}\t{softirq}\t{steal}\t{guest}\t{guest}\t{guest_nice}\n".format(
                            user=cpu_measure.user,nice=cpu_measure.nice,system=cpu_measure.system,idle=cpu_measure.idle,
                            iowait=cpu_measure.iowait,irq=cpu_measure.irq,softirq=cpu_measure.softirq,
                            steal=cpu_measure.steal,guest=cpu_measure.guest,guest_nice=cpu_measure.guest_nice)
                        )
            self.m = []
            return True
        else:
            self.m = []
            return False


#############       Main begins here      ##############

parser = argparse.ArgumentParser(description='Collect cpu usage and memory consumption of monitored program.\n\
                                 The cpu usage is collected by process (<cpu-output-prefix>-*-<pid>.txt) and by \
                                 processor(<cpu-output-prefix>-SystemCPU-<ProcessorID>.txt).\n\
                                 The memory consumption is collect by process (<memory-output-prexix>-<pid>.txt)')

parser.add_argument('monitored_name', type=str, default='a.out',
                    help='Process that the program will monitor cpu and memory consumption')
parser.add_argument('-c', '--cpu-output-prefix', dest='out_file_cpu', type=str, default='cpu-out',
                    help='output filename prefix to store cpu usage (each pid will have a file for it)')
parser.add_argument('-m', '--memory-output-prexix', dest='out_file_mem', type=str, default='memory-out',
                    help='output filename prefix to store memory consumption (each pid will have a file for it)')
parser.add_argument('-b', '--buffer-size', dest='buffer_size', type=int, default=20,
                    help='total of stored cpu/memory measures before wirte in output file (0 = unlimeted)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                    help='enable prints in stdout')
parser.add_argument('-p', '--per-cpu', dest='per_cpu', action='store_true', default=False,
                    help='store the cpu (total cpu usage) usage per cpu')
parser.add_argument('-i','--interval-time', dest='interval_time', type=float, default=0.5,
                    help='time between measures')

args=parser.parse_args()

monitored_name = args.monitored_name
out_file_cpu = args.out_file_cpu
out_file_mem = args.out_file_mem
buffer_size = args.buffer_size
verbose = args.verbose
interval_time = args.interval_time
per_cpu = args.per_cpu


if buffer_size <= 0:
    buffer_size = float('inf')

me = getpass.getuser()

if verbose:
    print(f'user:{me}')
    print(f'args:{args}')

# procs is a dict with pids as keys and DataProcess class 
# (declared here) as values
procs: dict[int, DataProcess] =  {}

# dict to store pid of running process
monitored_pids: dict[int, bool] = {}

#processor monitor
processor = ProcessorMonitor()

#wait until process start
if verbose:
    print(f'waiting for a process with name {monitored_name} starts...')

write_header = {}
proc_header = True



while monitored_pids == {}:
    sleep(interval_time)
    for p in psutil.process_iter():
        try:
            if p.name() == monitored_name:
                monitored_pids[p.pid] = True
                write_header[p.pid] = True
                procs[p.pid] = DataProcess(p)
        except:
            print(f'error in process {p.pid}', file=sys.stderr)
if verbose:
    print(f"Process {monitored_name} START!")

print(write_header)

while monitored_pids != {}:
    sleep(interval_time)
    measure = psutil.cpu_times_percent(percpu=per_cpu)
    if per_cpu == False:
        measure = [measure]
    processor.insert_measure(measure)
    if len(processor) > buffer_size:
        processor.save_measures(out_file_cpu,
                                verbose=verbose,
                                header=proc_header)
        proc_header = proc_header and False
        
    for p in psutil.process_iter():
        try:
            if p.name() == monitored_name:
                if not(p.pid in procs):
                    procs[p.pid] = DataProcess(p)
                    monitored_pids[p.pid] = True
                    write_header[p.pid] = True
                procs[p.pid].insert_cpu_usage(verbose=verbose)
                procs[p.pid].insert_mem_usage(verbose=verbose)
                if len(procs[p.pid].cpu_usage) > buffer_size:
                    print(write_header)
                    procs[p.pid].save_mem_usage(out_file_mem,
                                                verbose=verbose,
                                                header=write_header[p.pid])
                    procs[p.pid].save_cpu_usage(out_file_cpu,
                                                verbose=verbose,
                                                header=write_header[p.pid])
                    write_header[p.pid] = write_header[p.pid] and False
                    
        except:
            print(f'error in process {p.pid}', file=sys.stderr)
    pop_vals = []
    for p in monitored_pids:
        if not psutil.pid_exists(p):
            pop_vals.append(p)
    for p in pop_vals:
        monitored_pids.pop(p)

for p in procs:
    procs[p].save_cpu_usage(out_file_cpu,
                            verbose=verbose,
                            header=write_header[p])
    procs[p].save_mem_usage(out_file_mem,
                            verbose=verbose,
                            header=write_header[p])
    procs[p].save_times(out_file_cpu,
                        verbose=verbose)
processor.save_measures(out_file_cpu,
                        verbose=verbose,
                        header=proc_header)

