import requests
import json
import time
from bs4 import BeautifulSoup

totalPage = input("Total page: ")
totalPage = int(totalPage)
jsonValue = []
for page in range(1, totalPage + 1):
    url = 'https://tamilbookspdf.com/books/page/' + str(page) + '/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    items = soup.select('.item.books')
    for item in items:
        image = item.select('.poster img')[0]['src']
        link = item.select('.data h3 a')[0]['href']
        views = item.select('.dtinfo .metadata span')[0].text.replace(' views', '')
        title = item.select('.data h3 a')[0].text

        print(title)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'html.parser')
        description = soup.select('#info .wp-content > p')[0].text
        title = soup.select('#info .wp-content ul li:nth-child(1) b')[0].text
        author = soup.select('#info .wp-content ul li:nth-child(2) a')[0].text
        
        genre = []
        category = []
        pages = ""
        size =  ""
        liValue = soup.select('#info .wp-content ul li')
        for li in liValue:
            if 'Genre' in li.text:
                aValues = li.select('a')
                for a in aValues:
                    genre.append(a.text)
            if 'pages' in li.text:
                pages = li.text.replace('Total pages: ', '')
            if 'Size' in li.text:
                size = li.text.replace('PDF Size: ', '').replace(' Mb', '')
            if 'Category' in li.text:
                aValues = li.select('a')
                for a in aValues:
                    category.append(a.text)

        drivelink = []
        drivelinks = soup.select('#info .wp-content blockquote a')
        for x in drivelinks:
            if 'drive.google.com' in x['href']:
                drivelink.append(x['href'])
                
        # remove the duplicate values
        genre = list(dict.fromkeys(genre))
        category = list(dict.fromkeys(category))
        drivelink = list(dict.fromkeys(drivelink))

        jsonValue.append({
            'title': title,
            'author': author,
            'genre': genre,
            'category': category,
            'pages': pages,
            'size': size,
            'views': views,
            'image': image,
            'description': description,
            'drivelink': drivelink
        })
    time.sleep(3)
    with open('books_' + str(page) + '.json', 'w') as outfile:
        json.dump(jsonValue, outfile)

print('Done')
