import common_util
import os.path

READ_TXT_FILE = 'ch05_data/sample.txt'
WRITE_TXT_FILE = 'ch05_data/sample_write.txt'
READ_BIN_FILE = 'ch05_data/sample.bin'
WRITE_BIN_FILE = 'ch05_data/sample_write.bin'


# ====================================================
# 0501 read / write text data
#      python has text mode in IO
#       - 'rt' or 'wt' for text read or write
# ----------------------------------------------------
def test_0501():
    # read text file
    #  - open w/ 'rt' option -> get all contents as str object
    with open(READ_TXT_FILE, 'rt') as f:
        # use read function
        data = f.read()
        print(data)
        print(type(data))  # type is str

    #  - iterate over the lines
    with open(READ_TXT_FILE, 'rt') as f:
        # iterate w/ for in
        for line in f:
            print(line)

    # write text file
    #  - use 'wt' to write
    #  - use 'at' to append
    with open(WRITE_TXT_FILE, 'wt') as f:
        f.write('aaa\n')
        f.write('bbb\n')
        f.write('ccc\n')


# ====================================================
# 0503 using separator in print()
#      easy way to join data
# ----------------------------------------------------
def doctest_0503():
    """
    >>> rows = ('ACME', 50, 91.5)
    >>> print(*rows, sep=',')
    ACME,50,91.5

    # join can be applied only on str
    >>> print(','.join(rows))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: sequence item 1: expected str instance, int found
    """


# ====================================================
# 0504 read / write binary data
# ----------------------------------------------------
def doctest_0504():
    """
    # test binary data
    >>> b = b'Hellow World'
    >>> b[0]
    72
    >>> for c in b:
    ...     print(c)
    ...
    72
    101
    108
    108
    111
    """


def test_0504():
    # read binary file
    with open(READ_BIN_FILE, 'rb') as f:
        data = f.read()
        print(type(data))  # it shows <class 'bytes'>
        print(data)

    # write binary file
    with open(WRITE_BIN_FILE, 'wb') as f:
        f.write(b'Hello World')


# ====================================================
# 0509 read binary data into buffer
# ----------------------------------------------------
def test_0509():
    buf = bytearray(os.path.getsize(READ_BIN_FILE))
    with open(READ_BIN_FILE, 'rb') as f:
        # use readinto() to fill existing buffer with data
        f.readinto(buf)
    print(type(buf))
    print(buf)

    # simple pattern to read bin file to buffer
    buf_size = 32
    buf = bytearray(buf_size)
    with open(READ_BIN_FILE, 'rb') as f:
        while True:
            n = f.readinto(buf)
            if n < buf_size:
                break
            # use the contents of buf
            # ...


if __name__ == '__main__':
    common_util.call_funcs(vars(), lambda s: s.startswith('test_'))
