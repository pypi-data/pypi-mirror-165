# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import sys

# from toybox import boxfile, dependency, exceptions, git, toybox, version

from toybox.toybox import Toybox
from toybox.exceptions import ArgumentError


def main():
    try:
        # -- Remove the first argument (which is the script filename)
        Toybox(sys.argv[1:]).main()
    except ArgumentError as e:
        print(str(e) + '\n')
        Toybox.printUsage()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Execution interrupted by user.')
        pass


if __name__ == '__main__':
    main()
