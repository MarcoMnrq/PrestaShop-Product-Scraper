# Library Imports
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
WELCOME_MSG = "[———————————————————————————————————————]\nPrestaShop Product Scraper Tool\nAuthor: @MarcoMnrq\n"
browser = webdriver.Chrome(DRIVER_PATH)
browser.maximize_window()


def main():
    print(WELCOME_MSG)
    RUNNING = True
    browser.get("https://tienda.telwareperu.com/admin587ufuvum")
    browser.find_element_by_xpath('//*[@id="email"]').send_keys("manriqueacham@gmail.com")
    browser.find_element_by_xpath('//*[@id="passwd"]').send_keys("T1d1l1mfEZ#bFrpsr&11A8N&E")
    browser.find_element_by_xpath('//*[@id="submit_login"]').click()
    time.sleep(9)
    browser.find_element_by_xpath('//*[@id="subtab-AdminCatalog"]/a').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="subtab-AdminProducts"]/a').click()
    time.sleep(4)
    browser.find_element_by_xpath('//*[@id="page-header-desc-configuration-add"]').click()
    adminUrl = browser.current_url
    print(adminUrl)
    while RUNNING:
        print("1. PrestaShop Website")
        print("2. Linio Website")
        print("0. Exit program")
        print("[———————————————————————————————————————]\n")
        SELECTION = int(input("[•] Select an option: "))
        adminUrl = browser.current_url
        if SELECTION == 1:
            # PrestaShop Website
            TOOL_URL = input("[•] Url to scrape: ")
            browser.get(TOOL_URL)
            productTitle = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div/h2').text
            productPrice = browser.find_element_by_xpath(
                '//*[@id="main"]/div[2]/div[4]/div[1]/div[2]/div/div[1]/div/ins').send_keys(productPrice[3:])
            print("TITLE: ", productTitle)
            print("PRICE: ", productPrice)
        elif SELECTION == 2:
            # Linio Website
            TOOL_URL = input("[•] Url to scrape: ")
            browser.get(TOOL_URL)

            browser.find_element_by_xpath('//*[@id="panel-features"]/h2').click()
            productTitle = browser.find_element_by_xpath('//*[@id="display-zoom"]/div[1]/h1/span').text
            productPrice = browser.find_element_by_class_name("price-main-md").text
            productSummary = browser.find_element_by_xpath('//*[@id="panel-features"]/div[2]/div[2]/div/div').text

            browser.find_element_by_xpath('//*[@id="panel-details"]/h2').click()
            productSku = browser.find_element_by_xpath('//*[@id="panel-details"]/div[2]/div[2]/div[1]/div[2]').text
            productDesc = browser.find_element_by_xpath('//*[@id="panel-details"]/div[2]/div[3]').text
            print("============ DETAILS ============")
            print("[•] TITULO: ", productTitle)
            print("[•] PRECIO: ", productPrice)
            print("[•] SKU: ", productSku, "\n")
            print("============ SUMMARY ============\n", productSummary, "\n\n")
            print("============ DESCRIPTION ============\n", productDesc)

            # Image downloader
            gallery = browser.find_element_by_class_name("gallery-container")
            pictures = gallery.find_elements_by_tag_name("li")
            contador = 1
            print("\n\n")
            for picture in pictures:
                picture = picture.find_element_by_class_name("image-wrapper")
                sources = picture.find_elements_by_tag_name("source")
                pictureUrl = sources[1].get_attribute("srcset")
                pictureUrl = "https://" + pictureUrl[2:]
                print("IMAGEN ", contador, ": ", pictureUrl)
                contador = contador + 1

            # Admin product fill form
            browser.get(adminUrl)
            browser.find_element_by_xpath('//*[@id="form_step1_price_ttc_shortcut"]').send_keys(productPrice[3:])
            # Fill Text
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="mce_13"]/button').click()
            browser.find_element_by_id("mce_56").send_keys(productSummary)
            browser.find_element_by_id("mce_58").click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="tab_description"]/a').click()
            browser.find_element_by_xpath('//*[@id="mce_33"]/button').click()
            browser.find_element_by_id("mce_63").send_keys(productDesc)
            browser.find_element_by_id("mce_65").click()
            browser.find_element_by_id("form_step6_reference").send_keys(productSku)

            browser.find_element_by_xpath('//*[@id="tab_step3"]/a').click()
            browser.find_element_by_id("form_step3_out_of_stock_1").click()
            browser.find_element_by_xpath('//*[@id="tab_step1"]/a').click()

            browser.find_element_by_id("form_step1_name_1").send_keys(productTitle)

        elif SELECTION == 0:
            RUNNING = False
            browser.close()
        print("\n\n\n")
    print("[•] Thank you for using this tool. Goodbye!")


main()
