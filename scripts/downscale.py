import skimage as sk
import numpy as np
import os
import argparse
import imageio.v3 as iio
import imageio_freeimage


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('filename', type = str, help='input file')
parser.add_argument('--factor', '-f', dest='downsample_factor', default='2,2', type=str,
                    help='downsample scale using comma as separator')
parser.add_argument('--output-file', '-o', dest='output_file', default='ds.jpg',type=str,
                    help='ouput filename with extension')
parser.add_argument('--verbose', dest='verbose', action='store_true')
parser.add_argument('--library', '-l', dest='library', default='skimage',
                    help='library to read image [skimage(default) | imageio]\n imageio uses freeimage')
args=parser.parse_args()

filename = args.filename
dsf_str = args.downsample_factor
out_name = args.output_file
lib = args.library
verbose = args.verbose

in_prefix, ext = os.path.splitext(filename)

factor_lst = list(int(x) for x in dsf_str.split(','))

if lib == 'skimage':
    im = sk.io.imread(filename)
elif lib == 'imageio':
    im = iio.imread(filename,plugin='JP2-FI')
else:
    print("invalid plugin")
    exit()

factor = list(1 for i in range(len(im.shape)))
min_shape = min(len(factor_lst),len(factor))
for i in range(min_shape):
    factor[i] = factor_lst[i]

factor=tuple(factor)    

if verbose:
    print(factor)
    print(im.shape)

ds = sk.transform.downscale_local_mean(im,factor)

if verbose:
    print('downscale from {0} to {1}'.format(im.shape,ds.shape))

ds = np.round(ds)
ds = ds.astype(np.uint8)

if lib == 'skimage':
    sk.io.imsave(out_name,ds)
elif lib == 'imageio':
    iio.imwrite(out_name,ds,plugin='JP2-FI')