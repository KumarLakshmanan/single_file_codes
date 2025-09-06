import os
from selenium import webdriver
import json
import requests
import json
import requests
import time

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
    pageNo = 1
    while True:
        url = 'https://uiverse.io/all?page={}&_data=routes%2F%24category'.format(
            pageNo)
        response = requests.get(url, headers=headers)
        jsonData1 = response.json()
        posts = jsonData1['posts']
        for item in posts:
            if (os.path.exists('uiverse/html/' + item['id'] + '.html') == False):
                url = 'https://uiverse.io/{}/{}?_data=routes%2F%24username.%24friendlyId'.format(
                    item['user']['username'], item['friendlyId'])
                print(url)
                response = requests.get(url, headers=headers)
                jsonData = response.json()

                avatar = jsonData['post']['user']['avatar_url']
                # download the avatar
                avatarResponse = requests.get(avatar)
                avatarFileName = './uiverse/avatar/' + \
                    jsonData['post']['user']['username'] + '.png'
                with open(avatarFileName, 'wb') as f:
                    f.write(avatarResponse.content)

                htmlFile = 'uiverse/html/' + \
                    jsonData['post']['id'] + '.html'
                htmlContent = '''<!DOCTYPE html>
<html lang="en" style="padding: 0px;margin: 0px;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body style="background-color: #e8e8e8; padding: 20px;display: flex;align-items: center;justify-content: center;height: 100vh;width: 100vw; padding: 0px; margin: 0px;">
'''
                htmlContent += jsonData['post']['html']
                htmlContent += '</div><style>' + \
                    jsonData['post']['css'] + '</style>'
                htmlContent += '''</body></html>'''
                with open(htmlFile, 'w', encoding='utf-8') as f:
                    f.write(htmlContent)

                browser.get(os.path.abspath(htmlFile))
                browser.set_window_size(600, 400)
                screenshot_path = "uiverse/screenshot/" + \
                    jsonData['post']['id'] + ".png"
                browser.save_screenshot(screenshot_path)
                tailwind = 0
                if (jsonData['post']['isTailwind'] == True):
                    tailwind = 1
                data = {
                    'slug': jsonData['post']['id'],
                    'background': jsonData['post']['backgroundColor'],
                    'tailwind': tailwind,
                    'html': jsonData['post']['html'],
                    'css': jsonData['post']['css'],
                    'theme': jsonData['post']['theme'],
                    'type': jsonData['post']['type'],
                    'prefixcss': jsonData['post']['prefixedCss'],
                    'views': jsonData['post']['viewCount'],
                    'likes': jsonData['post']['_count']['user_favorite_post'],
                    'created_at': jsonData['post']['createdDate'],
                    "tags": ','.join(jsonData['post']['post_tag']),
                    'username': jsonData['post']['user']['username'],
                    'name': jsonData['post']['user']['name'],
                    'avatar': jsonData['post']['user']['username'] + '.png',
                    'thumb':  jsonData['post']['id'] + ".png"
                }
                response = requests.post(
                    'https://frontendforever.com/api/uiverse.php', data=data)
                print(response.text)
            else:
                print('skip ' + item['id'])

        if (jsonData1['hasNextPage'] == False):
            break
        pageNo += 1


main()
