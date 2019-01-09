import csv
import os

import pypexels
py_pexel = pypexels.PyPexels(api_key=os.environ['PEXELS_API_KEY'])


def transform_row(row):
    if not row[1]:
        search_photos = py_pexel.search(query=row[0], per_page=1)
        try:
            return [row[0], next(search_photos.entries).src['medium']]
        except:
            return row
    return row


with open('bands.csv') as csv_in, open('bands_enriched.csv', 'w') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(transform_row(row) for row in csv.reader(csv_in))


