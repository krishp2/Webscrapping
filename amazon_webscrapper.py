import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

url = "https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1685083765&sprefix=ba%2Caps%2C283&ref=sr_pg_2"
num_pages = 20


rows = []
for page in range(1, num_pages + 1):
    page_url = url.format(page)
    retry_count = 0
    while retry_count < 10:  
        try:
            response = requests.get(page_url)
            if response.status_code == 503:
                print("trying", page)
                time.sleep(2)  
                retry_count += 1
                continue

            response.raise_for_status()  
            time.sleep(1)  

            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", class_="sg-col-inner")

            for product in products:
                new_row = []  

                url_element = product.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
                if url_element:
                    product_url = "https://www.amazon.in" + url_element["href"]
                    new_row.append(product_url)

                    name_element = product.find("span", class_="a-size-medium a-color-base a-text-normal")
                    if name_element:
                        product_name = name_element.text.strip()
                        new_row.append(product_name)
                    else:
                        new_row.append("")  

                    price_element = product.find("span", class_="a-price-whole")
                    if price_element:
                        product_price = price_element.text.strip()
                        new_row.append(product_price)
                    else:
                        new_row.append("") 

                    rating_element = product.find("span", class_="a-icon-alt")
                    if rating_element:
                        product_rating = rating_element.text.strip()
                        new_row.append(product_rating)
                    else:
                        new_row.append("")  

                    reviews_element = product.find("span", class_="a-size-base s-underline-text")
                    if reviews_element:
                        product_reviews_count = reviews_element.text.strip()
                        new_row.append(product_reviews_count)
                    else:
                        new_row.append("")  

                    rows.append(new_row)  
            break  
        except requests.exceptions.HTTPError as err:
            print("HTTP error occurred:", err)
            retry_count += 1  
        except requests.exceptions.RequestException as err:
            print("An error occurred:", err)
            retry_count += 1  

df = pd.DataFrame(rows, columns=['Product URL', 'Product Name', 'Product Price', 'Rating','Number of reviews'])
df = pd.DataFrame(rows, columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
df = df.drop_duplicates(subset=['Product URL','Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
df = df.reset_index(drop=True)
df.to_csv("output_Final.csv")
