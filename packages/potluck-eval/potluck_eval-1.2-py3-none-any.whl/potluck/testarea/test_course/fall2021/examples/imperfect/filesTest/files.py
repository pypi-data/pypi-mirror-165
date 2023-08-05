"""
Imperfect code for files.py.
"""


def listFile(filename):
    """
    Prints out the contents of a file, with line numbers at the start of
    each line.
    """
    with open(filename, 'r') as fin:
        # Numbers lines incorrectly
        ln = 0
        for line in fin:
            print(ln, line, end='') # line has a newline at the end
            ln += 1


def grep(filename, fragment, writeTo):
    """
    Finds just lines of the file which contain the given fragment, and
    writes them into the writeTo file.
    """
    with open(filename, 'r') as fin:
        # Tries to write back into the source file: a major error!
        with open(filename, 'w') as fout:
            for line in fin:
                if fragment in line:
                    fout.write(line)


def readNums(filename):
    """
    Given a filename, reads a list of floating-point numbers from the
    file, one per line, skipping lines that cannot be interpreted as
    numbers.
    """
    result = []
    with open(filename, 'r') as fin:
        for line in fin:
            # ERROR: no try/except
            result.append(float(line.strip()))

    return result


def addRecords(filename, records):
    """
    Given a filename and a list of strings, adds one line to the file
    for each string, consisting of just that string plus a newline. If
    called multiple times, the file will grow longer each time.
    """
    # Writes instead of appending
    with open(filename, 'w') as fout:
        for record in records:
            fout.write(record) # doesn't add newlines
