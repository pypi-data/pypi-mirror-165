# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

class ArgumentError(Exception):
    """Error caused when command line arguments have something wrong in them."""
    pass


class DependencyError(Exception):
    """Error caused when a dependency cannot be resolved."""
    pass
