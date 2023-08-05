# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from . import utils
from ..data import get_contents


@pytest.mark.parametrize("content", get_contents())
def test_get_content_with_swhid(client, content):
    query_str = """
    {
      content(swhid: "%s") {
        swhid
        checksum {
          blake2s256
          sha1
          sha1_git
          sha256
        }
        length
        status
        data {
          url
        }
        fileType {
          encoding
        }
        language {
          lang
        }
        license {
          licenses
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % content.swhid())
    archive_url = "https://archive.softwareheritage.org/api/1/"
    response = {
        "swhid": str(content.swhid()),
        "checksum": {
            "blake2s256": content.blake2s256.hex(),
            "sha1": content.sha1.hex(),
            "sha1_git": content.sha1_git.hex(),
            "sha256": content.sha256.hex(),
        },
        "length": content.length,
        "status": content.status,
        "data": {
            "url": f"{archive_url}content/sha1:{content.sha1.hex()}/raw/",
        },
        "fileType": None,
        "language": None,
        "license": None,
    }
    assert data["content"] == response


@pytest.mark.parametrize("content", get_contents())
def test_get_content_with_hash(client, content):
    query_str = """
    {
      contentByHash(checksums: ["blake2s256:%s", "sha1:%s", "sha1_git:%s", "sha256:%s"]) {
        swhid
      }
    }
    """
    data, _ = utils.get_query_response(
        client,
        query_str
        % (
            content.blake2s256.hex(),
            content.sha1.hex(),
            content.sha1_git.hex(),
            content.sha256.hex(),
        ),
    )
    assert data["contentByHash"] == {"swhid": str(content.swhid())}


def test_get_content_with_invalid_swhid(client):
    query_str = """
    {
      content(swhid: "swh:1:cnt:invalid") {
        swhid
      }
    }
    """
    errors = utils.get_error_response(client, query_str)
    # API will throw an error in case of an invalid SWHID
    assert len(errors) == 1
    assert "Invalid SWHID: invalid syntax" in errors[0]["message"]


def test_get_content_with_invalid_hashes(client):
    content = get_contents()[0]
    query_str = """
    {
      contentByHash(checksums: ["blake2s256:%s", "sha1:%s", "sha1_git:%s", "sha256:%s"]) {
        swhid
      }
    }
    """
    errors = utils.get_error_response(
        client,
        query_str
        % (
            "invalid",  # Only one hash is invalid
            content.sha1.hex(),
            content.sha1_git.hex(),
            content.sha256.hex(),
        ),
    )
    # API will throw an error in case of an invalid content hash
    assert len(errors) == 1
    assert "Invalid content checksum" in errors[0]["message"]


def test_get_content_as_target(client):
    # SWHID of a test dir with a file entry
    directory_swhid = "swh:1:dir:87b339104f7dc2a8163dec988445e3987995545f"
    query_str = """
    {
      directory(swhid: "%s") {
        swhid
        entries(first: 2) {
          nodes {
            type
            target {
              ...on Content {
                swhid
                length
              }
            }
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str % directory_swhid)
    content_obj = data["directory"]["entries"]["nodes"][1]["target"]
    assert content_obj == {
        "length": 4,
        "swhid": "swh:1:cnt:86bc6b377e9d25f9d26777a4a28d08e63e7c5779",
    }
