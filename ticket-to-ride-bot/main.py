from collections import namedtuple

from matplotlib import pyplot
import numpy as np
from PIL.Image import Image
import pyautogui
import pymonctl
import pywinctl


Color = namedtuple('Color', ['red', 'green', 'blue'])


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


def screenshot_window(name) -> Image:
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


def main():
    print_windows()
    mouse_area = screenshot_around_mouse()
    mouse_array = np.array(mouse_area)
    average_color_and_display(mouse_array)
    screenshot = screenshot_window("tk")
    # Convert it into an array
    rgb_array = np.array(screenshot)
    average_color_and_display(rgb_array)

    pyplot.show()


if __name__ == "__main__":
    main()