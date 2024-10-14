from typing import Self

from matplotlib import pyplot
import numpy as np
from PIL.Image import Image
import pyautogui
from pynput import keyboard
import pymonctl
import pywinctl


class Color:
    def __init__(self, red: float, green: float, blue: float):
        self.red = red
        self.green = green
        self.blue = blue

    def distance(self, other: Self) -> float:
        return abs(self.red - other.red) + abs(self.green - other.green) + abs(self.blue - other.blue)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'(x:{self.x}, y:{self.y})'


class GlobalPoint(Point):
    pass


class WindowPoint(Point):
    def __init__(self, x, y, window):
        super().__init__(x, y)
        self.window = window


def global_to_window_space(window: pywinctl.Window, point: GlobalPoint) -> WindowPoint:
    return WindowPoint(point.x - window.left, point.y - window.top, window)


def window_to_global_space(window: pywinctl.Window, point: WindowPoint) -> GlobalPoint:
    return GlobalPoint(point.x + window.left, point.y + window.top)


def is_point_in_window(window: pywinctl.Window, point: GlobalPoint) -> bool:
    return window.left <= point.x <= window.right and window.top <= point.y <= window.bottom


def print_windows():
    for window in pywinctl.getAllWindows():
        print(f"Window: [{window.title}] {window.size}")


def get_window_or_exit(name) -> pywinctl.Window:
    window = pywinctl.getWindowsWithTitle(name, condition=pywinctl.Re.CONTAINS, flags=pywinctl.Re.IGNORECASE)
    if window:
        window = window[0]
    else:
        print("No window found")
        exit(1)
    print(f"Target Window: [{window.title}] ({window.topleft}) {window.size}")
    return window


def screenshot_around_mouse() -> Image:
    mouse = pymonctl.getMousePos()
    rect_size = 20
    return pyautogui.screenshot(region=(mouse.x - rect_size // 2, mouse.y - rect_size // 2, rect_size, rect_size))


def screenshot_window(window=None, name=None) -> Image:
    if window is None and name:
        window = get_window_or_exit(name)
    # Define the region (left, top, width, height) for the screenshot
    x = window.topleft.x
    y = window.topleft.y
    width = window.width
    height = window.height

    # Take a screenshot of the defined region
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    return screenshot


def display_color(color: Color, ax: pyplot.Axes):
    # Create a plot of that color

    # Display the color
    ax.axis('off')
    ax.set_title(f'average color')
    ax.imshow([[[int(color.red), int(color.green), int(color.blue)]]], extent=[0, 1, 0, 1], vmin=0, vmax=255)


def average_color(nparray) -> Color:
    average_rgb = nparray.mean(axis=(0, 1))
    return Color(average_rgb[0], average_rgb[1], average_rgb[2])


def average_color_and_display(nparray):
    fig, (ax1, ax2) = pyplot.subplots(nrows=1, ncols=2)
    ax1.imshow(nparray)
    display_color(average_color(nparray), ax2)
    fig.show()
    pass


def subrect_of_img_size(img: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    return subrect_of_img(img, x, y, x+width, y+height)


def subrect_of_img(img: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> np.ndarray:
    return img[y1:y2, x1:x2]


TOP_LEFT = GlobalPoint(0, 0)
BOTTOM_RIGHT = GlobalPoint(0, 0)
LISTENER: keyboard.Listener = None
TARGET_WINDOW: pywinctl.Window = None


def on_press(key):
    global TOP_LEFT, BOTTOM_RIGHT, LISTENER
    if key == keyboard.Key.f7:
        # Mark top left
        x, y = pymonctl.getMousePos()
        TOP_LEFT = GlobalPoint(x, y)
    elif key == keyboard.Key.f8:
        # Mark top left
        x, y = pymonctl.getMousePos()
        BOTTOM_RIGHT = GlobalPoint(x, y)
        top_left = global_to_window_space(TARGET_WINDOW, TOP_LEFT)
        bottom_right = global_to_window_space(TARGET_WINDOW, BOTTOM_RIGHT)
        print(f'Top left: {top_left}, Bottom right: {bottom_right}')
    elif key == keyboard.Key.esc:
        LISTENER.stop()


def main():
    global LISTENER, TARGET_WINDOW

    print_windows()

    mouse_area = screenshot_around_mouse()
    mouse_array = np.array(mouse_area)
    average_color_and_display(mouse_array)

    TARGET_WINDOW = get_window_or_exit("TicketToRide")
    screenshot = screenshot_window(window=TARGET_WINDOW)
    window_array = np.array(screenshot)
    average_color_and_display(window_array)

    subimg = subrect_of_img(window_array, 606, 1190, 1258, 1329)
    average_color_and_display(subimg)

    LISTENER = keyboard.Listener(on_press=on_press)
    LISTENER.start()
    LISTENER.wait()
    print('Press F7 to mark top left, F8 to mark bottom right')

    pyplot.show()
    print('Press ESC to exit')
    LISTENER.join()


if __name__ == "__main__":
    main()