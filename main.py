import os
import sys
import io
import contextlib
import tkinter as tk
from tkinter import messagebox
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

def run(code):
    tokens = tokenize(code)
    tree = Parser(tokens).parse()
    Interpreter().eval(tree)

def run_with_output(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run(code)
    return buf.getvalue()

def list_programs():
    prog_dir = r"c:/Users/Elyas/Desktop/Pl_project/programs"
    files = sorted([f for f in os.listdir(prog_dir) if os.path.isfile(os.path.join(prog_dir, f))])
    return prog_dir, files

def gui_main():
    prog_dir, files = list_programs()
    
    root = tk.Tk()
    root.title("Program Runner")
    
    # Left frame: List of available programs
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    tk.Label(left_frame, text="Available Programs:").pack()
    listbox = tk.Listbox(left_frame, width=40, height=15)
    listbox.pack(fill=tk.BOTH, expand=True)
    for f in files:
        listbox.insert(tk.END, f)
    
    # Right frame: Output of the executed program
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    tk.Label(right_frame, text="Program Output:").pack()
    output_text = tk.Text(right_frame, width=60, height=20)
    output_text.pack(fill=tk.BOTH, expand=True)
    
    def run_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a program from the list.")
            return
        index = selection[0]
        filename = listbox.get(index)
        file_path = os.path.join(prog_dir, filename)
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                code = f.read()
            output = run_with_output(code)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Control buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=5)
    run_button = tk.Button(button_frame, text="Run Program", command=run_selected)
    run_button.pack(side=tk.LEFT, padx=5)
    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)
    exit_button.pack(side=tk.RIGHT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    gui_main()