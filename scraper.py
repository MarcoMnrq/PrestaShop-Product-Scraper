import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
WELCOME_MSG = "[———————————————————————————————————————]\nPrestaShop Product Scraper Tool\nAuthor: @MarcoMnrq\n"
browser = webdriver.Chrome(DRIVER_PATH)
browser.minimize_window()
browser.maximize_window()

default_title = "Titulo"
default_price = "999.9"
default_sku = "999999"
default_brand = "Telware"
default_summary = "Resumen de producto"
default_description = "Description de producto"
default_categories = "Web Cams,Accesorios,Inicio"


def save_to_file(file_name, active, title, price, sku, brand, summary, description, images):
    row = [
        1,  # ID
        active,  # Activo (0/1)
        title,  # Nombre
        default_categories,  # Categorías (x,y,z...)
        price,  # Precio impuestos INCLUIDOS
        1,  # ID regla de impuestos
        '',  # Precio de coste
        0,  # En oferta (0/1)
        '',  # Valor del descuento
        '',  # Porcentaje de descuento
        '',  # Descuento desde (aaaa-mm-dd)
        '',  # Descuento hasta (aaaa-mm-dd)
        sku,  # Referencia nº
        '',  # N° de referencia proveedor
        '',  # Proveedor
        brand,  # Marca
        '',  # EAN13
        '',  # UPC
        '',  # MPN
        '',  # Ecotasa
        '',  # Anchura
        '',  # Altura
        '',  # Profundidad
        '',  # Peso
        '',  # Plazo de entrega para los productos en stock:
        '',  # Plazo de entrega para los productos fuera de stock que se permiten comprar:
        0,  # Cantidad
        '',  # Cantidad mínima
        '',  # Nivel de stock bajo
        '',  # Envíame un mensaje de correo electrónico cuando la cantidad esté por debajo de este nivel
        '',  # Visible en
        '',  # Coste adicional del envío
        '',  # Unidad para el precio unitario
        '',  # Precio unitario
        summary,  # Resumen
        description,  # Descripción
        '',  # Etiquetas (x,y,z...)
        '',  # Meta-título
        '',  # Meta keywords
        '',  # Meta descripción
        '',  # URL reescrita
        '',  # Etiqueta cuando se encuentra en stock
        '',  # Etiqueta para cuando se permiten pedidos en espera
        '',  # Disponible para pedidos (0 = No, 1 = Si)
        '',  # Fecha de disponibilidad del producto
        '',  # Fecha de creación del producto
        1,  # Mostrar Precio (0 = No, 1 = Si)
        images,  # URL's de las imágenes (x,y,z...)
        '',  # Textos alternativos de imagen (x,y,z...)
        '',  # Elimine las imágenes existentes (0 = No, 1 = Si)
        '',  # Característica (Nombre:Valor:Posición:Personalizado)
        '',  # Solo disponible por Internet (0 = No, 1 = Si)
        'new',  # Estado
        0,  # Personalizable (0 = No, 1 = Sí)
        0,  # Se pueden subir archivos (0 = No, 1 = Sí)
        '',  # Campos de texto (0 = No, 1 = Sí)
        1,  # Acción cuando no haya existencias de stock
        0,  # Producto virtual (0 = No, 1 = Sí)
        '',  # URL de archivo
        '',  # Número de descargas permitidas
        '',  # Fecha de expiración (dd-mm-aaaa)
        '',  # Número de días
        '',  # ID / Nombre de la tienda
        '',  # Administración Avanzada de Stock
        '',  # Dependiendo del stock
        '',  # Almacén
        '',  # Accesorios (x,y,z...)
    ]
    # writing to csv file
    with open(file_name, 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(row)


def print_product(title, price, brand, sku, summary, desc):
    print("============ DETAILS ============")
    print("[•] TITULO:", title)
    print("[•] PRECIO:", price)
    print("[•] BRAND:", brand)
    print("[•] SKU:", sku, "\n")
    print("============ SUMMARY ============\n", summary, "\n\n")
    print("============ DESCRIPTION ============\n", desc)

def scrape_yamoshi(tool_url):
    # Open URL
    browser.get(tool_url)

    # Scraping title, price, etc...
    skip_product = False
    try:
        # Title
        title = browser.find_element_by_xpath('//*[@id="muestra"]/div[2]/h1').text
    except NoSuchElementException:
        title = default_title
    try:
        # Price
        price = browser.find_element_by_xpath('//*[@id="muestra"]/div[2]/div[2]/div[3]/div[1]/div/ul[2]/li[2]/span').text
    except NoSuchElementException:
        price = default_price
        input("[!] Element price not found...")
    try:
        # Brand
        brand = browser.find_element_by_xpath('//*[@id="muestra"]/div[2]/div[2]/div[1]/p[1]').text
        brand = default_brand
    except NoSuchElementException:
        brand = default_brand
        # input("[!] Element brand not found...")
    try:
        # Summary
        summary = browser.find_element_by_xpath('//*[@id="muestra"]/div[2]/div[2]/div[1]').text
    except NoSuchElementException:
        summary = default_summary
        input("[!] Element summary not found...")
    try:
        # SKU / Reference
        sku = browser.find_element_by_xpath('//*[@id="muestra"]/div[2]/div[1]/span/b').text
    except NoSuchElementException:
        sku = default_sku
        input("[!] Element sku not found...")
    try:
        # Description
        description = browser.find_element_by_xpath('//*[@id="description"]/div')
    except NoSuchElementException:
        description = default_description
        input("[!] Element description not found...")

    # Image scraping
    print("\n\n")
    time.sleep(2)
    try:
        # Gallery Container
        gallery_container = browser.find_element_by_xpath('//*[@class="slick-track"]/')
    except NoSuchElementException:
        gallery_container = "404"
    if gallery_container == "404":
        try:
            gallery_container = browser.find_element_by_xpath('//*[@id="content"]/div/div[2]/ul/div/div')
        except NoSuchElementException:
            input("[!] Image container alternative not found...")
            skip_product = True
    if skip_product:
        return
    pictures = gallery_container.find_elements_by_tag_name("li")
    images = ""
    img_counter = 1
    for picture in pictures:
        if img_counter != 1:
            images = images + ","
        picture = picture.find_element_by_tag_name("img")
        picture_url = picture.get_attribute("src")
        print("IMAGEN ", img_counter, ": ", picture_url)
        images = images + picture_url
        img_counter = img_counter + 1
    if img_counter == 0:
        input("[!] Image elements not found...")

    # Refactor variables
    brand = brand[7:]

    description = description.get_attribute("innerHTML")
    sku = "YM000000A" + sku

    price = price[4:]
    price = float(price)
    price = price * 1.03
    price = round(price, 2)

    # Print product and save to csv
    print_product(title, price, brand, sku, summary, description)
    save_to_file("export/yamoshi.csv", 0, title, price, sku, brand, summary, description, images)


def scrape_infotech(tool_url):
    browser.get(tool_url)
    productTitle = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div/h2').text
    productPrice = browser.find_element_by_xpath(
        '//*[@id="main"]/div[2]/div[4]/div[1]/div[2]/div[1]/div[1]/div/ins').text
    productPrice = productPrice[3:]
    pricing = ''
    for character in productPrice:
        if character != '\n':
            pricing = pricing + character
        else:
            break
    productPrice = pricing
    productBrand = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div[3]/div/div[2]/ul/li[1]').text
    productBrand = productBrand[8:]
    productSummary = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div[3]/div/div[2]/ul')
    productSku = browser.find_element_by_xpath('//*[@id="referenciaPrincipal"]').text
    productDesc = browser.find_element_by_xpath('//*[@id="description"]/div')
    productSummary = productSummary.text
    productDesc = productDesc.get_attribute("innerHTML")
    productSku = "IT000000A" + productSku
    print("============ DETAILS ============")
    print("[•] TITULO:", productTitle)
    print("[•] PRECIO:", productPrice)
    print("[•] BRAND:", productBrand)
    print("[•] SKU:", productSku, "\n")
    print("============ SUMMARY ============\n", productSummary, "\n\n")
    print("============ DESCRIPTION ============\n", productDesc)
    # Image downloader
    gallery = browser.find_element_by_xpath('//*[@id="content"]/div/div/ul')
    pictures = gallery.find_elements_by_tag_name("li")
    contador = 1
    print("\n\n")
    productImages = ""
    for picture in pictures:
        if contador != 1:
            productImages = productImages + ","
        picture = picture.find_element_by_tag_name("img")
        pictureUrl = picture.get_attribute("src")
        print("IMAGEN ", contador, ": ", pictureUrl)
        productImages = productImages + pictureUrl
        contador = contador + 1
    # CSV writing
    productPrice = productPrice.replace(',', '')
    price = float(productPrice)
    price = price * 1.03
    price = round(price, 2)
    print("(•)  PRODUCT PRICE: ", price)
    row = [
        1,  # ID
        0,  # Activo (0/1)
        productTitle,  # Nombre
        "Fuentes de Poder,Componentes,Inicio",  # Categorías (x,y,z...)
        price,  # Precio impuestos INCLUIDOS
        1,  # ID regla de impuestos
        '',  # Precio de coste
        0,  # En oferta (0/1)
        '',  # Valor del descuento
        '',  # Porcentaje de descuento
        '',  # Descuento desde (aaaa-mm-dd)
        '',  # Descuento hasta (aaaa-mm-dd)
        productSku,  # Referencia nº
        '',  # N° de referencia proveedor
        '',  # Proveedor
        productBrand,  # Marca
        '',  # EAN13
        '',  # UPC
        '',  # MPN
        '',  # Ecotasa
        '',  # Anchura
        '',  # Altura
        '',  # Profundidad
        '',  # Peso
        '',  # Plazo de entrega para los productos en stock:
        '',  # Plazo de entrega para los productos fuera de stock que se permiten comprar:
        0,  # Cantidad
        '',  # Cantidad mínima
        '',  # Nivel de stock bajo
        '',  # Envíame un mensaje de correo electrónico cuando la cantidad esté por debajo de este nivel
        '',  # Visible en
        '',  # Coste adicional del envío
        '',  # Unidad para el precio unitario
        '',  # Precio unitario
        productSummary,  # Resumen
        productDesc,  # Descripción
        '',  # Etiquetas (x,y,z...)
        '',  # Meta-título
        '',  # Meta keywords
        '',  # Meta descripción
        '',  # URL reescrita
        '',  # Etiqueta cuando se encuentra en stock
        '',  # Etiqueta para cuando se permiten pedidos en espera
        '',  # Disponible para pedidos (0 = No, 1 = Si)
        '',  # Fecha de disponibilidad del producto
        '',  # Fecha de creación del producto
        1,  # Mostrar Precio (0 = No, 1 = Si)
        productImages,  # URL's de las imágenes (x,y,z...)
        '',  # Textos alternativos de imagen (x,y,z...)
        '',  # Elimine las imágenes existentes (0 = No, 1 = Si)
        '',  # Característica (Nombre:Valor:Posición:Personalizado)
        '',  # Solo disponible por Internet (0 = No, 1 = Si)
        'new',  # Estado
        0,  # Personalizable (0 = No, 1 = Sí)
        0,  # Se pueden subir archivos (0 = No, 1 = Sí)
        '',  # Campos de texto (0 = No, 1 = Sí)
        1,  # Acción cuando no haya existencias de stock
        0,  # Producto virtual (0 = No, 1 = Sí)
        '',  # URL de archivo
        '',  # Número de descargas permitidas
        '',  # Fecha de expiración (dd-mm-aaaa)
        '',  # Número de días
        '',  # ID / Nombre de la tienda
        '',  # Administración Avanzada de Stock
        '',  # Dependiendo del stock
        '',  # Almacén
        '',  # Accesorios (x,y,z...)
    ]
    # name of csv file
    filename = "infotec.csv"

    # writing to csv file
    with open(filename, 'a', newline='', encoding="utf-8") as file:
        csvwriter = csv.writer(file, delimiter=';')
        csvwriter.writerow(row)


def main():
    print(WELCOME_MSG)
    RUNNING = True
    while RUNNING:
        print("1. Linio Website")
        print("2. Infotec (prestashop)")
        print("3. Infotec Website")
        print("4. Yamoshi Website")
        print("0. Exit program")
        print("[———————————————————————————————————————]\n")
        SELECTION = int(input("[•] Select an option: "))
        adminUrl = browser.current_url
        if SELECTION == 1:
            # Linio Website
            TOOL_URL = input("[•] Url to scrape: ")
            browser.get(TOOL_URL)
            browser.find_element_by_xpath('//*[@id="panel-features"]/h2').click()
            productTitle = browser.find_element_by_xpath('//*[@id="display-zoom"]/div[1]/h1/span').text
            productPrice = browser.find_element_by_class_name("price-main-md").text
            # productPrice = browser.find_element_by_xpath('//*[@id="display-zoom"]/div[2]/div[2]/div[2]/div[1]/div/span').text
            productBrand = browser.find_element_by_xpath('//*[@id="display-zoom"]/div[1]/span/a').text
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
            productImages = ""

            for picture in pictures:
                if contador != 1:
                    productImages = productImages + ","
                picture = picture.find_element_by_class_name("image-wrapper")
                sources = picture.find_elements_by_tag_name("source")
                pictureUrl = sources[1].get_attribute("srcset")
                pictureUrl = "https://" + pictureUrl[2:]
                print("IMAGEN ", contador, ": ", pictureUrl)
                productImages = productImages + pictureUrl
                contador = contador + 1
            # CSV writing
            myString = productPrice[3:]
            myString = myString.replace(',', '')
            price = float(myString)
            print("(•)  PRODUCT PRICE: ", price)
            categories = "Laptops,Inicio"
            row = [
                1,  # ID
                1,  # Activo (0/1)
                productTitle,  # Nombre
                categories,  # Categorías (x,y,z...)
                price,  # Precio impuestos INCLUIDOS
                1,  # ID regla de impuestos
                '',  # Precio de coste
                0,  # En oferta (0/1)
                '',  # Valor del descuento
                '',  # Porcentaje de descuento
                '',  # Descuento desde (aaaa-mm-dd)
                '',  # Descuento hasta (aaaa-mm-dd)
                productSku,  # Referencia nº
                '',  # N° de referencia proveedor
                '',  # Proveedor
                productBrand,  # Marca
                '',  # EAN13
                '',  # UPC
                '',  # MPN
                '',  # Ecotasa
                '',  # Anchura
                '',  # Altura
                '',  # Profundidad
                '',  # Peso
                '',  # Plazo de entrega para los productos en stock:
                '',  # Plazo de entrega para los productos fuera de stock que se permiten comprar:
                0,  # Cantidad
                '',  # Cantidad mínima
                '',  # Nivel de stock bajo
                '',  # Envíame un mensaje de correo electrónico cuando la cantidad esté por debajo de este nivel
                '',  # Visible en
                '',  # Coste adicional del envío
                '',  # Unidad para el precio unitario
                '',  # Precio unitario
                productSummary,  # Resumen
                productDesc,  # Descripción
                '',  # Etiquetas (x,y,z...)
                '',  # Meta-título
                '',  # Meta keywords
                '',  # Meta descripción
                '',  # URL reescrita
                '',  # Etiqueta cuando se encuentra en stock
                '',  # Etiqueta para cuando se permiten pedidos en espera
                '',  # Disponible para pedidos (0 = No, 1 = Si)
                '',  # Fecha de disponibilidad del producto
                '',  # Fecha de creación del producto
                1,  # Mostrar Precio (0 = No, 1 = Si)
                productImages,  # URL's de las imágenes (x,y,z...)
                '',  # Textos alternativos de imagen (x,y,z...)
                '',  # Elimine las imágenes existentes (0 = No, 1 = Si)
                '',  # Característica (Nombre:Valor:Posición:Personalizado)
                '',  # Solo disponible por Internet (0 = No, 1 = Si)
                'new',  # Estado
                0,  # Personalizable (0 = No, 1 = Sí)
                0,  # Se pueden subir archivos (0 = No, 1 = Sí)
                '',  # Campos de texto (0 = No, 1 = Sí)
                1,  # Acción cuando no haya existencias de stock
                0,  # Producto virtual (0 = No, 1 = Sí)
                '',  # URL de archivo
                '',  # Número de descargas permitidas
                '',  # Fecha de expiración (dd-mm-aaaa)
                '',  # Número de días
                '',  # ID / Nombre de la tienda
                '',  # Administración Avanzada de Stock
                '',  # Dependiendo del stock
                '',  # Almacén
                '',  # Accesorios (x,y,z...)
            ]
            # name of csv file
            filename = "products-linio.csv"

            # writing to csv file
            with open(filename, 'a', newline='') as file:
                csvwriter = csv.writer(file, delimiter=';')
                csvwriter.writerow(row)
        elif SELECTION == 2:
            # Infotech Website
            TOOL_URL = input("[•] Url to scrape: ")
            scrape_infotech(TOOL_URL)
        elif SELECTION == 3:
            TOOL_URL = input("[•] Url to scrape: ")
            browser.get(TOOL_URL)
            productHolder = browser.find_element_by_xpath('//*[@id="js-product-list"]/div[1]/div')
            productList = productHolder.find_elements_by_tag_name("article")
            productCount = 0
            productLinks = []
            for product in productList:
                name = product.find_element_by_class_name("product-name")
                link = name.find_element_by_tag_name("a").get_attribute("href")
                productLinks.append(link)
                print(link)
                productCount += 1
            print("\nAMOUN OF PRODUCTS FOUND: ", productCount)
            input("Proceed to export products to CSV?")
            count = 0
            percentage = 0
            for link in productLinks:
                # Execute operation
                scrape_infotech(link)

                # Print percentage
                count += 1
                percentage = (count * 100) / productCount
                print("\n\n[•] PORCENTAJE DE TAREA: ", round(percentage, 2), "%")
        elif SELECTION == 4:
            TOOL_URL = input("[•] Yamoshi Url to scrape: ")
            browser.get(TOOL_URL)
            productHolder = browser.find_element_by_xpath('//*[@id="js-product-list"]/div')
            productList = productHolder.find_elements_by_tag_name("article")
            productCount = 0
            productLinks = []
            for product in productList:
                name = product.find_element_by_class_name("product-title")
                link = name.find_element_by_tag_name("a").get_attribute("href")
                productLinks.append(link)
                print(link)
                productCount += 1
            print("\nAMOUN OF PRODUCTS FOUND: ", productCount)
            input("Proceed to export products to CSV?")
            count = 0
            percentage = 0
            for link in productLinks:
                # Execute operation
                scrape_yamoshi(link)

                # Print percentage
                count += 1
                percentage = (count * 100) / productCount
                print("\n\n[•] PORCENTAJE DE TAREA: ", round(percentage, 2), "%")
            print("\n[•] SE EXPORTARON", productCount, "PRODUCTOS")
        elif SELECTION == 5:
            # writing to csv file
            with open("export.csv", 'r', encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=';')
                # csvwriter.writerow(row)
                counter = 0
                for row in reader:
                    if counter > 0:
                        line_id = row[0]
                        categories = row[1]
                        link_url = row[2]
                        exported = row[3]
                        if exported == "false":
                            print(row)
                    counter += 1
        elif SELECTION == 0:
            RUNNING = False
            browser.close()
        print("\n")

main()
