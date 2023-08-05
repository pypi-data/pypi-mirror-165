# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode
from .origin import OriginNode


class BaseVisitNode(BaseNode):
    """
    Base resolver for all the visit nodes
    """

    @property
    def id(self):
        # FIXME, use a better id
        return utils.get_b64_string(f"{self.origin}-{str(self.visit)}")

    @property
    def visitId(self):  # To support the schema naming convention
        return self._node.visit


class OriginVisitNode(BaseVisitNode):
    """
    Node resolver for a visit requested directly with an origin URL
    and a visit ID
    """

    def _get_node_data(self):
        return archive.Archive().get_origin_visit(
            self.kwargs.get("originUrl"), int(self.kwargs.get("visitId"))
        )


class LatestVisitNode(BaseVisitNode):
    """
    Node resolver for the latest visit in an origin
    """

    obj: OriginNode

    def _get_node_data(self):
        # self.obj.url is the origin URL
        return archive.Archive().get_origin_latest_visit(self.obj.url)


class OriginVisitConnection(BaseConnection):
    """
    Connection resolver for the visit objects in an origin
    """

    obj: OriginNode

    _node_class = BaseVisitNode

    def _get_paged_result(self) -> PagedResult:
        # self.obj.url is the origin URL
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
        )
