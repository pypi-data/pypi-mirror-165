#!/usr/bin/env python3
# encoding: utf-8
"""
foo
"""

class UnionFind(object):
    """a class realize the union find algorithm, consuming a pair of str or unicode. output disjoint set of those str/unicode
    try to compatite both python 2 and python 3, but mainly for python 2.
    because the purpose is to get the disjoint set finally, we do not use the forest struct.
    
    usage:
        call add_set(v1, v2) multiple times, and then visite the root_to_set variable directly.
    """
    
    def __init__(self):
        self.root_to_set = {}
        self.to_root = {}
        
    def _find(self, ele):
        if ele in self.to_root:
            return self.to_root[ele]
        return None
    
    def _merge(self, root_1, root_2):
        len_1 = len(self.root_to_set[root_1])
        len_2 = len(self.root_to_set[root_2])
        if len_1 < len_2:
            for ele in self.root_to_set[root_1]:
                self.to_root[ele] = root_2
                self.root_to_set[root_2].add(ele)
            del self.root_to_set[root_1]
        else:
            for ele in self.root_to_set[root_2]:
                self.to_root[ele] = root_1
                self.root_to_set[root_1].add(ele)
            del self.root_to_set[root_2]
    
    def add_set(self, ele_1, ele_2):
        """
        only public method, adding an equivalent pair. 
        对外提供的唯一接口 把关联的两个加入到集合中 
        """
        root_1 = self._find(ele_1)
        root_2 = self._find(ele_2)
        
        if root_1:
            if root_1 == root_2:
                # already in same set, return
                return
            if root_2:
                # merge 2 exist sets
                self._merge(root_1, root_2)
            else:
                # root_2 is None
                self.to_root[ele_2] = root_1
                self.root_to_set[root_1].add(ele_2)
        else:
            if root_2:
                self.to_root[ele_1] = root_2
                self.root_to_set[root_2].add(ele_1)
            else:
                # both is None
                self.root_to_set[ele_1] = set([ele_1, ele_2])
                self.to_root[ele_1] = ele_1
                self.to_root[ele_2] = ele_1
