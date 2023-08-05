# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql.resolvers import resolver_factory


class TestFactory:
    @pytest.mark.parametrize(
        "input_type, expected",
        [
            ("origin", "OriginNode"),
            ("visit", "OriginVisitNode"),
            ("latest-visit", "LatestVisitNode"),
            ("latest-status", "LatestVisitStatusNode"),
            ("visit-snapshot", "VisitSnapshotNode"),
            ("snapshot", "SnapshotNode"),
            ("branch-revision", "TargetRevisionNode"),
            ("branch-release", "TargetReleaseNode"),
            ("branch-directory", "TargetDirectoryNode"),
            ("branch-content", "TargetContentNode"),
            ("branch-snapshot", "TargetSnapshotNode"),
            ("revision", "RevisionNode"),
            ("revision-directory", "RevisionDirectoryNode"),
            ("release", "ReleaseNode"),
            ("release-revision", "TargetRevisionNode"),
            ("release-release", "TargetReleaseNode"),
            ("release-directory", "TargetDirectoryNode"),
            ("release-content", "TargetContentNode"),
            ("directory", "DirectoryNode"),
            ("content", "ContentNode"),
            ("dir-entry-dir", "TargetDirectoryNode"),
            ("dir-entry-file", "TargetContentNode"),
            ("search-result-snapshot", "TargetSnapshotNode"),
            ("search-result-revision", "TargetRevisionNode"),
            ("search-result-release", "TargetReleaseNode"),
            ("search-result-directory", "TargetDirectoryNode"),
            ("search-result-content", "TargetContentNode"),
        ],
    )
    def test_get_node_resolver(self, input_type, expected):
        response = resolver_factory.get_node_resolver(input_type)
        assert response.__name__ == expected

    def test_get_node_resolver_invalid_type(self):
        with pytest.raises(AttributeError):
            resolver_factory.get_node_resolver("invalid")

    @pytest.mark.parametrize(
        "input_type, expected",
        [
            ("origins", "OriginConnection"),
            ("origin-visits", "OriginVisitConnection"),
            ("origin-snapshots", "OriginSnapshotConnection"),
            ("visit-status", "VisitStatusConnection"),
            ("snapshot-branches", "SnapshotBranchConnection"),
            ("revision-parents", "ParentRevisionConnection"),
            ("revision-log", "LogRevisionConnection"),
            ("directory-entries", "DirectoryEntryConnection"),
            ("resolve-swhid", "ResolveSwhidConnection"),
        ],
    )
    def test_get_connection_resolver(self, input_type, expected):
        response = resolver_factory.get_connection_resolver(input_type)
        assert response.__name__ == expected

    def test_get_connection_resolver_invalid_type(self):
        with pytest.raises(AttributeError):
            resolver_factory.get_connection_resolver("invalid")
