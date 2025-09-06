import os
import time
from selenium import webdriver

headers = {
    'Host': 'uiverse.io',
    'Referer': 'https://uiverse.io/all',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/80.0.3987.149 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
images = []


def main():
    browser = webdriver.Chrome()
    listofHtmlFiles = os.listdir('./uiverse/html/')
    time.sleep(5)
    for htmlFile in listofHtmlFiles:
        if htmlFile.endswith('.html'):
            with open('./uiverse/html/' + htmlFile, 'r', encoding='utf-8') as f:
                htmlContent = f.read()
                htmlContent = htmlContent.replace(
                    'html lang="en" style="padding: 0px;margin: 0px;">',
                    'html lang="en" style="padding: 0px;margin: 0px;overflow: hidden;">')
                htmlContent = htmlContent.replace(
                    'background-color: #212121; padding: 20px;display: flex;align-items: center;justify-content: center;height: 100vh;width: 100vw; padding: 0px; margin: 0px;', 'background-color: #e8e8e8; padding: 20px;display: flex;align-items: center;justify-content: center;height: 100vh;width: 100vw; padding: 0px; margin: 0px;overflow: hidden;')
            with open('./uiverse/html/' + htmlFile, 'w', encoding='utf-8') as f:
                f.write(htmlContent)

            browser.get(os.path.abspath('./uiverse/html/' + htmlFile))
            browser.set_window_size(600, 400)
            screenshot_path = "uiverse/light/" + htmlFile[:-5] + ".png" 
            browser.save_screenshot(screenshot_path)

main()
