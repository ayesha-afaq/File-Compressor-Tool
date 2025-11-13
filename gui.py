import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from huffman import HuffmanCompressor

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Compressor")
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        
        self.compressor = HuffmanCompressor()
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Text File Compressor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        # Subtitle showing supported formats
        subtitle_label = ttk.Label(main_frame, 
                                   text="Supports: TXT, CSV, JSON, DOCX, XLSX (Text-based files only)", 
                                   font=("Arial", 9), foreground="gray")
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
         # Compression section
        compress_frame = ttk.LabelFrame(main_frame, text="Compress File", padding="10")
        compress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(compress_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.compress_input_entry = ttk.Entry(compress_frame, width=50)
        self.compress_input_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(compress_frame, text="Browse", 
                  command=self.browse_compress_input).grid(row=0, column=2, padx=5)
        
        ttk.Label(compress_frame, text="Output File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.compress_output_entry = ttk.Entry(compress_frame, width=50)
        self.compress_output_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(compress_frame, text="Browse", 
                  command=self.browse_compress_output).grid(row=1, column=2, padx=5)
        
        ttk.Button(compress_frame, text="Compress", 
                  command=self.compress_file).grid(row=2, column=1, pady=10)
        
