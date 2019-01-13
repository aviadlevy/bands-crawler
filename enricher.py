import csv

import requests


def transform_row(row):
    if not row[1]:
        search_photos = requests.get("https://en.wikipedia.org/w/api.php", params={
            'action': 'query',
            'format': 'json',
            'prop': 'images',
            'titles': row[0]
        })
        try:
            pages = search_photos.json()['query']['pages']
            dict_key = list(pages.keys())[0]
            title = pages[dict_key]['images'][0]['title']
            for optional_title in pages[dict_key]['images']:
                if row[0] in optional_title['title']:
                    title = optional_title['title']
                    break
            url = requests.get("https://en.wikipedia.org/w/api.php", params={
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'imageinfo',
                'iiprop': 'url'
            })
            return [row[0], url.json()['query']['pages']['-1']['imageinfo'][0]['url']]
        except:
            print(row[0])
            return row
    return row


with open('bands.csv') as csv_in, open('bands_enriched.csv', 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(transform_row(row) for row in csv.reader(csv_in) if row)
