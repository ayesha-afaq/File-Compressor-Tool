import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

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
        
