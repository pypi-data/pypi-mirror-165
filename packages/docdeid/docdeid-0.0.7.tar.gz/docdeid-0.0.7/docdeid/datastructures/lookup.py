import codecs
from typing import Iterable, Optional, Union, Hashable

import itertools

from docdeid.datastructures.datastructure import Datastructure
from docdeid.string.processor import BaseStringProcessor, StripString


class LookupList(Datastructure):
    def __init__(self):
        self._items = set()

    def clear_items(self):
        self._items = set()

    def add_item(
        self, item: str, cleaning_pipeline: Optional[list[BaseStringProcessor]] = None
    ):

        if cleaning_pipeline is not None:

            for processor in cleaning_pipeline:
                item = processor.process_item(item)

                if item is None:
                    return

        self._items.add(item)

    def add_items_from_file(
        self,
        file: str,
        strip_lines: bool = True,
        cleaning_pipeline: Optional[list[BaseStringProcessor]] = None,
        encoding: str = "utf-8",
    ):

        with codecs.open(file, encoding=encoding) as handle:
            items = handle.read().splitlines()

        if strip_lines:
            cleaning_pipeline = [StripString()] + (cleaning_pipeline or [])

        self.add_items_from_iterable(items, cleaning_pipeline)

    def add_items_from_iterable(
        self,
        items: Iterable[str],
        cleaning_pipeline: Optional[list[BaseStringProcessor]] = None,
    ):

        for item in items:
            self.add_item(item, cleaning_pipeline)

    def add_items_from_self(
        self,
        cleaning_pipeline: Optional[list[BaseStringProcessor]] = None,
        replace: bool = False,
    ):

        items = self._items.copy()

        if replace:
            self.clear_items()

        for item in items:
            self.add_item(item, cleaning_pipeline)

    def __contains__(self, item: str) -> bool:
        return item in self._items

    def __add__(self, other):

        if not isinstance(other, LookupList):
            raise ValueError(
                f"Can only add LookupList together, trying to add a {type(other.__name__)}"
            )

        combined_list = LookupList()
        combined_list.add_items_from_iterable(self._items.union(other._items))
        return combined_list

    def __sub__(self, other):

        if not isinstance(other, LookupList):
            raise ValueError(
                f"Can only subtract LookupList from each other, trying to subtract a {type(other.__name__)}"
            )

        combined_list = LookupList()
        combined_list.add_items_from_iterable(self._items.difference(other._items))
        return combined_list

    def __iter__(self):
        return iter(self._items)


class LookupTrie(Datastructure):

    def __init__(self):
        self._children = {}
        self._is_terminal = False

    def add(self, items: list[Hashable]):

        if len(items) == 0:
            self._is_terminal = True

        else:

            head, tail = items[0], items[1:]

            if head not in self._children:
                self._children[head] = LookupTrie()

            self._children[head].add(tail)

    def __contains__(self, items: list[Hashable]) -> bool:

        if len(items) == 0:
            return self._is_terminal

        head, tail = items[0], items[1:]

        return (head in self._children) and tail in self._children[head]

    def longest_matching_prefix(self, items: list[Hashable]) -> Union[list, None]:

        longest_match = None
        current_node = self

        for i in itertools.count():

            if current_node._is_terminal:
                longest_match = i

            if i >= len(items) or (items[i] not in current_node._children):
                break

            current_node = current_node._children[items[i]]

        return items[:longest_match] if longest_match else None


if __name__ == '__main__':

    t = LookupTrie()

    t.add([])
    t.add([1, 2])
    t.add([1, 2, 3, 4, 5])

    print(t.longest_matching_prefix([1, 2, 3]))


# def longest_matching_prefix(self, items: list[Hashable]) -> Union[list, None]:
#
#     if (len(items) == 0) or (items[0] not in self._nodes):
#         return [] if self._is_terminal else None
#
#     rec = self._nodes[items[0]].longest_matching_prefix(items[1:])
#
#     if rec is None:
#
#         if self._is_terminal:
#             return []
#         else:
#             return None
#     else:
#         return [items[0]] + rec

#
#
# class LookupTrie(Datastructure):
#     """
#     This class contains an implementation of a ListTrie, which is not much different
#     from a normal Trie, except that it accepts lists. It also has a method for
#     finding all prefixes of a certain list.
#     """
#
#     def __init__(self):
#         """Initiate ListTrie"""
#         self.root = _ListTrieNode()
#
#     def add(self, item_list):
#         """Add a list to the ListTrie"""
#         self.root.add(item_list, 0)
#
#     def print_all(self):
#         """Print all lists in the ListTrie"""
#         self.root.print_all([])
#
#     def find_all(self):
#         """Find all lists in the ListTrie"""
#         result = []
#         self.root.find_all([], result)
#         return result
#
#     def find_all_prefixes(self, prefix):
#         """Find all lists in the ListTrie that are a prefix of the prefix argument"""
#         result = []
#         self.root.find_all_prefixes([], prefix, 0, result)
#         return result
#
#     def find_longest_common_prefix(self, text: list[str]) -> Union[None, list[str]]:
#
#         prefixes = self.find_all_prefixes(text)
#
#         if len(prefixes) == 0:
#             return None
#
#         return max(prefixes, key=lambda x: len(x))
#
#
# class _ListTrieNode:
#     """List Trie Nodes"""
#
#     def __init__(self):
#         """Initiate ListTrieNode with empty dictionary and non terminal state"""
#         self.nodes = {}  # empty dict
#         self.is_terminal = False
#
#     def add(self, item_list, position):
#         """Add a list to the ListTrie by adding the current item
#         in the list to this ListTrieNode"""
#
#         # Last position of the list, make the node terminal
#         if position == len(item_list):
#             self.is_terminal = True
#
#         # Else recurse
#         else:
#
#             # Current item in the list
#             current_item = item_list[position]
#
#             # If the item is not yet in the dictionary, create a new empty ListTrieNode
#             if current_item not in self.nodes:
#                 self.nodes[current_item] = _ListTrieNode()
#
#             # Recurse on the ListTrieNode corresponding to the current_item
#             self.nodes[current_item].add(item_list, position + 1)
#
#     def print_all(self, item_list):
#         """Print all lists in the ListTrie"""
#
#         # If the ListTrieNode is terminal, print the list
#         if self.is_terminal:
#             print(item_list)
#
#         # Else recurse through the ListTrie
#         for key, node in self.nodes:
#             node.print_all(item_list + [key])
#
#     def find_all(self, item_list, result):
#         """Find all lists in the ListTrie"""
#
#         # If the ListTrieNode is terminal, append the list to the list of results
#         if self.is_terminal:
#             result.append(item_list)
#
#         # Else recurse through the ListTrie
#         for key, node in self.nodes:
#             node.find_all(item_list + [key], result)
#
#     def find_all_prefixes(self, item_list, prefix, prefix_pos, result):
#         """Find all lists in the ListTrie that are a prefix of the prefix argument"""
#
#         # If the ListTrieNode is terminal, append the list so far to the results
#         if self.is_terminal:
#             result.append(item_list)
#
#         # If we have not satisfied the prefix condition yet, continue
#         if prefix_pos < len(prefix):
#
#             # Current item in the list
#             current_item = prefix[prefix_pos]
#
#             # If the current item is in this node, continue
#             if current_item in self.nodes:
#
#                 node = self.nodes[current_item]
#                 key = current_item
#
#                 node.find_all_prefixes(
#                     item_list + [key], prefix, prefix_pos + 1, result
#                 )
#
