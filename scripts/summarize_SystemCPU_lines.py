import argparse
import glob
import utils
import math
import matplotlib.pyplot as plt
import numpy as np
    
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('directory',
                    help='directory containing files')
parser.add_argument('--regular-expr', '-r', type=str, dest='regular_expr', default='*-SystemCPU-*',
                    help='regular expression to filenames')
parser.add_argument('--output-figure', '-o', dest='out_name', default='cpu_usage_per_cpu.png',
                    help='figure name output')
parser.add_argument('--no-header', action='store_false', dest='header',
                    help='if file does not have the header in first line')
parser.add_argument('--column', '-c', dest='column', default=0, type=int,
                    help='column that will be plotted')

args=parser.parse_args()

directory = args.directory
regular_expr = args.regular_expr
header = args.header
fig_name = args.out_name
column = args.column


files = glob.glob(f'{directory}/{regular_expr}')


plt.rc('xtick', labelsize=7) 
plt.rc('ytick', labelsize=7) 

cpu_usage={}

col_type = [float for i in range(11)]

for fn in files:
    with open(fn) as f:
        file_str = f.read()
    ip = fn.split('@')[1].replace('.txt','')
    all_data = utils.text_table_to_data(file_str, colum_types=col_type, header=header)
    if not ip in cpu_usage:
        cpu_usage[ip] = len([d[column] for d in all_data])
    elif cpu_usage[ip] != len([d[column] for d in all_data]):
        raise Exception(f"different number of columns for ip:{ip}")
    
fig = plt.figure()
ax = fig.add_subplot()
for fn in cpu_usage:
    #print(fn, cpu_usage[fn])
    #print('=======================================')
    #names=[x.split('@')[1].replace('.txt','') for x in cpu_usage.keys()]
    names=list(cpu_usage.keys())
    ax.bar(names, cpu_usage.values())
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=30)
    int_max_val=int(math.ceil(max(cpu_usage.values())))
    ax.set_yticks(range(0,int_max_val+1,2))

#print(fig_name)
plt.savefig(f'{fig_name}', dpi=400)

#print("end")