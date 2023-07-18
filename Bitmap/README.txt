Assignment: HW4

Import the file as a module and call the functions as desired.

Program Interface:

create_index(input_file, output_path, sorted)

Where: ‘input_file’ is a file that you will use to create the bitmap index. ‘output_path’ is the destination directory for your output bitmap file. It must be a regular file with no suffixes(.txt, .c, etc). ‘sorted’ is a boolean value that specifies whether your data will be sorted.

compress_index(bitmap_index, output_path, compression_method, word_size)

Where: ‘bitmap_index’ is the input file that will be used in the compression. ‘output_path’
is the path to a directory where the compressed version will be written using the naming scheme
specified above. ‘compression_method’ is a String specifying which bitmap compression method you will be using (WAH, BBC, PLWAH, etc). ‘word_size’ is an integer specifying the word size to be used.
