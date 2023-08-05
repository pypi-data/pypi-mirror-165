# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from .content import ContentNode, HashContentNode, TargetContentNode
from .directory import DirectoryNode, RevisionDirectoryNode, TargetDirectoryNode
from .directory_entry import DirectoryEntryConnection
from .origin import OriginConnection, OriginNode, TargetOriginNode
from .release import ReleaseNode, TargetReleaseNode
from .revision import (
    LogRevisionConnection,
    ParentRevisionConnection,
    RevisionNode,
    TargetRevisionNode,
)
from .search import ResolveSwhidConnection, SearchConnection
from .snapshot import (
    OriginSnapshotConnection,
    SnapshotNode,
    TargetSnapshotNode,
    VisitSnapshotNode,
)
from .snapshot_branch import AliasSnapshotBranchNode, SnapshotBranchConnection
from .visit import LatestVisitNode, OriginVisitConnection, OriginVisitNode
from .visit_status import LatestVisitStatusNode, VisitStatusConnection


def get_node_resolver(resolver_type):
    # FIXME, replace with a proper factory method
    mapping = {
        "origin": OriginNode,
        "visit": OriginVisitNode,
        "latest-visit": LatestVisitNode,
        "latest-status": LatestVisitStatusNode,
        "visit-snapshot": VisitSnapshotNode,
        "snapshot": SnapshotNode,
        "branch-alias": AliasSnapshotBranchNode,
        "branch-revision": TargetRevisionNode,
        "branch-release": TargetReleaseNode,
        "branch-directory": TargetDirectoryNode,
        "branch-content": TargetContentNode,
        "branch-snapshot": TargetSnapshotNode,
        "revision": RevisionNode,
        "revision-directory": RevisionDirectoryNode,
        "release": ReleaseNode,
        "release-revision": TargetRevisionNode,
        "release-release": TargetReleaseNode,
        "release-directory": TargetDirectoryNode,
        "release-content": TargetContentNode,
        "directory": DirectoryNode,
        "content": ContentNode,
        "content-by-hash": HashContentNode,
        "dir-entry-dir": TargetDirectoryNode,
        "dir-entry-file": TargetContentNode,
        "search-result-origin": TargetOriginNode,
        "search-result-snapshot": TargetSnapshotNode,
        "search-result-revision": TargetRevisionNode,
        "search-result-release": TargetReleaseNode,
        "search-result-directory": TargetDirectoryNode,
        "search-result-content": TargetContentNode,
    }
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid node type: {resolver_type}")
    return mapping[resolver_type]


def get_connection_resolver(resolver_type):
    # FIXME, replace with a proper factory method
    mapping = {
        "origins": OriginConnection,
        "origin-visits": OriginVisitConnection,
        "origin-snapshots": OriginSnapshotConnection,
        "visit-status": VisitStatusConnection,
        "snapshot-branches": SnapshotBranchConnection,
        "revision-parents": ParentRevisionConnection,
        "revision-log": LogRevisionConnection,
        "directory-entries": DirectoryEntryConnection,
        "resolve-swhid": ResolveSwhidConnection,
        "search": SearchConnection,
    }
    if resolver_type not in mapping:
        raise AttributeError(f"Invalid connection type: {resolver_type}")
    return mapping[resolver_type]
