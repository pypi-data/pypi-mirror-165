# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Union

from swh.graphql.backends import archive

from .base_node import BaseSWHNode
from .snapshot_branch import BaseSnapshotBranchNode


class BaseReleaseNode(BaseSWHNode):
    """
    Base resolver for all the release nodes
    """

    def _get_release_by_id(self, release_id):
        return (archive.Archive().get_releases([release_id]) or None)[0]

    @property
    def target_hash(self):
        return self._node.target

    @property
    def targetType(self):  # To support the schema naming convention
        return self._node.target_type.value

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Release"


class ReleaseNode(BaseReleaseNode):
    """
    Node resolver for a release requested directly with its SWHID
    """

    def _get_node_data(self):
        return self._get_release_by_id(self.kwargs.get("swhid").object_id)


class TargetReleaseNode(BaseReleaseNode):
    """
    Node resolver for a release requested as a target
    """

    obj: Union[BaseSnapshotBranchNode, BaseReleaseNode]

    def _get_node_data(self):
        # self.obj.target_hash is the requested release id
        return self._get_release_by_id(self.obj.target_hash)
