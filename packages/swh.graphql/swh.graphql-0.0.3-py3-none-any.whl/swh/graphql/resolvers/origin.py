# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive, search
from swh.model.model import Origin
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseSWHNode
from .search import SearchResultNode


class BaseOriginNode(BaseSWHNode):
    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Origin"


class OriginNode(BaseOriginNode):
    """
    Node resolver for an origin requested directly with its URL
    """

    def _get_node_data(self):
        return archive.Archive().get_origin(self.kwargs.get("url"))


class TargetOriginNode(BaseOriginNode):
    """
    Node resolver for an origin requested as a target
    """

    obj: SearchResultNode

    def _get_node_data(self):
        # The target origin URL is guaranteed to exist in the archive
        # Hence returning the origin object without any explicit check in the archive
        # This assumes that the search index and archive are in sync
        return Origin(self.obj.target_url)


class OriginConnection(BaseConnection):
    """
    Connection resolver for the origins
    """

    _node_class = BaseOriginNode

    def _get_paged_result(self) -> PagedResult:
        # Use the search backend if a urlPattern is given
        if self.kwargs.get("urlPattern"):
            origins = search.Search().get_origins(
                query=self.kwargs.get("urlPattern"),
                after=self._get_after_arg(),
                first=self._get_first_arg(),
            )
            results = [Origin(ori["url"]) for ori in origins.results]
            return PagedResult(results=results, next_page_token=origins.next_page_token)
        # Use the archive backend by default
        return archive.Archive().get_origins(
            after=self._get_after_arg(), first=self._get_first_arg()
        )
