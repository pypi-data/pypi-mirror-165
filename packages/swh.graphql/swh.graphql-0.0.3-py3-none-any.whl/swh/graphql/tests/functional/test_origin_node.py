# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from ..data import get_origins
from .utils import assert_missing_object, get_query_response


def test_invalid_get(client):
    query_str = """
    {
      origin(url: "http://example.com/non-existing") {
        url
      }
    }
    """
    assert_missing_object(client, query_str, "origin")


@pytest.mark.parametrize("origin", get_origins())
def test_get(client, storage, origin):
    query_str = (
        """
    {
      origin(url: "%s") {
        url
        id
        visits(first: 10) {
          nodes {
            id
          }
        }
        latestVisit {
          visitId
        }
        snapshots(first: 2) {
          nodes {
            id
          }
        }
      }
    }
    """
        % origin.url
    )

    response, _ = get_query_response(client, query_str)
    data_origin = response["origin"]
    storage_origin = storage.origin_get([origin.url])[0]
    visits_and_statuses = storage.origin_visit_get_with_statuses(origin.url).results
    assert data_origin["url"] == storage_origin.url
    assert data_origin["id"] == storage_origin.id.hex()
    assert len(data_origin["visits"]["nodes"]) == len(visits_and_statuses)
    assert data_origin["latestVisit"]["visitId"] == visits_and_statuses[-1].visit.visit
    snapshots = storage.origin_snapshot_get_all(origin.url)
    assert len(data_origin["snapshots"]["nodes"]) == len(snapshots)
