import numpy as np
import nrrd
import argparse


def read_raw(file, x, y, z):
    # TODO: Let user supply bit-type and switch here accordingly?!
    data = np.fromfile(file, dtype=np.ubyte)
    data = data.reshape((x, y, z), order='F')

    return data


def make_binary(data, x, y, z):
    # TODO: This task is ideal for a multi thread operation!
    # As we return only two labels, ubyte should be enough... might even be reduced
    binary_data = np.zeros([x, y, z], dtype=np.ubyte)

    # Iterate through array values; if 0 => do nothing (output array contains 0s), if != 0 => write 1
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if data[i, j, k] != 0:
                    binary_data[i, j, k] = np.ubyte(1)

    return binary_data


def make_header(x, y, z):
    header = {'dimension': 3, 'sizes': [x, y, z]}
    # TODO: The values defined here are added automatically anyways. The header is also optional for writing,
    #  as a minimal one is added automatically. This part here is still kept for extension in the future.
    #  See below for possible values.
    # dict => see https://docs.python.org/3/library/stdtypes.html#dict
    # header = {'kinds': ['domain', 'domain', 'domain'], 'units': ['mm', 'mm', 'mm'],
    # 'spacings': [1.0458, 1.0458, 2.5], 'space': 'right-anterior-superior',
    # 'space directions': np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    # 'encoding': 'ASCII'}

    return header


def write_nrrd(data, header, filename):
    # If the provided filename has no file extension, we add it here
    if filename[-5:] != '.nrrd':
        filename = str(filename) + '.nrrd'

    print('Writing output to ' + filename)

    # write our array into a .nrrd file
    nrrd.write(filename, data, header)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a raw volume image to a .nrrd file')
    parser.add_argument('input_file', action='store', type=str, help='Raw file to convert')
    parser.add_argument('x', action='store', type=int, help='x dimension size')
    parser.add_argument('y', action='store', type=int, help='y dimension size')
    parser.add_argument('z', action='store', type=int, help='z dimension size')
    parser.add_argument('-b', '--binary', dest='binary', action='store_true', required=False,
                        help='Return a binary image; every value != 0 in the input file will be returned as 1')
    parser.add_argument('-o', '--output_file', action='store', type=str, help='Output filename')
    # TODO: Add optional arguments to fill header data: Voxel spacing, units, offset, etc.
    parser.set_defaults(binary=False)

    args = parser.parse_args()

    input_file = args.input_file
    x_dim = args.x
    y_dim = args.y
    z_dim = args.z
    binary = args.binary
    output_file = args.output_file

    print('Reading raw data')
    raw_data = read_raw(input_file, x_dim, y_dim, z_dim)

    print('Creating .nrrd header')
    file_header = make_header(x_dim, y_dim, z_dim)

    if binary:
        print('Converting to binary image')
        raw_data = make_binary(raw_data, x_dim, y_dim, z_dim)

    if output_file == '':
        output_file = 'conversion'

    print('Writing .nrrd file')
    write_nrrd(raw_data, file_header, output_file)
