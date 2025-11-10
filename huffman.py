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
    def get_encoded_data(self, data):
        """Convert bytes to encoded binary string"""
        encoded_text = ""
        for byte_val in data:
            encoded_text += self.codes[byte_val]
        return encoded_text
    
    def pad_encoded_text(self, encoded_text):
        """Pad encoded text to make it multiple of 8 bits"""
        extra_padding = 8 - (len(encoded_text) % 8)
        if extra_padding == 8:
            extra_padding = 0
        encoded_text += '0' * extra_padding
        
        # Store padding info at beginning (3 bits is enough for 0-7)
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text
    
    def get_byte_array(self, padded_encoded_text):
        """Convert binary string to byte array"""
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte_segment = padded_encoded_text[i:i+8]
            b.append(int(byte_segment, 2))
        return b
    def remove_padding(self, padded_encoded_text):
        """Remove padding from encoded text"""
        # Read 3 bits for padding info
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        
        padded_encoded_text = padded_encoded_text[8:]
        if extra_padding > 0:
            encoded_text = padded_encoded_text[:-extra_padding]
        else:
            encoded_text = padded_encoded_text
        
        return encoded_text