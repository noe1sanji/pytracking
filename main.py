import argparse
import os
import sys
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers import save_status
from tracking import price_tracking

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True)
parser.add_argument("--headless", action="store_true")
parser.add_argument("--cache", help="directory")

args = parser.parse_args()

if args.cache and not os.path.isdir(args.cache):
    print(f"directory {args.cache_directory} not found...")
    sys.exit(1)

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
    items = {}

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
        items[title] = {
            "price": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        price_tracking(title, amount)

    print(f"{count} elementos")
    tracking_file = os.path.join(args.cache, "items.json")
    save_status(tracking_file, items)
