from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def ml_extract(url, headless):
    class_item = "ui-search-layout__item"
    class_title_card = (
        "//li[@class='ui-search-layout__item']//a[contains(@class, 'title')]"
    )
    class_amount = "//li[@class='ui-search-layout__item']//div[contains(@class, 'price__current')]//span[contains(@class, 'amount__fraction')]"

    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless")

    items = []

    with webdriver.Chrome(options=options) as driver:
        driver.implicitly_wait(5)
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_item))
        )

        list_title = [
            element.text for element in driver.find_elements(By.XPATH, class_title_card)
        ]

        list_amount = [
            element.text for element in driver.find_elements(By.XPATH, class_amount)
        ]

        list_url = [
            element.get_attribute("href")
            for element in driver.find_elements(By.XPATH, class_title_card)
        ]

        count = 0

        for title, amount, href in zip(list_title, list_amount, list_url):
            count += 1
            item = {
                "title": title,
                "price": amount,
                "url": href,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            items.append(item)

    return items
