# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql import server


class Search:
    def __init__(self):
        self.search = server.get_search()

    def get_origins(self, query: str, after=None, first=50):
        return self.search.origin_search(
            url_pattern=query,
            page_token=after,
            limit=first,
        )
