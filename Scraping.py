import requests
from bs4 import BeautifulSoup
import csv

counter = 1
scraping = True
with open("Extracted_data.csv", newline='', mode='w', encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, ["Author", "Book_Name", "Book_Category", "Book_url"])
    writer.writeheader()
    while scraping:
        request = requests.get("https://www.arab-books.com//page/{}".format(counter))
        if request.status_code == 404:
            scraping = False
            continue
        soup = BeautifulSoup(request.text)

        for book in soup.select("#posts-container > li"):
            book_name = None
            book_url = None
            if len(book.select("a[aria-label]")) > 0:
                book_url = book.select("a[aria-label]")[0]['href']
                book_name = book.select("a[aria-label]")[0]['aria-label']
            book_category = None
            if book_url is not None:
                try:
                    book_soup = BeautifulSoup(requests.get(book_url).text)
                    book_category = '-'.join([x.text for x in book_soup.select("div.entry-header > span.post-cat-wrap > a")])
                except Exception:
                    book_category = None
            # check if author data exist
            author = None
            if len(book.select("div.book-writer > a")) > 0:
                author = book.select("div.book-writer > a")[0].text
            writer.writerow({
                "Author": author,
                "Book_Name": book_name,
                "Book_Category": book_category,
                "Book_url": book_url
            })
        print(f"Page {counter} finished.....")
        counter += 1
