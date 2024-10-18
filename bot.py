import queue
import tkinter as tk
from threading import Thread
from tkinter import ttk

import PIL.Image
import PIL.ImageTk
from pynput import keyboard
import pymonctl
import pywinctl

import bot.window_interface_helpers as win
from bot.window_interface_helpers import is_point_in_window
from view_elements.scroll_list import ScrollList


TARGET_WINDOW: pywinctl.Window|None = None


class WindowChooser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ticket To Ride bot")
        self.geometry("400x400")

        ttk.Label(text="Choose your window", padding=10).pack(side=tk.TOP, fill=tk.X)
        tk.Button(text="Select", padx=10, pady=10, background='lightblue', command=self.set_target_window).pack(side=tk.BOTTOM, fill=tk.X)
        chooser_frame = tk.Frame(self)
        self.window_options = win.get_windows()
        self.chooser = ScrollList(chooser_frame)
        chooser_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        for window in self.window_options:
            self.chooser.list_view.insert('end', window.title)

    def set_target_window(self):
        global TARGET_WINDOW
        selected = self.chooser.list_view.curselection()
        TARGET_WINDOW = self.window_options[selected[0]]
        self.destroy()


class Bot(tk.Tk):
    def __init__(self, window: pywinctl.Window):
        super().__init__()
        self.title("Ticket To Ride bot")
        self.geometry("800x800")

        self.top_left = win.GlobalPoint(0, 0)
        self.bottom_right = win.GlobalPoint(0, 0)
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.target_window = window

        self.listener.start()
        self.listener.wait()

        print('Press F7 to mark top left, F8 to mark bottom right')
        print('Press ESC to exit')
        self.bind_all("<Escape>", self.escape_key)

        self.image_queue: queue.Queue[PIL.Image.Image] = queue.Queue()
        self.image_frame = tk.Frame(self, bg='lightblue', padx=10, pady=10)
        self.image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.key_bindings_frame = ttk.LabelFrame(text='Key bindings', height=4)
        self.key_bindings_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        ttk.Label(self.key_bindings_frame, text='Exit: ESC').grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.key_bindings_frame, text='Mark rectangle top-left: F7').grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.key_bindings_frame, text='Mark rectangle bottom-right and print rectangle: F8').grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.key_bindings_frame, text='Mark point and print point: F10').grid(row=3, column=0, sticky=tk.W)
        self.after(200, self.poll_for_new_image_to_render)

    def poll_for_new_image_to_render(self):
        try:
            item: PIL.Image.Image = self.image_queue.get_nowait()
            size = self.resize_image_for_constraints(
                item,
                win.Size(self.image_frame.winfo_width(), self.image_frame.winfo_height() - 20), # -20 for 10 padding
            )
            for widget in self.image_frame.winfo_children():
                widget.destroy()
            resized = item.resize((size.width, size.height))
            imtk = PIL.ImageTk.PhotoImage(resized)
            img = tk.Label(self.image_frame, image=imtk, borderwidth=0)
            img.image = imtk
            img.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        except queue.Empty:
            pass
        finally:
            self.after(200, self.poll_for_new_image_to_render)

    @staticmethod
    def resize_image_for_constraints(image: PIL.Image.Image, constraints: win.Size) -> win.Size:
        # Find the constraining dimension. Ex: a vertical video playing on a wide screen. The video has a low aspect
        # ratio than the screen. As a result, the Y dimension is constraining. Otherwise, X constrains.
        image_aspect_ratio = image.width / image.height
        constraints_aspect_ratio = constraints.width / constraints.height
        if image_aspect_ratio > constraints_aspect_ratio:
            # Image is "wider" than the screen, we need to fit the width in the screen and make the height match.
            width = constraints.width
            height = width / image_aspect_ratio
            return win.Size(width, int(height))
        else:
            # Image is "taller" than the screen, we need to fit the height in the screen and make the width match.
            height = constraints.height
            width = height * image_aspect_ratio
            return win.Size(int(width), height)


    def escape_key(self, _):
        self.quit()

    def quit(self):
        self.destroy()

    def on_press(self, key):
        if key == keyboard.Key.f7:
            # Mark top left
            point = win.GlobalPoint(*pymonctl.getMousePos())
            if is_point_in_window(self.target_window, point):
                self.top_left = win.global_to_window_space(self.target_window, point)
            else:
                print(f'Point must be in window')
        elif key == keyboard.Key.f8:
            # Mark bottom right
            point = win.GlobalPoint(*pymonctl.getMousePos())
            if not is_point_in_window(self.target_window, point):
                print(f'Point must be in window')
                return
            self.bottom_right = win.global_to_window_space(self.target_window, point)
            if self.bottom_right.x <= self.top_left.x or self.bottom_right.y <= self.top_left.y:
                print(f'Rectangle points invalid')
                return
            print(f'Top left: {self.top_left}, Bottom right: {self.bottom_right}')
            rect = win.Rectangle(self.top_left, self.bottom_right)
            screenshot = win.screenshot_rect(rect)
            self.image_queue.put(screenshot)
        elif key == keyboard.Key.f10:
            point = win.global_to_window_space(self.target_window, win.GlobalPoint(*pymonctl.getMousePos()))
            screenshot = win.screenshot_around_mouse()
            self.image_queue.put(screenshot)
            print(f'{point}')
        elif key == keyboard.Key.esc:
            self.listener.stop()
            self.destroy()


def main():
    win.print_windows()
    window_chooser = WindowChooser()
    window_chooser.mainloop()
    app = Bot(TARGET_WINDOW)
    app.mainloop()

    Thread(target=app.listener.stop).start()


if __name__ == "__main__":
    main()