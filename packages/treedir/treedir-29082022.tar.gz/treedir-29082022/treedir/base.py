from anytree import AnyNode
from anytree.node.nodemixin import NodeMixin
from abc import ABC, abstractmethod


from networktools.library import set_id


class TreeDir(NodeMixin):
    __node_types = {"directory", "file"}
    idx_list = []
    node_map = {}

    def __init__(self, name, parent, options={}, *args, **kwargs):
        super().__init__()
        self.name = name
        self.parent = parent
        self.options = options if options else {}
        self.idx = self.new_idx()
        if parent:
            self.node_map = parent.node_map
        else:
            self.set_idx_node("root")
        self.set_idx_node(self.idx)

    def new_idx(self):
        idx = set_id(self.idx_list, uin=12)
        return idx

    def get_node(self, idx):
        return self.node_map.get(idx)

    def set_idx_node(self, idx:str):        
        self.node_map[idx] = self

    @property
    def can_have_children(self):
        return self.__node_type == "directory"

    @property
    def filename(self) -> str:
        """
        return the filename as string
        """
        pass

    @property
    def url(self) -> str:
        """
        return the url as string
        """
        pass

    def get_dict(self):
        return {}

    def children_directories(self):
        """
        Return the children directory path generator for instance
        """
        pass


    def set_parent(self, parent):
        idx_set_a = set(self.idx_list)
        idx_set_b = set(parent.idx_list)
        # check for emptyness
        something = idx_set_a - idx_set_b
        idx_add = idx_set_b - idx_set_a
        self.idx_list += list(idx_add)
        if something:
            # update the branch with nex idx if those exists on parent
            for old_idx in something:
                idx = self.new_idx()
                node = self.node_map[old_idx]
                del self.node_map[old_idx]
                if old_idx in self.node_list:
                    self.node_list.remove(old_idx)
                self.node_map[idx] = node
        # update parent node_map with self node map
        parent.node_map.update(self.node_map)
        # no change self node_map to parent node map
        self.node_map = parent.node_map
        # and the self idx list to parent idx_list
        parent.idx_list += self.idx_list
        self.parent = parent


