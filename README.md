# 📲 Search for apps in Appstore
> ℹ️ He creado este script para búsqueda de Apps en la AppStore de Europa (€ como moneda). Si se desea cambiar la AppStore se debe modificar la moneda en circulación.

AppStore_Scraper es un script desarrollado en Python para ayudar a usuarios de dispositivos **Apple** a buscar las Apps que deseen conocer si son de pago o son gratuitas.

### Estructura del código
> *Dentro del código se puede encontrar comentarios para cada línea o proceso que es importante mencionar su utilidad.*

El script consta de una única función llamada `web_scrapper` que se encarga de recorrer el diccionario que contiene los nombres y URLs de las Apps (*apps*), se conecta a la URL para extraer la información de pago y finalmente imprime los nombres de las Apps que son de pago, las que son gratuitas y las que dieron error de conexión.
