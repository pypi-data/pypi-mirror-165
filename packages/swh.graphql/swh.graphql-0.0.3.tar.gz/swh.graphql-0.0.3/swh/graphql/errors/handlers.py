# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


def format_error(error) -> dict:
    """
    Response error formatting
    """
    formatted = error.formatted
    formatted["message"] = "Unknown error"
    return formatted
