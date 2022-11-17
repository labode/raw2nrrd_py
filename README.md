# RAW to Nrrd converter
This program converts a .raw volume image file to a Nearly Raw Raster Data (.nrrd) file.
Advantages of .nrrd:
- Header with image information allows for easier import into other programs
- File compression is employed and will possibly lead to a much smaller file size than the initial .raw file had

The program was written to convert .raw segmentation images of CT-scans for further processing.

## Requirements
Required packages are listed in requirements.txt and can be installed using pip as follows:\
`pip3 install -r requirements.txt`

## Limitations
- At the current time the input is limited to three-dimensional 8-bit .raw images.
- Only a minimal header is created, containing only type, dimension and sizes.
- Program operation is single thread only. This leads to long run times for the binary conversion.
- Only one foreground label is supported in the  conversion.

These limitations might be addressed in future versions of the program.

## How to use this program?
Only two parameters are required to run this program.
A user must specify the .raw input file, as well as the x, y and z dimensions of the volume image. Example:

`python3 raw2nrrd.py myfile.raw 1500 1500 1500`

Optional parameters are the path of an output file (-o option). E.g. `python3 raw2nrrd.py myfile.raw 1500 1500 1500 -o path/to/my_file.nrrd` 

You can also add the -b (--binary) flag. This will replace every image value != 0 with 1 to turn the image into a segmentation image, consisting of a background label (0), and a foreground label (1). It can e.g. be imported into itksnap.

