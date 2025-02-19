import time
import requests
import pandas as pd
import os
import re

def sanitize_filename(filename):
    return re.sub(r'[\/*?:"<>|]', "", filename)

def download_image(image_url, title, save_path_img):
    if image_url:
        sanitized_name = sanitize_filename(title.replace(' ', '-'))
        img_path = os.path.join(save_path_img, sanitized_name + ".png")
        
        img_data = requests.get(image_url)
        if img_data.status_code == 200:
            with open(img_path, "wb") as f:
                f.write(img_data.content)
            print(f"Image {sanitized_name} downloaded successfully.")
        else:
            print(f"Failed to download image {sanitized_name}. Status code: {img_data.status_code}")

# Шлях для збереження файлів
save_path_xlsx = "C:/Resume/Test Case DA/junior_analyst_тестове_2/Exel table"
save_path_img = "C:/Resume/Test Case DA/junior_analyst_тестове_2/Images"
os.makedirs(save_path_xlsx, exist_ok=True)
os.makedirs(save_path_img, exist_ok=True)

# API-запит для отримання даних
url = "https://zbcpkxr8me-dsn.algolia.net/1/indexes/shopify_prod_products_international_en"
params = {
    "x-algolia-api-key": "3dacc900abf92f86aea111e187796ff3",
    "x-algolia-application-id": "ZBCPKXR8ME",
    "query": "",
    "page": 0,
    "hitsPerPage": 100,
    "facetFilters": "[\"collections:fragrances\"]"
}

response = requests.get(url, params=params)
data = response.json()["hits"]

# Обробка та форматування отриманих даних
items = []
for item in data:
    
    print("On the product №: " + str((len(items)) + 1))
    
    item_dict = {}
    
    item_dict["URL"] = f"https://smets.lu/products/{item.get('handle')}"
    item_dict["Brand"] = item.get("vendor")
    item_dict["Name"] = item.get("title")
    item_dict["Price"] = item.get("price")
    
    # Завантаження та збереження зображень
    download_image(item.get("product_image"), f"{item_dict["Brand"]}_{item_dict["Name"]}", save_path_img)
    
    items.append(item_dict)
    
    time.sleep(1.5)

df = pd.DataFrame(items)

excel_path = os.path.join(save_path_xlsx, sanitize_filename("Table.xlsx"))
df.to_excel(excel_path, index=False)