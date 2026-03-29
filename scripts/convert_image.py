import PIL.Image
import PIL.ImageFile
import skimage
import argparse
import os
import PIL
parser = argparse.ArgumentParser(description='Convert images using skimage library',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('file', type=str, help='input filename')
parser.add_argument('-f', '--format', dest='format', default='png', help='output format')
parser.add_argument('--unlimited-size', action='store_true', dest='unlimited_size', help='set flag to unlimited size')
parser.add_argument('--load-truncate', action='store_true', dest='load_truncate', help='enable load truncate images')
args=parser.parse_args()

in_file = args.file
prefix, in_fmt = os.path.splitext(in_file)
out_fmt = args.format

if args.unlimited_size:
    PIL.Image.MAX_IMAGE_PIXELS = None

if args.load_truncate:
    PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True


im = skimage.io.imread(in_file)
try:
    skimage.io.imsave(f'{prefix}.{out_fmt}',im)
except Exception as e:
    print(f'Impossible to save file{prefix}.{out_fmt}')
    print('Exception generated:')
    print(e)
    