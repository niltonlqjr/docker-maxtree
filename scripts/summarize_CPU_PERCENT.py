import argparse
import glob
import utils
import os
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('directory',
                    help='directory containing files')
parser.add_argument('--regular-expr', '-r', type=str, dest='regular_expr', default='*-CPU_PERCENT-*',
                    help='regular expression to filenames')
parser.add_argument('--no-header', action='store_false', dest='header',
                    help='if file does not have the header in first line')
parser.add_argument('--output-figure', '-o', dest='out_name', default='cpu_usage_per_process.png',
                    help='figure name output')

args=parser.parse_args()

directory = args.directory
regular_expr = args.regular_expr
header = args.header
fig_name = args.out_name


glob_str = os.path.join(directory, regular_expr)
files = glob.glob(glob_str)

cpu_usage={}

for fn in files:
    with open(fn) as f:
        file_str = f.read()
    all_data = utils.text_table_to_data(file_str, colum_types=[float], header=header)
    cpu_usage[fn] = [d[0] for d in all_data]

i=0

for fn in cpu_usage:
    print(fn, cpu_usage[fn], len(cpu_usage[fn]))
    print('=======================================')
    plt.plot(cpu_usage[fn],label=fn)
    

print(fig_name)
plt.savefig(f'{fig_name}',dpi=200)
