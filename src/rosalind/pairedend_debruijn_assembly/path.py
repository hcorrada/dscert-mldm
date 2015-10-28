from collections import defaultdict

# class representing item in a doubly-linked list
# we use this for path representation as a doubly-linked
# list of nodes
class DoubleList:
    def __init__(self, node, prev_item=None, next_item=None):
        self._node = node
        self._prev_item = prev_item
        self._next_item = next_item


# class representing a path
#
# slots:
#   _k: length of each part of input paired k-mers
#   _d: gap in paired k-mers
#   _head: first item in doubly-linked list
#   _tail: last item in doubly_linked list
class Path:
    # set head and tail to None
    # and create an empty node->item map
    def __init__(self):
        self._head = None
        self._tail = None
        self._item_map = defaultdict(list)

    # return true if path is empty
    def is_empty(self):
        return self._head is None and self._tail is None

    # append node to the tail of the list
    # add node to item map
    def append(self, node):
        # create a new item and add it
        # to the node->item map
        item = DoubleList(node)
        self._item_map[node.label()].append(item)

        if self.is_empty():
            # make new item head and tail of list
            self._head = self._tail = item
        else:
            # grab the item in the tail
            tail_item = self._tail

            # make item in tail point to new item
            tail_item._next_item = item

            # make new item's back pointer point to item in tail
            item._prev_item = tail_item

            # make the new item the tail of the list
            self._tail = item

    # find item in path linked list containing given node
    def find_item(self, node):
        # grab the list of items for the node
        item_map = self._item_map[node.label()]
        if item_map is None or len(item_map) == 0:
            return None
        else:
            # return the first item in the list
            return item_map[0]

    # return list of items in path containing
    # given node
    def find_all_items(self, node):
        return self._item_map[node.label()]

    # extend this path with other path
    # at given item
    #
    # starting state:
    #   self: self.head <-> ... <-> prev <-> item <-> next ... <-> self.tail
    #   other: other.head <-> ... <-> other.tail
    #
    # after stitching we will have
    #   self.head <-> ... <-> prev <-> other.head <-> ... <-> other.tail <-> next <-> ... <-> self.tail
    def stitch(self, item, other):
        # if this path is empty, just
        # return the other path
        if self.is_empty():
            return other

        # if there is no place to stich the other path
        # just return this path
        if item is None:
            return self

        # get reference to item preceding stitch item on this path
        prev_item = item._prev_item

        # stick head of other path after preceding item on this path
        # state after this operation
        #   a) self.head <-> ... <-> prev <-> other.head <-> ... <-> other.tail
        #   b) item <-> next <-> ... <-> self.tail
        prev_item._next_item = other._head
        other._head._prev_item = prev_item

        # get reference to next item on this path
        next_item = item._next_item

        # put tail of other path before next item on this path
        # we get final state after this operation
        next_item._prev_item = other._tail
        other._tail._next_item = next_item

        # merge item maps
        for label, item_list in other._item_map.items():
            self._item_map[label] += item_list
        return self

    # a generator for nodes in the path
    def nodes(self):
        current = self._head
        while current is not None:
            yield current._node
            # make sure you stop after the tail
            # to avoid inifite loop
            if current == self._tail:
                current = None
            else:
                current = current._next_item

    # a string representation of the path
    def __repr__(self):
        node_labels = [node.label().as_string() for node in self.nodes()]
        return " -> ".join(node_labels)
