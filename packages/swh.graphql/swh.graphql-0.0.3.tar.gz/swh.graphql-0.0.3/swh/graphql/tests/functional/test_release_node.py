# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import base64

import pytest

from . import utils
from ..data import get_releases


@pytest.mark.parametrize("release", get_releases())
def test_get_release(client, release):
    query_str = (
        """
    {
      release(swhid: "%s") {
        swhid
        name {
          text
          base64
        }
        message {
          text
        }
        author {
          email {
            text
          }
          name {
            text
          }
          fullname {
            text
          }
        }
        date
        targetType
      }
    }
    """
        % release.swhid()
    )
    data, _ = utils.get_query_response(client, query_str)

    assert data["release"] == {
        "swhid": str(release.swhid()),
        "name": {
            "text": release.name.decode(),
            "base64": base64.b64encode(release.name).decode("ascii"),
        },
        "message": {"text": release.message.decode()},
        "author": {
            "email": {"text": release.author.email.decode()},
            "name": {"text": release.author.name.decode()},
            "fullname": {"text": release.author.fullname.decode()},
        }
        if release.author
        else None,
        "date": release.date.to_datetime().isoformat() if release.date else None,
        "targetType": release.target_type.value,
    }


def test_get_release_with_invalid_swhid(client):
    query_str = """
    {
      content(swhid: "swh:1:rel:invalid") {
        swhid
      }
    }
    """
    errors = utils.get_error_response(client, query_str)
    # API will throw an error in case of an invalid SWHID
    assert len(errors) == 1


def test_get_release_target_revision(client):
    swhid = "swh:1:rel:9129dc4e14acd0e51ca3bcd6b80f4577d281fd25"
    query_str = """
    {
      release(swhid: "%s") {
        targetType
        target {
          ...on Revision {
            swhid
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % swhid)
    assert data["release"] == {
        "target": {"swhid": "swh:1:rev:66c7c1cd9673275037140f2abff7b7b11fc9439c"},
        "targetType": "revision",
    }


def test_get_release_target_release(client):
    swhid = "swh:1:rel:6429dc4e14acd0e51ca3bcd6b80f4577d281fd32"
    query_str = """
    {
      release(swhid: "%s") {
        targetType
        target {
          ...on Release {
            swhid
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % swhid)
    assert data["release"] == {
        "target": {"swhid": "swh:1:rel:8059dc4e17fcd0e51ca3bcd6b80f4577d281fd08"},
        "targetType": "release",
    }


def test_get_release_target_directory(client):
    swhid = "swh:1:rel:3129dc4e14acd0e51ca3bcd6b80f4577d281fd42"
    query_str = """
    {
      release(swhid: "%s") {
        targetType
        target {
          ...on Directory {
            swhid
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % swhid)
    assert data["release"] == {
        "target": {"swhid": "swh:1:dir:4b825dc642cb6eb9a060e54bf8d69288fbee4904"},
        "targetType": "directory",
    }


def test_get_release_target_content(client):
    swhid = "swh:1:rel:7589dc4e14acd0e51ca3bcd6b80f4577d281fd34"
    query_str = """
    {
      release(swhid: "%s") {
        targetType
        target {
          ...on Content {
            swhid
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % swhid)
    assert data["release"] == {
        "target": {"swhid": "swh:1:cnt:86bc6b377e9d25f9d26777a4a28d08e63e7c5779"},
        "targetType": "content",
    }


def test_get_release_target_unknown(client):
    # Clinet can request all the possible options if the target type
    # is unknown. The data under the right type will be returned

    # The target is of type Revision in this case
    # ie: both swhid and message will be available in the response
    swhid = "swh:1:rel:9129dc4e14acd0e51ca3bcd6b80f4577d281fd25"
    query_str = """
    {
      release(swhid: "%s") {
        targetType
        target {
          ...on Revision {
            swhid
            message {
              text
            }
          }
          ...on Release {
            swhid
          }
          ...on Directory {
            swhid
          }
          ...on Content {
            swhid
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % swhid)
    assert data["release"] == {
        "target": {
            "message": {"text": "hello"},
            "swhid": "swh:1:rev:66c7c1cd9673275037140f2abff7b7b11fc9439c",
        },
        "targetType": "revision",
    }
