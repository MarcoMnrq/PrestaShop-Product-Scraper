# Library Imports
from selenium import webdriver

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
WELCOME_MSG = "[———————————————————————————————————————]\nPrestaShop Product Scraper Tool\nAuthor: @MarcoMnrq\n"


def main():
    print(WELCOME_MSG)
    RUNNING = True
    while RUNNING:
        print("1. PrestaShop Website")
        print("0. Exit program")
        print("[———————————————————————————————————————]\n")
        SELECTION = int(input("[•] Select an option: "))
        if SELECTION == 1:
            # PrestaShop Website
            TOOL_URL = input("[•] Url to scrape: ")
            browser = webdriver.Chrome(DRIVER_PATH)
            browser.get(TOOL_URL)
            if browser.
            productTitle = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div/h2').text
            productPrice = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div[4]/div[1]/div[2]/div/div[1]/div/ins').text
            print("Product title: ", productTitle)
            print("Price: ", productPrice)
        elif SELECTION == 2:
            # Linio Website
            print("TODO")
        elif SELECTION == 0:
            RUNNING = False
        print("\n\n\n")
    print("[•] Thank you for using this tool. Goodbye!")


main()
