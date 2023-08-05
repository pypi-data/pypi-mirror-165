# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


class ObjectNotFoundError(Exception):
    """ """


class PaginationError(Exception):
    """ """

    msg: str = "Pagination error"

    def __init__(self, message, errors=None):
        # FIXME, log this error
        super().__init__(f"{self.msg}: {message}")
