# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.model.hashutil import hash_to_bytes
from swh.model.model import ObjectType, Release, Revision, RevisionType
from swh.model.tests import swh_model_data


def populate_search_data(search):
    search.origin_update({"url": origin.url} for origin in get_origins())


def get_origins():
    return swh_model_data.ORIGINS


def get_snapshots():
    return swh_model_data.SNAPSHOTS


def get_releases():
    return swh_model_data.RELEASES


def get_revisions():
    return swh_model_data.REVISIONS


def get_contents():
    return swh_model_data.CONTENTS


def get_directories():
    return swh_model_data.DIRECTORIES


def get_releases_with_target():
    """
    GraphQL will not return a target object unless the target id
    is present in the DB.
    Return release objects with real targets instead of dummy
    targets in swh.model.tests.swh_model_data
    """
    with_revision = Release(
        id=hash_to_bytes("9129dc4e14acd0e51ca3bcd6b80f4577d281fd25"),
        name=b"v0.0.1",
        target_type=ObjectType.REVISION,
        target=get_revisions()[0].id,
        message=b"foo",
        synthetic=False,
    )
    with_release = Release(
        id=hash_to_bytes("6429dc4e14acd0e51ca3bcd6b80f4577d281fd32"),
        name=b"v0.0.1",
        target_type=ObjectType.RELEASE,
        target=get_releases()[0].id,
        message=b"foo",
        synthetic=False,
    )
    with_directory = Release(
        id=hash_to_bytes("3129dc4e14acd0e51ca3bcd6b80f4577d281fd42"),
        name=b"v0.0.1",
        target_type=ObjectType.DIRECTORY,
        target=get_directories()[0].id,
        message=b"foo",
        synthetic=False,
    )
    with_content = Release(
        id=hash_to_bytes("7589dc4e14acd0e51ca3bcd6b80f4577d281fd34"),
        name=b"v0.0.1",
        target_type=ObjectType.CONTENT,
        target=get_contents()[0].sha1_git,
        message=b"foo",
        synthetic=False,
    )
    return [with_revision, with_release, with_directory, with_content]


def get_revisions_with_parents():
    """
    Revisions with real revisions as parents
    """
    return [
        Revision(
            id=hash_to_bytes("37580d63b8dcc0ec73e74994e66896858542844c"),
            message=b"hello",
            date=swh_model_data.DATES[0],
            committer=swh_model_data.COMMITTERS[0],
            author=swh_model_data.COMMITTERS[0],
            committer_date=swh_model_data.DATES[0],
            type=RevisionType.GIT,
            directory=b"\x01" * 20,
            synthetic=False,
            parents=(get_revisions()[0].id, get_revisions()[1].id),
        )
    ]


GRAPHQL_EXTRA_TEST_OBJECTS = {
    "release": get_releases_with_target(),
    "revision": get_revisions_with_parents(),
}


def populate_dummy_data(storage):
    for object_type, objects in swh_model_data.TEST_OBJECTS.items():
        method = getattr(storage, object_type + "_add")
        method(objects)
    for object_type, objects in GRAPHQL_EXTRA_TEST_OBJECTS.items():
        method = getattr(storage, object_type + "_add")
        method(objects)
