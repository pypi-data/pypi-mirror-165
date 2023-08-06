import io
import os
import re
import sys
from npdoc_to_md import render_obj_docstring


PATTERN = r'^```\s*{(?P<directive>[. a-zA-Z0-9_]+)}\s*\n(?P<code>.*?)\n```\s*$'


def parse_text(md_in: str, debug=False) -> str:
    '''Accepts a `str` containing Markdown text, then finds the tagged code blocks
    in the markdown, executes these code blocks and captures the output, which is
    then embedded into the output markdown.

    Parameters
    ----------
    md_in: str
        The input Markdown text string
    debug: bool
        default: False, if True outputs mathing tagged code blocks

    Returns
    -------
    str
        The compiled markdown string
    '''
    md_out = md_in
    workspace = {}
    output = ""
    offset = 0  # Tracks growth of input_string resulting from inserting code output

    # Scan input looking for tagged code blocks
    matches = re.finditer(PATTERN, md_in, re.MULTILINE | re.DOTALL)

    for match in matches:
        if debug:
            print(f"{match.group('directive')} found at {match.start()}")

        directive = match.group('directive').split()
        # Only process code blocks with capture or replace directives
        if 'capture' not in directive and 'replace' not in directive:
            continue

        start = match.start() + offset
        end = match.end() + offset

        # Execute the code block, and capture all the output that was generated
        if 'exception' in directive:
            try:
                exec(match.group('code'), workspace)
            except Exception as e:
                output = str(e)
            else:
                raise ValueError(f'Error - an expected Exception did not occur: {e}')
        else:
            # Execute and capture output
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            exec(match.group('code'), workspace)
            sys.stdout = sys.__stdout__
            output = output_buffer.getvalue()

        if 'replace' in directive:
            output = f"```\n{output}\n```"
            md_out = md_out[:start] + output + md_out[end:]
            offset = offset + len(output) - end + start

        if 'capture' in directive:
            insert = f'\n__Output:__\n\n```\n{output.strip()}\n```\n'
            md_out = md_out[:end] + insert + md_out[end:]
            offset += len(insert)

    return md_out


def parse_file(src: str, dest: str, debug=False):
    '''Takes a markdown file as input, executes any code blocks contained within,
    captures the output and write the result to a new file.

    src: str
        The full path to the input file
    dest: str
        The full path for the output file
    '''
    if not os.path.isfile(src):
        raise ValueError(f"Error: {src} is not a file or does not exist!")

    md_text = ''
    with open(src, 'r') as fh_in:
        md_text = fh_in.read()
        if debug:
            print(f'Processing file: {src}')
        fh_in.close()

    out_text = parse_text(md_in=md_text, debug=debug)

    if dest is not None:
        if os.path.isfile(dest):
            raise ValueError(
                f"Error: {dest} file already exist! Use the --force (-f) flag to force overwriting existing files.")

    with open(dest, 'w') as fh_out:
        if debug:
            print(f'Writing file: {dest}')
        fh_out.write(out_text)
        fh_out.close()

    if debug:
        print('Processing complete')


# In Pycharm press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_file('../doc_src/readme_template.md', '../demo-out.md')
