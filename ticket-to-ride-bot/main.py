import pyautogui

# Define the region (left, top, width, height) for the screenshot
x = 100
y = 100
width = 500
height = 300

# Take a screenshot of the defined region
screenshot = pyautogui.screenshot(region=(x, y, width, height))

# Save the screenshot with the name 'region_screenshot.png' in the current directory
screenshot.save('region_screenshot.png')

print("Screenshot of a specific region taken and saved as 'region_screenshot.png'")
