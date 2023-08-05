# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from ..data import get_origins
from .utils import assert_missing_object, get_query_response


@pytest.mark.parametrize("origin", get_origins())
def test_get_visit(client, storage, origin):
    query_str = """
    {
      visit(originUrl: "%s", visitId: %s) {
        visitId
        date
        type
        latestStatus {
          status
          date
          type
          snapshot {
            swhid
          }
        }
        status {
          nodes {
            status
          }
        }
      }
    }
    """

    visits_and_statuses = storage.origin_visit_get_with_statuses(origin.url).results
    for vws in visits_and_statuses:
        visit = vws.visit
        statuses = vws.statuses
        data, _ = get_query_response(client, query_str % (origin.url, visit.visit))
        assert data["visit"] == {
            "visitId": visit.visit,
            "type": visit.type,
            "date": visit.date.isoformat(),
            "latestStatus": {
                "date": statuses[-1].date.isoformat(),
                "type": statuses[-1].type,
                "status": statuses[-1].status,
                "snapshot": ({"swhid": f"swh:1:snp:{statuses[-1].snapshot.hex()}"})
                if statuses[-1].snapshot
                else None,
            },
            "status": {"nodes": [{"status": status.status} for status in statuses]},
        }


def test_invalid_get_visit(client):
    query_str = """
    {
      visit(originUrl: "http://example.com/forge1", visitId: 3) {
        type
      }
    }
    """
    assert_missing_object(client, query_str, "visit")
