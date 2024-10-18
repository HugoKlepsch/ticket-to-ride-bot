from typing import Self, List
from matplotlib import pyplot
import numpy as np
from PIL.Image import Image
import pyautogui
import pymonctl
import pywinctl


class Color:
    def __init__(self, red: float, green: float, blue: float):
        for var, name in ((red, 'red'), (green, 'green'), (blue, 'blue')):
            if var < 0 or var > 255:
                raise ValueError(f"{name} must be between 0 and 255")
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

    def xy_tuple(self) -> tuple:
        return self.x, self.y


class GlobalPoint(Point):
    pass


class WindowPoint(Point):
    def __init__(self, x, y, window):
        super().__init__(x, y)
        self.window: pywinctl.Window = window

    def global_point(self) -> GlobalPoint:
        return GlobalPoint(self.x + self.window.left, self.y + self.window.top)


class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def __repr__(self):
        return f'(top left:{self.top_left}, bottom right:{self.bottom_right})'

    @property
    def width(self):
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self):
        return self.bottom_right.y - self.top_left.y


class Size:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __repr__(self):
        return f'(width:{self.width}, height:{self.height})'


def global_to_window_space(window: pywinctl.Window, point: GlobalPoint) -> WindowPoint:
    return WindowPoint(point.x - window.left, point.y - window.top, window)


def window_to_global_space(window: pywinctl.Window, point: WindowPoint) -> GlobalPoint:
    return GlobalPoint(point.x + window.left, point.y + window.top)


def is_point_in_window(window: pywinctl.Window, point: GlobalPoint) -> bool:
    return window.left <= point.x <= window.right and window.top <= point.y <= window.bottom


def get_windows() -> List[pywinctl.Window]:
    return pywinctl.getAllWindows()


def print_windows():
    for window in get_windows():
        print(f"Window: [{window.title}] {window.size}")


def get_window(name) -> pywinctl.Window | None:
    window = pywinctl.getWindowsWithTitle(name, condition=pywinctl.Re.CONTAINS, flags=pywinctl.Re.IGNORECASE)
    if window:
        window = window[0]
        print(f"Target Window: [{window.title}] {window.topleft} {window.size}")
        return window
    return None


def screenshot_around_mouse() -> Image:
    mouse = pymonctl.getMousePos()
    rect_size = 20
    return pyautogui.screenshot(region=(mouse.x - rect_size // 2, mouse.y - rect_size // 2, rect_size, rect_size))


def screenshot_window(window=None, name=None) -> Image:
    if window is None and name:
        window = get_window(name)
    # Define the region (left, top, width, height) for the screenshot
    x = window.topleft.x
    y = window.topleft.y
    width = window.width
    height = window.height

    # Take a screenshot of the defined region
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    return screenshot


def screenshot_rect(rect: Rectangle) -> Image:
    # Define the region (left, top, width, height) for the screenshot
    top_left = rect.top_left
    if isinstance(top_left, WindowPoint):
        top_left = top_left.global_point()
    x = top_left.x
    y = top_left.y
    width = rect.width
    height = rect.height

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
