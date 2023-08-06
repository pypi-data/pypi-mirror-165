#!/usr/bin/env python3
from gendiff import diff, cli


def main():
    args = cli.run()
    diff.start(args)


if '__name__' == '__main__':
    main()
