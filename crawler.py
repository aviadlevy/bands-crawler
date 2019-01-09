import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


def main():
    bands_img_dicts = []
    with urlopen('https://www.britannica.com/topic/list-of-bands-2026814') as con:
        res = con.read().decode('utf8')
    soup = BeautifulSoup(res, features='html.parser')
    for band in soup.find('article', {'id': 'article-content'}).find_all('li'):
        with urlopen(band.find('a', href=True)['href']) as con:
            res = con.read().decode('utf-8')
            inner_soup = BeautifulSoup(res, features='html.parser')
            img = ''
            try:
                img = inner_soup.find('div', {'class': 'fact-box-picture'}).find('img')['src']
            except:
                try:
                    inner_soup.find('article', {'id': 'article-content'}).find('img')['src']
                except:
                    print(band.text)
            bands_img_dicts.append({'band': band.text, 'img': img})

    with open('bands.csv', 'w', newline='') as f:
        fieldnames = ['band', 'img']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bands_img_dicts)


if __name__ == '__main__':
    main()
