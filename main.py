# import argparse

from file_renamer import FileRenamer

# TODO: 1. add CLI command 
# parser = argparse.ArgumentParser(prog="Humble Bundle Ebook Renamer", description="blablabla")
# parser.add_argument('-r', '--reference', type=str, required=True, help="Reference file path")
# args = parser.parse_args()
# aa = args.reference

# TODO: 2. Integration with GUI

# path of file that contains list of corrected ebook titles
REFERENCE_PATH = ''

# path of directory that contains list of ebooks that have not been renamed
FILE_PATH = ''


fr = FileRenamer(reference_path=REFERENCE_PATH, file_path=FILE_PATH)
