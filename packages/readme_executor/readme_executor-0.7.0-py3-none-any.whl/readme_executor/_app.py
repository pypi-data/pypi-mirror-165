from readme_executor import parse_file


def app(infile: str, outfile: str = None, verbose: bool = False):
    parse_file(src=infile, dest=outfile, debug=verbose)


if __name__ == '__main__':
    infile = '../readme_template.md'
    app(infile=infile)
