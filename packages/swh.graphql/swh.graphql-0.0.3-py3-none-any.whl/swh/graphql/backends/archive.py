# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql import server
from swh.model.swhids import ObjectType


class Archive:
    def __init__(self):
        self.storage = server.get_storage()

    def get_origin(self, url):
        return self.storage.origin_get([url])[0]

    def get_origins(self, after=None, first=50):
        return self.storage.origin_list(page_token=after, limit=first)

    def get_origin_visits(self, origin_url, after=None, first=50):
        return self.storage.origin_visit_get(origin_url, page_token=after, limit=first)

    def get_origin_visit(self, origin_url, visit_id):
        return self.storage.origin_visit_get_by(origin_url, visit_id)

    def get_origin_latest_visit(self, origin_url):
        return self.storage.origin_visit_get_latest(origin_url)

    def get_visit_status(self, origin_url, visit_id, after=None, first=50):
        return self.storage.origin_visit_status_get(
            origin_url, visit_id, page_token=after, limit=first
        )

    def get_latest_visit_status(self, origin_url, visit_id):
        return self.storage.origin_visit_status_get_latest(origin_url, visit_id)

    def get_origin_snapshots(self, origin_url):
        return self.storage.origin_snapshot_get_all(origin_url)

    def get_snapshot_branches(
        self, snapshot, after=b"", first=50, target_types=None, name_include=None
    ):
        return self.storage.snapshot_get_branches(
            snapshot,
            branches_from=after,
            branches_count=first,
            target_types=target_types,
            branch_name_include_substring=name_include,
        )

    def get_revisions(self, revision_ids):
        return self.storage.revision_get(revision_ids=revision_ids)

    def get_revision_log(self, revision_ids, after=None, first=50):
        return self.storage.revision_log(revisions=revision_ids, limit=first)

    def get_releases(self, release_ids):
        return self.storage.release_get(releases=release_ids)

    def get_directory_entries(self, directory_id, after=None, first=50):
        return self.storage.directory_get_entries(
            directory_id, limit=first, page_token=after
        )

    def is_object_available(self, object_id: str, object_type: ObjectType) -> bool:
        mapping = {
            ObjectType.CONTENT: self.storage.content_missing_per_sha1_git,
            ObjectType.DIRECTORY: self.storage.directory_missing,
            ObjectType.RELEASE: self.storage.release_missing,
            ObjectType.REVISION: self.storage.revision_missing,
            ObjectType.SNAPSHOT: self.storage.snapshot_missing,
        }
        return not list(mapping[object_type]([object_id]))

    def get_contents(self, checksums: dict):
        return self.storage.content_find(checksums)

    def get_content_data(self, content_sha1):
        return self.storage.content_get_data(content_sha1)
