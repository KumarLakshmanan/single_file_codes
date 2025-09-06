import os
from selenium import webdriver
import time
from PIL import Image, ImageChops
import io

def main():
    browser = webdriver.Chrome()
    listofHtml = os.listdir('uiverse/html')
    
    for htmlFile in listofHtml:
       
        screenshot_folder = "uiverse/lightgif/"
        fileName = htmlFile.replace('.html', '') + ".gif"
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        screenshot_path = os.path.join(screenshot_folder, fileName)

        if not os.path.exists(screenshot_path):
            screenshot_path = os.path.join(screenshot_path)
            browser.get(os.path.abspath('uiverse/html/' + htmlFile))
            browser.set_window_size(600, 400)

            # Capture individual screenshots at a specified interval (e.g., 0.1 seconds)
            screenshot_images = []
            for _ in range(30):  # 3 seconds (30 frames at 0.1 seconds per frame)
                screenshot = browser.get_screenshot_as_png()
                screenshot_image = Image.open(io.BytesIO(screenshot))
                screenshot_images.append(screenshot_image)
                time.sleep(0.1)  # Adjust the interval as needed
            
            # Save the captured screenshots as a GIF
            screenshot_images[0].save(
                screenshot_path,
                save_all=True,
                append_images=screenshot_images[1:],
                duration=100,  # 100ms per frame (0.1 seconds)
                loop=0  # Infinite loop
            )

main()
