import tkinter as tk
import random
from tkinter import ttk


class ScrollList:
    def __init__(self, container):
        # Create a listbox with a scrollbar
        self.scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_view = tk.Listbox(container, bg='light grey', yscrollcommand=self.scrollbar.set)
        self.list_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.list_view.yview)


class Configurator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My First GUI")
        self.geometry("400x400")

        # Create top label
        top_label = tk.Label(self, text="Top Fixed Size Label", bg="lightgreen", height=2)
        top_label.pack(side=tk.TOP, fill=tk.X)

        # Create bottom label
        b_frame = tk.Frame(self, bg="lightblue")
        b_frame.pack(side=tk.BOTTOM, fill=tk.X)
        bottom_label = tk.Label(b_frame, text="Bottom Fixed Size Label", bg="lightblue", height=2)
        bottom_label.pack(side=tk.TOP, fill=tk.BOTH)

        # Create expandable middle area
        m_frame = tk.Frame(self, bg="lightgrey")
        m_frame.pack(fill=tk.BOTH, expand=True)

        # left side list area
        l_frame = tk.Frame(m_frame)
        l_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollList = ScrollList(l_frame)

        # right side area
        r_frame = tk.Frame(m_frame)
        r_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.layout_right(r_frame)

    def layout_right(self, container):
        add_button = ttk.Button(container, text="Add", command=self.add_clicked)
        add_button.pack()

        remove_button = ttk.Button(container, text="Remove", command=self.remove_clicked)
        remove_button.pack()

    def layout_bottom(self, container):
        label = ttk.Label(container, text="Status", relief=tk.SUNKEN)
        label.pack()

    def add_clicked(self):
        print("Add clicked")
        self.scrollList.list_view.insert(tk.END, f"Hello, World! {random.randint(0, 100)}")

    def remove_clicked(self):
        print("Remove clicked")
        self.scrollList.list_view.delete(self.scrollList.list_view.curselection())
        self.scrollList.list_view.selection_set(0)


class Testing(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Example")
        self.geometry("300x200")

        # Create a Notebook widget
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create frames for each tab
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)

        # Add frames to the Notebook
        notebook.add(tab1, text='Tab 1')
        notebook.add(tab2, text='Tab 2')
        notebook.add(tab3, text='Tab 3')

        # Populate Tab 1
        label1 = tk.Label(tab1, text="This is Tab 1", font=("Arial", 16))
        label1.pack(pady=20)

        entry1 = tk.Entry(tab1)
        entry1.pack(pady=10)

        button1 = tk.Button(tab1, text="Submit", command=lambda: print("Tab 1 Button Clicked"))
        button1.pack(pady=10)

        # Populate Tab 2
        label2 = tk.Label(tab2, text="This is Tab 2", font=("Arial", 16))
        label2.pack(pady=20)

        button2 = tk.Button(tab2, text="Click Me", command=lambda: print("Tab 2 Button Clicked"))
        button2.pack(pady=10)

        # Populate Tab 3
        label3 = tk.Label(tab3, text="This is Tab 3", font=("Arial", 16))
        label3.pack(pady=20)

        checkbox = tk.Checkbutton(tab3, text="Check me!")
        checkbox.pack(pady=10)

        # Bind the Escape key to a function
        self.bind_all("<Escape>", lambda _: self.destroy())


if __name__ == "__main__":
    app = Configurator()
    # app = Testing()
    app.mainloop()
