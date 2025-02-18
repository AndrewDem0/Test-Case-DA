import requests
from bs4 import BeautifulSoup
import os
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

save_path = "C:/Resume/Test Case DA/Study project/Book_Images"
current_page = 1
data = []
prosed = True
when_to_stop = 20
    
url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"
    
page = requests.get(url)
    
soup = BeautifulSoup(page.text, "html.parser")

all_books_img = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
for image in all_books_img:
    name = image.find("h3").text
    link = "https://books.toscrape.com/catalogue/" + image.find("img").attrs["src"]
    
    sanitized_name = sanitize_filename(name.replace(' ', '-'))
    
    with open(os.path.join(save_path, sanitized_name + ".png"), "wb") as f :
        im = requests.get(link)
        f.write(im.content)