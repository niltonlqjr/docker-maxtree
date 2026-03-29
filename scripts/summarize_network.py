#string format
s_test= \
'''
pid	name	data sent	data recv
0	b'unknown TCP'	0	0
0	b'10.30.1.3:49792-10.30.6.42:1034'	2380	2380
0	b'10.30.1.3:43000-10.30.6.42:1033'	2196	2196
0	b'10.30.1.3:59604-10.30.9.6:1026'	808	808
0	b'10.30.1.3:42934-10.30.12.22:1031'	970	70
0	b'10.30.1.3:58740-10.30.6.42:1035'	2380	2380
0	b'10.30.1.3:47146-10.30.6.42:1038'	2196	2196
0	b'10.30.1.3:35134-10.30.1.15:1027'	723194	723194
0	b'10.30.1.3:48710-10.30.1.26:1024'	808	808
0	b'10.30.1.3:60346-10.30.1.15:1034'	306	306
0	b'10.30.1.3:34138-10.30.1.15:1033'	306	306
'''


import utils
import re
import argparse
import glob
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

def increase(transfer, source, dest, sent):
    if not source in transfer:
        transfer[source] = {}
    if not dest in transfer[source]:
        transfer[source][dest] = 0
    transfer[source][dest] += sent
    
def get_ips(str):
    regexp='\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips = re.findall(regexp, str)
    return ips



parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('directory',
                    help='directory containing files')
parser.add_argument('--regular-expr', '-r', type=str, dest='regular_expr', default='network*.txt',
                    help='regular expression to filenames')
parser.add_argument('--output-figure-prefix', '-o', dest='out_name', default='network_',
                    help='output figure prefix')
parser.add_argument('--output-type', '-t', dest='output_type', default='png',
                    help='output figure type')
parser.add_argument('--no-header', action='store_false', dest='header',
                    help='if file does not have the header in first line')


args=parser.parse_args()

directory = args.directory
regular_expr = args.regular_expr
header = args.header
fig_prefix = args.out_name
out_type = args.output_type

transfer_to={}
transfer_from={}



files = glob.glob(f'{directory}/{regular_expr}')

for fn in files:
    transfer_to[fn]={}
    transfer_from[fn]={}
    with open(fn) as f:
        s_file = f.read()

    x=utils.text_table_to_data(s_file,[int,str,int,int],header=header,field_sep='\t')
    for l in x:
        if len(l) == 4:
            ips = get_ips(l[1])
            if len(ips) == 2:
                source=ips[0]
                dest=ips[1]
                sent = l[2]
                recv = l[3]
                increase(transfer_to[fn],source,dest,sent)
                increase(transfer_from[fn],source,dest,recv)
            else:
                print(f"invalid ip {l[1]}")
        else:
            print(f"invalid line:{l}")

    k = list(transfer_to[fn].keys())
    max_transfer = transfer_to[fn][k[0]]

    print(f'to:{transfer_to[fn]}')
    print(f'from:{transfer_from[fn]}')

bar_width=0.25
for fn in files:
    data_plot_bar1 = []
    data_plot_label1 = [None]
    data_plot_bar2 = []
    data_plot_label2 =[None]
    for ip in transfer_to[fn]:
        for pair_ip in transfer_to[fn][ip]:
            data_plot_label1.append(pair_ip)
            data_plot_bar1.append(transfer_to[fn][ip][pair_ip])


    for ip in transfer_from[fn]:
        for pair_ip in transfer_from[fn][ip]:
            data_plot_bar2.append(transfer_from[fn][ip][pair_ip])
            data_plot_label2.append(pair_ip)
    
    x1=np.arange(len(data_plot_bar1))
    x2=np.arange(len(data_plot_bar2))
    


    fig = plt.figure()
    

    file_path = Path(fn)

    file_stem=file_path.stem

    ax = fig.add_subplot()
    ax.bar(x1+bar_width, data_plot_bar1, bar_width, label='sent bytes')   
    ax.bar(x2-bar_width, data_plot_bar2, bar_width, label='recv bytes')
    ax.set_xlabel('data transfer')
    ax.tick_params(labelrotation=45)
    print(data_plot_label1,data_plot_bar1)
    ax.set_xticklabels(data_plot_label1)
    ax.legend()
    fig_name=f'{file_stem}-{ip}.{out_type}'
    print(fig_name)

    plt.savefig(f'{fig_name}',dpi=200)
    