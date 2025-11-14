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
        
         # Decompression section
        decompress_frame = ttk.LabelFrame(main_frame, text="Decompress File", padding="10")
        decompress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 10))
        
        ttk.Label(decompress_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.decompress_input_entry = ttk.Entry(decompress_frame, width=50)
        self.decompress_input_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(decompress_frame, text="Browse", 
                  command=self.browse_decompress_input).grid(row=0, column=2, padx=5)
        
        ttk.Label(decompress_frame, text="Output File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.decompress_output_entry = ttk.Entry(decompress_frame, width=50)
        self.decompress_output_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(decompress_frame, text="Browse", 
                  command=self.browse_decompress_output).grid(row=1, column=2, padx=5)
        
        ttk.Button(decompress_frame, text="Decompress", 
                  command=self.decompress_file).grid(row=2, column=1, pady=10)
        
        # # Status section
        # status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        # status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # self.status_text = tk.Text(status_frame, height=8, width=60, state=tk.DISABLED)
        # self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # # Scrollbar for status text
        # scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        # scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        # self.status_text.configure(yscrollcommand=scrollbar.set)
        
    def browse_compress_input(self):
        filename = filedialog.askopenfilename(
            title="Select file to compress",
            filetypes=[
                ("All supported files", "*.txt *.csv *.json *.docx *.doc *.xlsx *.xls"),
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("Word documents", "*.docx *.doc"),
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.compress_input_entry.delete(0, tk.END)
            self.compress_input_entry.insert(0, filename)
            
            # Suggest output filename
            base_name = os.path.splitext(filename)[0]
            output_name = base_name + "_compressed.huf"
            self.compress_output_entry.delete(0, tk.END)
            self.compress_output_entry.insert(0, output_name)
    
    def browse_compress_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save compressed file as",
            defaultextension=".huf",
            filetypes=[("Huffman compressed", "*.huf"), ("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if filename:
            self.compress_output_entry.delete(0, tk.END)
            self.compress_output_entry.insert(0, filename)
    
    def browse_decompress_input(self):
        filename = filedialog.askopenfilename(
            title="Select file to decompress",
            filetypes=[("Huffman compressed", "*.huf"), ("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if filename:
            self.decompress_input_entry.delete(0, tk.END)
            self.decompress_input_entry.insert(0, filename)
            
            # Suggest output filename
            base_name = os.path.splitext(filename)[0]
            if base_name.endswith("_compressed"):
                base_name = base_name[:-11]
            output_name = base_name + "_decompressed"
            self.decompress_output_entry.delete(0, tk.END)
            self.decompress_output_entry.insert(0, output_name)
    
    def browse_decompress_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save decompressed file as",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("Word documents", "*.docx"),
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.decompress_output_entry.delete(0, tk.END)
            self.decompress_output_entry.insert(0, filename)

    def log_status(self, message):
        """Add message to status text area"""
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.configure(state=tk.DISABLED)
        self.root.update()
    
    def compress_file(self):
        input_file = self.compress_input_entry.get()
        output_file = self.compress_output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist")
            return

        try:
            # ✅ Always use a fresh compressor instance
            compressor = HuffmanCompressor()

            # Log info
            file_size = os.path.getsize(input_file)
            file_ext = os.path.splitext(input_file)[1].upper()

            allowed_extensions = ['.TXT', '.CSV', '.JSON', '.DOCX', '.DOC', '.XLSX', '.XLS']
            if file_ext not in allowed_extensions:
                messagebox.showerror(
                    "Error",
                    f"File type {file_ext} is not supported!\n\n"
                    f"Supported types: TXT, CSV, JSON, DOCX, DOC, XLSX, XLS"
                )
                self.log_status(f"✗ Error: Unsupported file type {file_ext}")
                return

            self.log_status(f"Starting compression...")
            self.log_status(f"File: {os.path.basename(input_file)} ({file_ext})")
            self.log_status(f"Size: {file_size:,} bytes")
            self.log_status("-" * 50)

            success = compressor.compress(input_file, output_file)

            if success:
                compressed_size = os.path.getsize(output_file)
                ratio = (1 - compressed_size / file_size) * 100
                self.log_status(f"✓ Compression successful!")
                self.log_status(f"Compressed size: {compressed_size:,} bytes")
                self.log_status(f"Space saved: {ratio:.2f}%")
                self.log_status("=" * 50)
                messagebox.showinfo(
                    "Success",
                    f"File compressed successfully!\nCompression ratio: {ratio:.2f}%"
                )
            else:
                self.log_status("✗ Compression failed!")
        except Exception as e:
            self.log_status(f"✗ Error during compression: {str(e)}")
            messagebox.showerror("Error", f"Compression failed: {str(e)}")

    def decompress_file(self):
        input_file = self.decompress_input_entry.get()
        output_file = self.decompress_output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist")
            return

        try:
            # ✅ Always use a fresh compressor instance
            compressor = HuffmanCompressor()

            self.log_status(f"Starting decompression...")
            self.log_status(f"File: {os.path.basename(input_file)}")
            self.log_status("-" * 50)

            # Run decompression
            success = compressor.decompress(input_file, output_file)

            if success:
                # The decompressor might change or append the extension automatically
                actual_output = output_file
                if not os.path.exists(actual_output):
                    # Try with added original extension
                    base, ext = os.path.splitext(output_file)
                    for f in os.listdir(os.path.dirname(output_file) or '.'):
                        if os.path.splitext(f)[0] == os.path.basename(base):
                            actual_output = os.path.join(os.path.dirname(output_file), f)
                            break

                if os.path.exists(actual_output):
                    decompressed_size = os.path.getsize(actual_output)
                    self.log_status(f"✓ Decompression successful!")
                    self.log_status(f"Output: {os.path.basename(actual_output)}")
                    self.log_status(f"Size: {decompressed_size:,} bytes")
                    self.log_status(f"Location: {actual_output}")
                    self.log_status("=" * 50)
                    messagebox.showinfo(
                        "Success",
                        f"File decompressed successfully!\n\nSaved as:\n"
                        f"{os.path.basename(actual_output)}\n\nLocation:\n{actual_output}"
                    )
                else:
                    self.log_status(f"✓ Decompression completed!")
                    self.log_status("=" * 50)
                    messagebox.showinfo("Success", "File decompressed successfully!")
            else:
                self.log_status("✗ Decompression failed!")
        except Exception as e:
            self.log_status(f"✗ Error during decompression: {str(e)}")
            messagebox.showerror("Error", f"Decompression failed:\n{str(e)}")

def decompress_file(self):
        input_file = self.decompress_input_entry.get()
        output_file = self.decompress_output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist")
            return

        try:
            # ✅ Always use a fresh compressor instance
            compressor = HuffmanCompressor()

            self.log_status(f"Starting decompression...")
            self.log_status(f"File: {os.path.basename(input_file)}")
            self.log_status("-" * 50)

            # Run decompression
            success = compressor.decompress(input_file, output_file)

            if success:
                # The decompressor might change or append the extension automatically
                actual_output = output_file
                if not os.path.exists(actual_output):
                    # Try with added original extension
                    base, ext = os.path.splitext(output_file)
                    for f in os.listdir(os.path.dirname(output_file) or '.'):
                        if os.path.splitext(f)[0] == os.path.basename(base):
                            actual_output = os.path.join(os.path.dirname(output_file), f)
                            break

                if os.path.exists(actual_output):
                    decompressed_size = os.path.getsize(actual_output)
                    self.log_status(f"✓ Decompression successful!")
                    self.log_status(f"Output: {os.path.basename(actual_output)}")
                    self.log_status(f"Size: {decompressed_size:,} bytes")
                    self.log_status(f"Location: {actual_output}")
                    self.log_status("=" * 50)
                    messagebox.showinfo(
                        "Success",
                        f"File decompressed successfully!\n\nSaved as:\n"
                        f"{os.path.basename(actual_output)}\n\nLocation:\n{actual_output}"
                    )
                else:
                    self.log_status(f"✓ Decompression completed!")
                    self.log_status("=" * 50)
                    messagebox.showinfo("Success", "File decompressed successfully!")
            else:
                self.log_status("✗ Decompression failed!")
        except Exception as e:
            self.log_status(f"✗ Error during decompression: {str(e)}")
            messagebox.showerror("Error", f"Decompression failed:\n{str(e)}")


def decompress_file(self):
        input_file = self.decompress_input_entry.get()
        output_file = self.decompress_output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist")
            return
        try:
            # ✅ Always use a fresh compressor instance
            compressor = HuffmanCompressor()

            self.log_status(f"Starting decompression...")
            self.log_status(f"File: {os.path.basename(input_file)}")
            self.log_status("-" * 50)

            # Run decompression
            success = compressor.decompress(input_file, output_file)

            if success:
                # The decompressor might change or append the extension automatically
                actual_output = output_file
                if not os.path.exists(actual_output):
                    # Try with added original extension
                    base, ext = os.path.splitext(output_file)
                    for f in os.listdir(os.path.dirname(output_file) or '.'):
                        if os.path.splitext(f)[0] == os.path.basename(base):
                            actual_output = os.path.join(os.path.dirname(output_file), f)
                            break

                if os.path.exists(actual_output):
                    decompressed_size = os.path.getsize(actual_output)
                    self.log_status(f"✓ Decompression successful!")
                    self.log_status(f"Output: {os.path.basename(actual_output)}")
                    self.log_status(f"Size: {decompressed_size:,} bytes")
                    self.log_status(f"Location: {actual_output}")
                    self.log_status("=" * 50)
                    messagebox.showinfo(
                        "Success",
                        f"File decompressed successfully!\n\nSaved as:\n"
                        f"{os.path.basename(actual_output)}\n\nLocation:\n{actual_output}"
                    )
                else:
                    self.log_status(f"✓ Decompression completed!")
                    self.log_status("=" * 50)
                    messagebox.showinfo("Success", "File decompressed successfully!")
            else:
                self.log_status("✗ Decompression failed!")
        except Exception as e:
            self.log_status(f"✗ Error during decompression: {str(e)}")
            messagebox.showerror("Error", f"Decompression failed:\n{str(e)}")


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()

