# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive
from swh.model.swhids import CoreSWHID, ObjectType
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode
from .visit import BaseVisitNode


class BaseVisitStatusNode(BaseNode):
    """
    Base resolver for all the visit-status nodes
    """

    @property
    def snapshotSWHID(self):  # To support the schema naming convention
        return CoreSWHID(object_type=ObjectType.SNAPSHOT, object_id=self._node.snapshot)


class LatestVisitStatusNode(BaseVisitStatusNode):
    """
    Node resolver for a visit-status requested from a visit
    """

    obj: BaseVisitNode

    def _get_node_data(self):
        # self.obj.origin is the origin URL
        return archive.Archive().get_latest_visit_status(
            self.obj.origin, self.obj.visitId
        )


class VisitStatusConnection(BaseConnection):
    """
    Connection resolver for the visit-status objects in a visit
    """

    obj: BaseVisitNode
    _node_class = BaseVisitStatusNode

    def _get_paged_result(self) -> PagedResult:
        # self.obj.origin is the origin URL
        return archive.Archive().get_visit_status(
            self.obj.origin,
            self.obj.visitId,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
        )
