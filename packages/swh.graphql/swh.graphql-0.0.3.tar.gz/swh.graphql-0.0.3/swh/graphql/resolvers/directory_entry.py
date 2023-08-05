# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class DirectoryEntryNode(BaseNode):
    """
    Node resolver for a directory entry
    """

    @property
    def target_hash(self):  # for DirectoryNode
        return self._node.target


class DirectoryEntryConnection(BaseConnection):
    """
    Connection resolver for entries in a directory
    """

    from .directory import BaseDirectoryNode

    obj: BaseDirectoryNode

    _node_class = DirectoryEntryNode

    def _get_paged_result(self) -> PagedResult:
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO
        entries = (
            archive.Archive().get_directory_entries(self.obj.swhid.object_id).results
        )
        return utils.paginated(entries, self._get_first_arg(), self._get_after_arg())
