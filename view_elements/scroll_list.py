import tkinter as tk
from tkinter import ttk


class ScrollList:
    def __init__(self, container):
        # Create a listbox with a scrollbar
        self.scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_view = tk.Listbox(container, bg='light grey', yscrollcommand=self.scrollbar.set)
        self.list_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.list_view.yview)
