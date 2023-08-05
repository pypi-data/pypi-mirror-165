# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import json
from typing import Dict, Tuple


def get_response(client, query_str: str):
    return client.post("/", json={"query": query_str})


def get_query_response(client, query_str: str) -> Tuple[Dict, Dict]:
    response = get_response(client, query_str)
    assert response.status_code == 200, response.data
    result = json.loads(response.data)
    return result.get("data"), result.get("errors")


def assert_missing_object(client, query_str: str, obj_type: str) -> None:
    data, errors = get_query_response(client, query_str)
    assert data[obj_type] is None
    assert len(errors) == 1
    assert errors[0]["message"] == "Requested object is not available"


def get_error_response(client, query_str: str, error_code: int = 400) -> Dict:
    response = get_response(client, query_str)
    assert response.status_code == error_code
    return json.loads(response.data)["errors"]


def get_query_params_from_args(**args) -> str:
    # build a GraphQL query parameters string from arguments
    return ",".join([f"{key}: {val}" for (key, val) in args.items()])
