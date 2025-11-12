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
    
    
    def compress(self, input_path, output_path):
        """Main compression function - works with text-based file types"""
        print(f"Compressing {input_path}...")
        
        # Check if file type is supported
        allowed_extensions = ['.txt', '.csv', '.json', '.docx', '.doc', '.xlsx', '.xls']
        file_extension = os.path.splitext(input_path)[1].lower()
        
        if file_extension not in allowed_extensions:
            print(f"Error: File type {file_extension} is not supported!")
            print(f"Supported types: {', '.join(allowed_extensions)}")
            return False
        
        # Read input file as binary
        with open(input_path, 'rb') as file:
            data = file.read()
        
        if not data:
            print("File is empty!")
            return False
        
        # Store original file extension for decompression
        file_extension = os.path.splitext(input_path)[1]
        
        # Build Huffman tree and codes
        frequency = self.build_frequency_dict(data)
        heap = self.build_heap(frequency)
        root = self.build_huffman_tree(heap)
        self.build_codes(root)
        
        # Encode data
        encoded_text = self.get_encoded_data(data)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)
        
        # Write compressed file with optimized storage
        with open(output_path, 'wb') as output:
            # Store file metadata
            metadata = {
                'extension': file_extension,
                'mapping': self.reverse_mapping
            }
            pickle.dump(metadata, output, protocol=pickle.HIGHEST_PROTOCOL)
            output.write(bytes(byte_array))
        
        # Calculate compression ratio
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        ratio = (1 - compressed_size/original_size) * 100
        
        print(f"Compression completed!")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compression ratio: {ratio:.2f}%")
        
        return True
    
        
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
    def decode_data(self, encoded_text):
        """Decode binary string to original bytes"""
        current_code = ""
        decoded_data = bytearray()
        
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                byte_val = self.reverse_mapping[current_code]
                decoded_data.append(byte_val)
                current_code = ""
        
        return bytes(decoded_data)
    
    def decode_data(self, encoded_text):
        """Decode binary string to original bytes"""
        current_code = ""
        decoded_data = bytearray()
        
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                byte_val = self.reverse_mapping[current_code]
                decoded_data.append(byte_val)
                current_code = ""
        
        return bytes(decoded_data)
    
    def decompress(self, input_path, output_path):
        """Main decompression function - restores original file type"""
        print(f"Decompressing {input_path}...")
        
        with open(input_path, 'rb') as file:
            # Load metadata
            metadata = pickle.load(file)
            self.reverse_mapping = metadata['mapping']
            original_extension = metadata['extension']
            
            # Read compressed data
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte_val = byte[0]  # ✅ Correct way to get integer value of byte
                bits = bin(byte_val)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

        
        # Decode data
        encoded_text = self.remove_padding(bit_string)
        decompressed_data = self.decode_data(encoded_text)
        
        # If output path doesn't have extension, add the original one
        output_base, output_ext = os.path.splitext(output_path)
        if not output_ext and original_extension:
            output_path = output_base + original_extension
        elif output_ext and original_extension and output_ext.lower() != original_extension.lower():
            # If user specified different extension, warn but use original
            print(f"Note: Using original extension {original_extension} instead of {output_ext}")
            output_path = output_base + original_extension
        
        # Write decompressed file as binary
        with open(output_path, 'wb') as output:
            output.write(decompressed_data)
        
        print(f"Decompression completed!")
        print(f"File saved as: {output_path}")
        return True
