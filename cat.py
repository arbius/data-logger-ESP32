def cat(fname):
    import sys
    with open(fname, 'r') as f:
        contents = f.read()

    print(contents)

