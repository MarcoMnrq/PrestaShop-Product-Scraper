# Library Imports
from selenium import webdriver

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
WELCOME_MSG = "[———————————————————————————————————————]\nPrestaShop Product Extractor Tool\nAuthor: @MarcoMnrq\n"
TOOL_URL = "https://www.google.com"


def main():
    print(WELCOME_MSG)
    TOOL_URL = input("Url to scrape: ")
    browser = webdriver.Chrome(DRIVER_PATH)
    browser.get(TOOL_URL)
    search = browser.find_element_by_class_name("product-name").get_attribute("h2")
    print(search)


main()
