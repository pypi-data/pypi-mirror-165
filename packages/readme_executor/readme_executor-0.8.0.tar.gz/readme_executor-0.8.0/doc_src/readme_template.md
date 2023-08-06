# README EXECUTOR

A tool for executing Python code blocks in Markdown documentation.

Copyright 2022 Randall Morgan

## Introduction

This script reads Markdown documents, locating tagged Python code blocks, 
executing them, and capturing their output. The output from the code block 
is then inserted into a generated Markdown document.

This script was developed to help ensure that code samples in Python project 
documentation actually reflected the current version of the software.
Running this script as part of the CI/CD process will help you keep your docs 
current with the latest software version. Note that this script does not parse 
Python code to generate Markdown documentation. There are many good tools for 
that already. The focus of this tool is solely to aid in maintaining code 
samples in that documentation.

## Usage

This script is ran on an existing Markdown document template. The template is 
a regular Markdown document containing specially tagged code blocks as described 
below. In fact, this script was used to generate this readme you are reading now.
It was generated using the Markdown template file /doc_src/readme_template.md
found in the doc_src folder of this project. It is recommended that you read the
template file as well as this document to gain a full understanding before creating
your own Markdown template files for your projects.

Since this document includes textual code snippets and actual tagged code blocks. 
I have denoted the textual code snippets with __Rendered__ and the tagged code 
blocks that are parsed and executed with __Code__. This will aid in grokking the 
Markdown template and demonstrates how the code blocks are displayed in the final
document.

### Running the script:
If this script is invoked without specifying an input file, input will be taken from
standard input (stdin). If an output file is not specified, output will be sent to
standard out (stdout). A debug flag (-d) may be passed on the command line. When 
provided, the script displays the code blocks it found and parsed. A force-overwrite
flag (-f) can also be specified and will cause the script to overwrite an existing
output file.

#### Command-Line Options:

``` { .python replace }
import sys
import subprocess
p = subprocess.run([sys.executable, 'readme_executor.py', '--help'],
                    capture_output=True, text=True)
print(p.stdout)
```
#### Example Invocations
```
$ readme_executor.py                                                            # input will be taken from stdin, and output sent to stdout
$ readme_executor.py -i ./doc_src/readme_template.md                            # input file specified, output sent to stdout
$ readme_executor.py -i ./doc_src/readme_template.md -o ./docs/readme.md        # input and output files specified
$ readme_executor.py -i ./doc_src/readme_template.md -o ./docs/readme.md -d     # debug output
$ readme_executor.py -i ./doc_src/readme_template.md -o ./docs/readme.md -f     # force the script to overwrite an existing output file
 
```

## Tagging Code Blocks

### Non-Tagged Code blocks
Non-tagged code blocks like this are not processed:

```
print('Leave this alone')
```

### Tagged Code Blocks

Code blocks containing directives will be processed. A directive is made up of three parts: 

    * The delimiters: { and }.
    * The language indicator: .python 
    * The directive: capture, replace, exception

Putting this all together a typical tagged code block would look like:

```
''' { .python capture }

import math

x, y = 47, 96

print(f'Coords: {math.sin(x)}, {math.cos(y)}') 

'''
```

*Note that while triple single-quotes are shown here, triple back-ticks are required in the markdown file.*
*Note that currently Python is the only programming language supported. But this may change in the future.*
### Capture

The `capture` directive indicates that the standard output should be captured and inserted as a new code block below the code.

__Rendered__
```

''' { .python capture }
print('This output should be captured!')
print('This too')
'''

```

__Code__
``` { .python capture }
print('This output should be captured!')
print('This too')
```

### Replace
The `replace` directive indicates that the code should be replaced by the output.

This code...

__Rendered__:
```
''' { .python replace } 
print('A replace cell')
'''
```

Gets replaced with:
__Code__
``` { .python replace }
print('A replace cell')
```

### Exception
The `exception` directive indicates that the code should raise an `Exception`. 
The traceback is then inserted instead of the standard output.
The `exception` directive is used with the `capture` and `replace` directives.

__Rendered__
``` 
''' { .python capture exception }
# A cell that should raise a ValueError
int('x')
'''
```
__Code__
``` { .python capture exception }
# A cell that should raise a ValueError
int('x')
```

## API

If you wish to use readme_executor as a module in your own 
document processor, the following text will help.

``` { .python replace }
from readme_executor import parse_text, parse_file
from npdoc_to_md import render_obj_docstring

print(render_obj_docstring(obj='readme_executor.parse_text', alias='parse_text'))
print(render_obj_docstring(obj='readme_executor.parse_file', alias='parse_file'))
```

## License
This software is licensed under the GNU General Public License 
version 2 or later. At the user's discretion. You are free to
use this script, and it's source code any way you like. 

## Waranty
This software is provided without warranty of any kind! The user is 
solely responsibility to determine the suitability of this software 
for their own specific use case.
