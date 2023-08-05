# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from . import utils


def test_search_origins(client):
    query_str = """
    {
      search(query: "fox", first: 1) {
        nodes {
          type
          target {
            ...on Origin {
              url
              latestVisit {
                date
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str)
    assert len(data["search"]["nodes"]) == 1
    assert data == {
        "search": {
            "nodes": [
                {
                    "target": {
                        "url": "https://somewhere.org/den/fox",
                        "latestVisit": {"date": "2018-11-27T17:20:39+00:00"},
                    },
                    "type": "origin",
                }
            ],
            "pageInfo": {"endCursor": "MQ==", "hasNextPage": True},
        }
    }


def test_search_missing_url(client):
    query_str = """
    {
      search(query: "missing-fox", first: 1) {
        nodes {
          type
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str)
    assert len(data["search"]["nodes"]) == 0
