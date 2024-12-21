import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True)
parser.add_argument("--headless", action="store_true")

args = parser.parse_args()

class_item = "ui-search-layout__item"
class_title_card = "poly-box.poly-component__title"
class_current_amount = "poly-price__current"
class_amount = "andes-money-amount__fraction"

options = webdriver.ChromeOptions()

if args.headless:
    options.add_argument("--headless")

with webdriver.Chrome(options=options) as driver:
    driver.implicitly_wait(15)
    driver.get(args.url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, class_item))
    )

    count = 0

    for item in driver.find_elements(By.CLASS_NAME, class_item):
        count += 1
        title = item.find_element(By.CLASS_NAME, class_title_card).text
        current_amount = item.find_element(By.CLASS_NAME, class_current_amount)
        amount = current_amount.find_element(By.CLASS_NAME, class_amount).text.replace(
            ",", ""
        )
        print(title)
        print(amount)
        print("-" * 8)

    print(f"{count} elementos")
