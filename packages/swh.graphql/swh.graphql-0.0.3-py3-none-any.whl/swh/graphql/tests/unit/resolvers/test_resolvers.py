# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql import resolvers
from swh.graphql.resolvers import resolvers as rs


class TestResolvers:
    """ """

    @pytest.fixture
    def dummy_node(self):
        return {"test": "test"}

    @pytest.mark.parametrize(
        "resolver_func, node_cls",
        [
            (rs.origin_resolver, resolvers.origin.OriginNode),
            (rs.visit_resolver, resolvers.visit.OriginVisitNode),
            (rs.latest_visit_resolver, resolvers.visit.LatestVisitNode),
            (
                rs.latest_visit_status_resolver,
                resolvers.visit_status.LatestVisitStatusNode,
            ),
            (rs.snapshot_resolver, resolvers.snapshot.SnapshotNode),
            (rs.visit_snapshot_resolver, resolvers.snapshot.VisitSnapshotNode),
            (rs.revision_resolver, resolvers.revision.RevisionNode),
            (rs.revision_directory_resolver, resolvers.directory.RevisionDirectoryNode),
            (rs.release_resolver, resolvers.release.ReleaseNode),
            (rs.directory_resolver, resolvers.directory.DirectoryNode),
            (rs.content_resolver, resolvers.content.ContentNode),
        ],
    )
    def test_node_resolver(self, mocker, dummy_node, resolver_func, node_cls):
        mock_get = mocker.patch.object(node_cls, "_get_node", return_value=dummy_node)
        node_obj = resolver_func(None, None)
        # assert the _get_node method is called on the right object
        assert isinstance(node_obj, node_cls)
        assert mock_get.assert_called

    @pytest.mark.parametrize(
        "resolver_func, connection_cls",
        [
            (rs.origins_resolver, resolvers.origin.OriginConnection),
            (rs.visits_resolver, resolvers.visit.OriginVisitConnection),
            (rs.origin_snapshots_resolver, resolvers.snapshot.OriginSnapshotConnection),
            (rs.visitstatus_resolver, resolvers.visit_status.VisitStatusConnection),
            (
                rs.snapshot_branches_resolver,
                resolvers.snapshot_branch.SnapshotBranchConnection,
            ),
            (rs.revision_parents_resolver, resolvers.revision.ParentRevisionConnection),
            # (rs.revision_log_resolver, resolvers.revision.LogRevisionConnection),
            (
                rs.directory_entry_resolver,
                resolvers.directory_entry.DirectoryEntryConnection,
            ),
        ],
    )
    def test_connection_resolver(self, resolver_func, connection_cls):
        connection_obj = resolver_func(None, None)
        # assert the right object is returned
        assert isinstance(connection_obj, connection_cls)

    @pytest.mark.parametrize(
        "branch_type, node_cls",
        [
            ("revision", resolvers.revision.TargetRevisionNode),
            ("release", resolvers.release.TargetReleaseNode),
            ("directory", resolvers.directory.TargetDirectoryNode),
            ("content", resolvers.content.TargetContentNode),
            ("snapshot", resolvers.snapshot.TargetSnapshotNode),
        ],
    )
    def test_snapshot_branch_target_resolver(
        self, mocker, dummy_node, branch_type, node_cls
    ):
        obj = mocker.Mock(type=branch_type)
        mock_get = mocker.patch.object(node_cls, "_get_node", return_value=dummy_node)
        node_obj = rs.snapshot_branch_target_resolver(obj, None)
        assert isinstance(node_obj, node_cls)
        assert mock_get.assert_called

    @pytest.mark.parametrize(
        "target_type, node_cls",
        [
            ("revision", resolvers.revision.TargetRevisionNode),
            ("release", resolvers.release.TargetReleaseNode),
            ("directory", resolvers.directory.TargetDirectoryNode),
            ("content", resolvers.content.TargetContentNode),
        ],
    )
    def test_release_target_resolver(self, mocker, dummy_node, target_type, node_cls):
        obj = mocker.Mock(target_type=(mocker.Mock(value=target_type)))
        mock_get = mocker.patch.object(node_cls, "_get_node", return_value=dummy_node)
        node_obj = rs.release_target_resolver(obj, None)
        assert isinstance(node_obj, node_cls)
        assert mock_get.assert_called

    @pytest.mark.parametrize(
        "target_type, node_cls",
        [
            ("dir", resolvers.directory.TargetDirectoryNode),
            ("file", resolvers.content.TargetContentNode),
        ],
    )
    def test_directory_entry_target_resolver(
        self, mocker, dummy_node, target_type, node_cls
    ):
        obj = mocker.Mock(type=target_type)
        mock_get = mocker.patch.object(node_cls, "_get_node", return_value=dummy_node)
        node_obj = rs.directory_entry_target_resolver(obj, None)
        assert isinstance(node_obj, node_cls)
        assert mock_get.assert_called

    def test_union_resolver(self, mocker):
        obj = mocker.Mock()
        obj.is_type_of.return_value = "test"
        assert rs.union_resolver(obj) == "test"

    def test_binary_string_text_resolver(self):
        text = rs.binary_string_text_resolver(b"test", None)
        assert text == "test"

    def test_binary_string_base64_resolver(self):
        b64string = rs.binary_string_base64_resolver(b"test", None)
        assert b64string == "dGVzdA=="
