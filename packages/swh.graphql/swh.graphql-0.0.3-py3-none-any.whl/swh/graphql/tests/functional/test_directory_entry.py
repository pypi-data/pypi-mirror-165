# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from . import utils
from ..data import get_directories


@pytest.mark.parametrize("directory", get_directories())
def test_get_directory_entry_connection(client, directory):
    query_str = """
    {
      directory(swhid: "%s") {
        swhid
        entries {
          nodes {
            type
            name {
              text
            }
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % directory.swhid())
    directory_entries = data["directory"]["entries"]["nodes"]
    assert len(directory_entries) == len(directory.entries)
    output = [
        {"name": {"text": de.name.decode()}, "type": de.type}
        for de in directory.entries
    ]
    for each_entry in output:
        assert each_entry in directory_entries
