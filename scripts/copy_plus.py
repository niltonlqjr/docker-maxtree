import argparse
import glob
import os
import shutil
from pathlib import Path

program_name = 'copy_plus'

example_text=f'''
Copy files of a regexp and append to output filename one filed of regexp
Example:\n
    python3 {program_name}.py -o /home/user/files_test/ -d /home/user -a 1 test/*/files*.txt
    this will copy all files from /home/user/test/*/files*.txt to /home/user/files_test/.
    Given that append field is 1, so /home/user/test/my_dir1/files_user.txt
    will be stored as /home/user/files_test/files_user-my_dir1.txt'''

parser = argparse.ArgumentParser(prog=program_name,
                                 description=example_text,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('regular_expr', type=str,
                    help='regular expression to filenames (using base directory)')
parser.add_argument('--output-dir', '-o', default='.', type=str ,  dest='output_dir',
                     help='output directory')
parser.add_argument('--directory','-d', dest='directory', default='.',
                    help='base directory containing files')
parser.add_argument('--separator', '-s', type=str, dest='separator', default='/',
                    help='string that split fields')
parser.add_argument('--append-field', '-a', dest='append_field', default=-1, type=int,
                    help='field of reguular expression that will be appended to destiny file (separator determines the fields)')
parser.add_argument('--erase', '-e', dest='erease', nargs='*', type=str, default=[],
                    help='list of substrings that will be removed from final name')
parser.add_argument('--verbose', '-v', action='store_true', dest='verbose', 
                    help='print source and origin from each file')
args=parser.parse_args()

regular_expr = args.regular_expr
base_dir = Path(args.directory)
out_dir = Path(args.output_dir)
pos_append = args.append_field
sep = args.separator
erease = args.erease
verbose = args.verbose

str_base_dir=str(base_dir.resolve())
if pos_append >= 0:
    real_pos=len(str_base_dir.split(sep)) + pos_append
glob_str = os.path.join(str_base_dir,regular_expr)
files = glob.glob(glob_str)



for p in files:
    file_dir, file_name = os.path.split(p)
    if pos_append >= 0:
        append_string = '-'
        append_string += p.split(sep)[real_pos]
    else:
        append_string=''
        
    new_name, ext = os.path.splitext(file_name)
    new_name += f'{append_string}{ext}'
    for s in erease:
        new_name = new_name.replace(s,'')
    dest = os.path.join(out_dir,new_name)
    shutil.copy(p, dest)
    if verbose:
        print(f'copy from {p} to {dest}')