#!/usr/bin/env python3

from readme_executor._app import main

#!/usr/bin/env python3

import argparse
import sys
import os

from readme_executor import parse_file, parse_text


def main():
    usage_msg = 'Examples:\n'\
              '----------------\n'\
              '\tmain.py                                                    # Input taken from stdin, output is stdout\n'\
              '\tmain.py -i doc_src/readme.md                               # Input file specified, output will be stdout\n'\
              '\tmain.py -i doc_src/classes.md -o docs/classes_doc.md       # Input and Output filename specified in command\n'\
              '\tmain.py -i doc_src/contrib.md -o docs/contributing.md -d   # Display all matched code blocks for '\
              'debugging\n' \
              '\tmain.py -i doc_src/contrib.md -o docs/contributing.md -f   # Force existing output file to be overwritten.\n\n'

    no_input_file_msg = '\nError: You must specify an input file and optionally an output\n'\
                    'file. If no output file is supplied, the input filename will\n'\
                    'be used with "_out" appended to the filename.\n\n'

    parser = argparse.ArgumentParser(usage=usage_msg, prog="main.py")

    parser.add_argument("-i", "--infile", help="The source markdown document", type=str, required=False)
    parser.add_argument("-o", "--outfile", help="The markdown file to be generated", type=str, required=False)
    parser.add_argument("-d", "--debug", help="Outputs the tagged code blocks found by the parser\n"
                                        "This is helpful for debugging when results are not as expected",
                        action="store_true", required=False)
    parser.add_argument("-f", "--force", help="Force output to overwrite existing file", action="store_true",
                        required=False)
    args = parser.parse_args()

    # If input file specified...
    in_text = ''
    if args.infile:
        try:
            with open(args.infile, 'r') as fhi:
                in_text = fhi.read()
                fhi.close()
        except FileNotFoundError:
            print(f'Error: {args.infile} does not exist!')
            sys.exit(-1)
    else:
        # Else read from standard input
        for line in sys.stdin:
            in_text += line

    verbose = False
    if args.debug:
        verbose = True

    out_text = parse_text(in_text, debug=verbose)

    # If no output file specified ...
    if args.outfile is not None:
        if os.path.isfile(args.outfile) and not args.force:
            raise ValueError(f"Error: {args.outfile} file already exist! Use -f to force overwriting an existing file")

        with open(args.outfile, 'w') as fho:
            fho.write(out_text)
            fho.close()
    else:
        print(out_text)




if __name__ == '__main__':
    main()
