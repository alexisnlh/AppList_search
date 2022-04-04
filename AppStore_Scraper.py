import sys
import re
import requests
from bs4 import BeautifulSoup


# Funcion para hacer el webscrapping de la AppStore
def web_scrapper(apps):
    # Define las variables iniciales del webscrapping
    status_nok = list()         # Lista para las APPs que devuelva la web error 404
    app_ok = dict()             # Diccionario para las APPs de pago
    app_free = list()           # Lista para las APPs que estan gratis
    num = len(apps)             # Longitud del diccionario que tiene las APPs y sus URLs
    print("\nTotal de APPS a buscar: {}\n".format(num))

    # Verifica si el diccionario de las APPs y sus URLs tiene datos
    if apps:
        for app, web in apps.items():       # Recorre el diccionario de las APPs y sus URLs
            try:
                price = str()
                while True:
                    page = requests.get(web)        # Ejecuta el requests a la URL de la APP a consultar
                    if page.status_code == 404:     # Si devuelve la web un error 404 almacena el nombre de la APP en la lista 'status_nok' y continua a la siguiente APP
                        status_nok.append(app)
                        continue

                    soup = BeautifulSoup(page.text, 'html.parser')      # Parsea el HTML de la pagina web de la APP a consultar
                    result_pay = soup.find_all('dd', text=re.compile("€"), attrs={"class": "information-list__item__definition"})           # Busca en el HTML los parametros indicados para las APPs de pago. OJO: Cambiar el '€' por el simbolo de la moneda para la tienda seleccionada
                    result_free = soup.find_all('dd', text=re.compile("Gratis"), attrs={"class": "information-list__item__definition"})     # Busca en el HTML los parametros indicados para las APPs gratis. OJO: Cambiar el 'Gratis' por el valor correspondiente para la tienda seleccionada

                    if result_pay or result_free:       # Si consigue alguno de las dos variables en el HTML finaliza el while
                        break

                # Si la APP no es gratis parsea el div del HTML para extraer el precio y agregarlo al diccionario 'app_ok'
                if not result_free:
                    for i, entrada in enumerate(result_pay):
                        entrada = str(entrada)
                        position = entrada.find("\">") + 2
                        price = entrada[position:].split("<")[0]
                        if "\xa0" in price:
                            price = price.replace("\xa0", " ")
                        app_ok[app] = price
                # Si la APP es gratis agrega el nombre de esta en la lista 'app_free'
                else:
                    app_free.append(app)
                    price = "Gratis"

                print("{0}. - Precio de {1}: {2}".format(num, app, price))
                num -= 1

                # Si el precio es vacio o no registra un valor, imprime el nombre de la APP que ha fallado y finaliza el proceso
                if price == "":
                    print("**************************************")
                    print("Fallo en la app {}".format(app))
                    sys.exit()
            except Exception as error:
                print("Ha fallado el proceso de obtener precios: {}".format(error))

        # Imprime el diccionario de APPs de pago, la lista de APPs gratis y la lista de APPs que fallaron
        print("\nAplicaciones de pago ({0}):\n{1}\n".format(len(app_ok), app_ok))
        print("Aplicaciones GRATIS ({0}):\n{1}\n".format(len(app_free), app_free))
        print("Aplicaciones que fallaron ({0}):\n{1}\n".format(len(status_nok), status_nok))
    else:
        print("No hay ninguna app para buscar")


if __name__ == "__main__":
    print("Inicia proceso de Scrapper de la AppStore")
    # Define el diccionario que tiene como key: 'Nombre de la APP' y como value: 'URL de la AppStore'. Ejemplo: 'GoCoEdit - Code & Text Editor': 'https://apps.apple.com/es/app/gocoedit-code-text-editor/id869346854?mt=8&ign-mpt=uo%3D4'
    apps = {}
    # Ejecuta la funcion para hacer el webscrapping de la AppStore
    web_scrapper(apps)
