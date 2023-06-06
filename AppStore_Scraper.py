import sys
import re
import requests
from bs4 import BeautifulSoup
from info_apps import apps_dict


# Funcion para hacer el webscrapping de la AppStore
def web_scrapper(apps_dict):
    # Define las variables iniciales del webscrapping
    status_nok = list()         # Lista para las APPs que devuelva la web error 404
    app_ok = dict()             # Diccionario para las APPs de pago
    app_free = list()           # Lista para las APPs que estan gratis
    num = len(apps_dict)             # Longitud del diccionario que tiene las APPs y sus URLs
    print(f"\nTotal de APPS a buscar: {num}\n")

    try:
        for app, web in apps_dict.items():       # Recorre el diccionario de las APPs y sus URLs
            try:
                price = str()
                while True:
                    page = requests.get(web)        # Ejecuta el requests a la URL de la APP a consultar
                    if page.status_code == 404:     # Si devuelve la web un error 404 almacena el nombre de la APP en la lista 'status_nok' y continua a la siguiente APP
                        status_nok.append(app)
                        continue

                    soup = BeautifulSoup(page.text, 'html.parser')      # Parsea el HTML de la pagina web de la APP a consultar
                    result_pay = soup.find_all('dd', string=re.compile("€"), attrs={"class": "information-list__item__definition"})           # Busca en el HTML los parametros indicados para las APPs de pago. OJO: Cambiar el '€' por el simbolo de la moneda para la tienda seleccionada
                    result_free = soup.find_all('dd', string=re.compile("Gratis"), attrs={"class": "information-list__item__definition"})     # Busca en el HTML los parametros indicados para las APPs gratis. OJO: Cambiar el 'Gratis' por el valor correspondiente para la tienda seleccionada

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

                print(f"{num}. - Precio de {app}: {price}")
                num -= 1

                # Si el precio es vacio o no registra un valor, imprime el nombre de la APP que ha fallado y finaliza el proceso
                if price == "":
                    print(f"**************************************\nFallo en la app {app}")
                    sys.exit()
            except Exception as error:
                print(f"Ha fallado el proceso de obtener precios: {error}")

        # Imprime el diccionario de APPs de pago, la lista de APPs gratis y la lista de APPs que fallaron
        print(f"\nAplicaciones de pago ({len(app_ok)}):\n{app_ok}\n")
        print(f"Aplicaciones GRATIS ({len(app_free)}):\n{app_free}\n")
        print(f"Aplicaciones que fallaron ({len(status_nok)}):\n{status_nok}\n")
    except Exception as error:
        print(f"Error Exception: {error}")


if __name__ == "__main__":
    print("Inicia proceso de Scrapper de la AppStore")
    """
        Define el diccionario que tiene como key: 'Nombre de la APP' y como value: 'URL de la AppStore'. Ejemplo: 'GoCoEdit - Code & Text Editor': 'https://apps.apple.com/es/app/gocoedit-code-text-editor/id869346854?mt=8&ign-mpt=uo%3D4'
        Ejecuta la funcion para hacer el webscrapping de la AppStore
    """
    if apps_dict:
        web_scrapper(apps_dict)
    else:
        print("No hay ninguna app para buscar")
