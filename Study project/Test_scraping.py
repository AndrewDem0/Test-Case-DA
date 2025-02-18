import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

save_path_img = "C:/Resume/Test Case DA/Study project/Book_Images"
current_page = 1
data = []
prosed = True
when_to_stop = 20

while len(data) < when_to_stop and prosed:
    
    print("Page: "+str(current_page))
    
    url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"
    
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, "html.parser")
    
    if soup.title.text == "404 Not Found":
        prosed = False
    else:
        all_books = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book in all_books:
            if len(data) >= when_to_stop:
                break
            item = {}
            
            item["Title"] = book.find("img").attrs["alt"]
            item["Link"] =  "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
            item["Price"] = book.find("p", class_="price_color").text[2:]
            item["Stock"] = book.find("p", class_="instock availability").text.strip()
            
            name_img = book.find("h3").text
            link_img = "https://books.toscrape.com/catalogue/" + book.find("img").attrs["src"]
            
            sanitized_name = sanitize_filename(name_img.replace(' ', '-'))
            
            with open(os.path.join(save_path_img, sanitized_name + ".png"), "wb") as f:
                im = requests.get(link_img)
                f.write(im.content)
            data.append(item)
            
    current_page += 1
prosed = False
df = pd.DataFrame(data)

df.index = df.index + 1
df.index.name = "No"

df.to_excel("C:/Resume/Test Case DA/Study project/Exel table/Books.xlsx")