import heapq
import os
import pickle
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
class HuffmanCompressor:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}
    
    def build_frequency_dict(self, data):
        """Count frequency of each byte in data"""
        return Counter(data)
    
    def build_heap(self, frequency):
        """Build a min-heap based on byte frequencies"""
        heap = []
        for byte_val, freq in frequency.items():
            node = HuffmanNode(byte_val, freq)
            heapq.heappush(heap, node)
        return heap
    
    def build_huffman_tree(self, heap):
        """Build Huffman tree by merging nodes"""
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def build_codes(self, node, current_code=""):
        """Build Huffman codes by traversing the tree"""
        if node is None:
            return
        
        if node.char is not None:
            # Handle single character case
            self.codes[node.char] = current_code if current_code else "0"
            self.reverse_mapping[current_code if current_code else "0"] = node.char
            return
        
        self.build_codes(node.left, current_code + "0")
        self.build_codes(node.right, current_code + "1")