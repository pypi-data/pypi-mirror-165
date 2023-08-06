"""Command-line interface"""

import re, sys

from .colorls import cols_format


LINE_REGEX = re.compile(r"\s*\S+")


def main(args):
    """Called indirectly from a `c*ls` script.  Colorise the input as required.

    Parameters: $size_column $inums $ownership_cols [ $human ]"""

    size_column = int(args[1]) - 1
    inums_on = args[2] == "y"
    ownership_cols = int(args[3])
    if inums_on:
        dir_column = 1
    else:
        dir_column = 0
    try:
        human = args[4] == "y"
    except IndexError:
        human = False

    ## print(len(args))
    for line in sys.stdin:
        cols = LINE_REGEX.findall(line)
        # TO-DO: better heuristics
        if line and line[-1] != ":" and len(cols) >= size_column + 3:
            print(cols_format(cols, ownership_cols, size_column, dir_column))
        else:
            # Pass dir header lines and block counts through unchanged
            print(line, end='')
    return 0


# *** MAINLINE ***
if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except (BrokenPipeError, IOError):
        # Avoid "Exception ignored ..." and "BrokenPipeError: [Errno 32]..."
        # messages from the Python interpreter
        sys.stderr.close()
