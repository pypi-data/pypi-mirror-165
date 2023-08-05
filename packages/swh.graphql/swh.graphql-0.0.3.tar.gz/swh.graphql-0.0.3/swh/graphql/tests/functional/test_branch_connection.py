# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from . import utils


def get_branches(client, swhid: str, first: int, **args) -> tuple:
    args["first"] = first
    params = utils.get_query_params_from_args(**args)
    query_str = """
    {
      snapshot(swhid: "%s") {
        branches(%s) {
          pageInfo {
            endCursor
          }
          edges {
            cursor
          }
          nodes {
            type
            name {
              text
            }
            target {
              __typename
              ...on Branch {
                name {
                  text
                }
              }
              ...on Revision {
                swhid
              }
              ...on Release {
                swhid
              }
              ...on Content {
                swhid
              }
              ...on Directory {
                swhid
              }
              ...on Snapshot {
                swhid
              }
            }
          }
        }
      }
    }
    """ % (
        swhid,
        params,
    )
    return utils.get_query_response(client, query_str)


def test_get_data(client):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    data, errors = get_branches(client, swhid, 10, types="[revision]")
    assert len(data["snapshot"]["branches"]["nodes"]) == 1
    # filter 'type' will return a single revision object and is used to assert data
    node = data["snapshot"]["branches"]["nodes"][0]
    assert node == {
        "name": {"text": "target/revision"},
        "target": {
            "__typename": "Revision",
            "swhid": "swh:1:rev:66c7c1cd9673275037140f2abff7b7b11fc9439c",
        },
        "type": "revision",
    }


def test_get_branches_with_alias(client):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    data, _ = get_branches(client, swhid, 10, types="[alias]")
    node = data["snapshot"]["branches"]["nodes"][0]
    assert node == {
        "name": {"text": "target/alias"},
        "target": {"__typename": "Branch", "name": {"text": "target/revision"}},
        "type": "alias",
    }


@pytest.mark.parametrize(
    "filter_type, count, target_type, swhid_pattern",
    [
        ("revision", 1, "Revision", "swh:1:rev"),
        ("release", 1, "Release", "swh:1:rel"),
        ("directory", 1, "Directory", "swh:1:dir"),
        ("content", 0, "Content", "swh:1:cnt"),
        ("snapshot", 1, "Snapshot", "swh:1:snp"),
    ],
)
def test_get_type_filter(client, filter_type, count, target_type, swhid_pattern):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    data, _ = get_branches(client, swhid, 10, types=f"[{filter_type}]")
    assert len(data["snapshot"]["branches"]["nodes"]) == count
    for node in data["snapshot"]["branches"]["nodes"]:
        assert node["target"]["__typename"] == target_type
        assert node["target"]["swhid"].startswith(swhid_pattern)


@pytest.mark.parametrize(
    "filter_types, count",
    [
        ("revision, release", 2),
        ("revision, snapshot, release", 3),
    ],
)
def test_get_type_filter_multiple(client, filter_types, count):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    data, _ = get_branches(client, swhid, 10, types=f"[{filter_types}]")
    assert len(data["snapshot"]["branches"]["nodes"]) == count


@pytest.mark.parametrize("name", ["rel", "rev", "non-exist"])
def test_get_name_include_filter(client, name):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    data, _ = get_branches(client, swhid, 10, nameInclude=f'"{name}"')
    for node in data["snapshot"]["branches"]["nodes"]:
        assert name in node["name"]["text"]


@pytest.mark.parametrize("count", [1, 2])
def test_get_first_arg(client, count):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    data, _ = get_branches(client, swhid, first=count)
    assert len(data["snapshot"]["branches"]["nodes"]) == count


def test_get_after_arg(client):
    swhid = "swh:1:snp:0e7f84ede9a254f2cd55649ad5240783f557e65f"
    first_data, _ = get_branches(client, swhid, first=1)
    end_cursor = first_data["snapshot"]["branches"]["pageInfo"]["endCursor"]
    node_name = first_data["snapshot"]["branches"]["nodes"][0]["name"]["text"]
    second_data, _ = get_branches(client, swhid, first=3, after=f'"{end_cursor}"')
    branches = second_data["snapshot"]["branches"]
    assert len(branches["nodes"]) == 3
    assert branches["edges"][0]["cursor"] == end_cursor
    for node in branches["nodes"]:
        assert node["name"]["text"] > node_name
