#!/usr/bin/env python3
# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2022 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import sys

from es7s.app import Es7sEntrypointApp


def main():
    (Es7sEntrypointApp()).run(sys.argv)


if __name__ == '__main__':
    main()
