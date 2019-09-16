import requests
import sys
import os
import shutil
import glob
import time
from parsel import Selector
from colorama import init, Fore
from argparse import ArgumentParser



init(autoreset=True) # Para que los colores se reseten tras un print

PATH_LOCALES = "./URLS_locales"
PATH_EXTERNAS = "./URLS_externas"
NIVEL_PROFUNDIDAD = 100 # Con qué nivel de profundidad se quiere escanear, más profundidad más tarda


def initFolders():
    """
    Función para crear carpetas donde se guardan las URLs encontradas
    """
    if os.path.exists(PATH_LOCALES) == False:
        os.mkdir(PATH_LOCALES)
    if os.path.exists(PATH_EXTERNAS) == False:
        os.mkdir(PATH_EXTERNAS)


def clearFolders():
    """
    Función que elimina los archivos dentro de las carpetas
    """

    if os.path.exists(PATH_LOCALES) == True:
        shutil.rmtree(PATH_LOCALES + "/")
    if os.path.exists(PATH_EXTERNAS) == True:
        shutil.rmtree(PATH_EXTERNAS + "/")

    initFolders()



def EliminarArchivosInnecesarios():
    """
    Función que elimina una serie de archivos creados que no hacen falta.
    """
    archivoslocales = glob.glob(PATH_LOCALES + "/*.txt")

    for archivo in archivoslocales:
        if(archivo[:-4][-1] != "_"):
            os.remove(archivo)


    archivosexternos = glob.glob(PATH_EXTERNAS + "/*.txt")

    for archivo in archivosexternos:
        if(archivo[:-4][-1] != "_"):
            os.remove(archivo)



def removeDuplicatedLines(nombre_archivo):
    """
    Función para eliminar las lineas duplicadas dentro de un archivo
    Se crea un archivo con el nombre del original + "_" y se elimina
    el original.

    Parámetros:
        nombre_archivo:string: Nombre del archivo al que se le quieren
                               eliminar las lineas duplicadas
    """
    lineas_comprobadas = set()
    archivo = open(nombre_archivo[:-4] + "_.txt" , "w")

    for linea in open(nombre_archivo, "r"):

        if linea not in lineas_comprobadas:
            archivo.write(linea)
            lineas_comprobadas.add(linea)


    archivo.close()
    #os.remove(nombre_archivo)


def selectLocalOrExternalLinks(enlaces, url):
    """
    Funcion para clasificar los enlaces en locales o en externos según una URL dada

    Los parámetros son:
        enlaces:lista:  Conjunto de todos los enlaces a clasificar
        baseURL:string: URL a la que se hace el crawling
    """

    urlsLocales = []
    urlsExternas = []
    baseURL = url.split("/")[2]

    for enlace in enlaces:

        if(enlace.split("/")[0] == 'http:' or enlace.split("/")[0] == 'https:'):
            comparacion = enlace.split("/")[2]

            if (comparacion == baseURL):
                urlsLocales.append(enlace)

            else:
                urlsExternas.append(enlace + " from ----> " + url)

        else:
            try:
                #Si el enlace comienza con / es que depende de la URL base
                if(enlace[0] != "/"):
                    #Si el enlace obtenido comienza con "." es que depende de
                    #la URL anterior
                    if(enlace[0] == "."):
                        trozo_url = url.rsplit("/", 1)[0]
                        enlace = trozo_url + enlace[1::]
                        urlsLocales.append(enlace)

                    if(enlace[0] == " "):
                        enlace = enlace[1:len(enlace)]

                        if enlace[0] != "/":
                            enlace = "/" + enlace
                            urlsLocales.append("http://" + baseURL + enlace)

                        else:
                            urlsLocales.append("http://" + baseURL + enlace)

                    else:
                        enlace = "/" + enlace
                        urlsLocales.append("http://" + baseURL + enlace)


                else:

                    urlsLocales.append("http://" + baseURL + enlace)

            except:
                pass


    return urlsLocales, urlsExternas




def getLinks(url):
    """
    Función que toma una URL, selecciona todos los enlaces a páginas que encuentra
    y llama a la funcion para clasificarlos en externos o en locales

    Los parámetros son:
        url:string: Url a la que se quiere hacer el crawling
    """
    try:
        #Accedemos a la páginas y nos quedamos con los href a otras urls
        if (url.split(".")[-1]).upper() == "PDF" or (url.split(".")[-1]).upper() == "ZIP" or (url.split("?")[-1]).upper() == "THEME=PDF":
            tipo_archivo = ""
            href_links = ""

        else:

            response = requests.get(url, timeout = 5)
            tipo_archivo = response.headers.get('content-type')

        if "text/" in tipo_archivo:
            selector = Selector(response.text)
            href_links = selector.xpath('//a/@href').getall()

        else:
            #print("Archivo diferente a texto")
            href_links = ""

    except:
        print("Página no disponible")
        href_links = ""

    return selectLocalOrExternalLinks(href_links, url)




def CrawlPage(url_principal, modo):
    """
    Función para ir haciendo el crawling a las páginas encontradas

    Los parámetros son:
        url:string:  Pagina a la que se quiere hacer el crawling de forma iterativa
        modo:string: Local o Externo para hacer crawling solo a las webs locales
                     o tambien a las externas.
    """

    print(Fore.YELLOW + "\nAnalizando: " +  url_principal, end = " ")

    #nombre_fichero = "/" + url_principal.replace("/", "_")
    baseURL = url_principal.split("/")[2]
    nombre_fichero = "/" + baseURL
    linksLocales, linksExternos = getLinks(url_principal)


    if modo == "Local":

        print(*linksLocales, sep = "\n", file=open(PATH_LOCALES + nombre_fichero + ".txt", "a"))
        removeDuplicatedLines(PATH_LOCALES + nombre_fichero + ".txt")

        #Prueba a ver si se van guardando tb en los linksExternos
        print(*linksExternos, sep = "\n", file=open(PATH_EXTERNAS + "/" + nombre_fichero + ".txt", "a"))
        removeDuplicatedLines(PATH_EXTERNAS + nombre_fichero + ".txt")

    elif modo == "Externo":
        print(Fore.RED + "------------- Modo Externo -------------")

    else:
        print(Fore.RED + "------------- Modo Mixto (Local + Externo) -------------")
        #Este modo pasará a ser el modo Default, implementado ahora en local

    print(Fore.GREEN + "OK")

    return linksLocales, linksExternos


def CrawlingIterative(Primera_url, modo):
    """
    Función que hace el crawling a la url especificada de forma iterativa.

    Los parámetros son:
        Primera_url:string: URL que se va a crawlear de forma iterativa
        modo:str: Puede ser Local o Externo
    """

    #Aqui se debe poner de forma iterativa el crawling
    enlacesLocales, enlacesExternos = CrawlPage(Primera_url, modo)

    #Se mete en todas las locales y las saca
    if modo == "Local":
        urls_por_visitar = {}
        enlaces_visitados = []

        for i in range(NIVEL_PROFUNDIDAD):
            urls_por_visitar[i] = []

        urls_por_visitar[0].append(enlacesLocales) #Primer Crawl

        for nivel in range(NIVEL_PROFUNDIDAD-1):

            for posicion in range(len(urls_por_visitar[nivel])):

                for num_enlace in range(len(urls_por_visitar[nivel][posicion])):
                    enlace = urls_por_visitar[nivel][posicion][num_enlace]

                    if enlace not in enlaces_visitados:
                        enlaces_visitados.append(enlace)
                        enlaces2, ext2 = CrawlPage(enlace, "Local")
                        urls_por_visitar[nivel+1].append(enlaces2)


    return len(enlaces_visitados)


def blockPrintOutput():
    sys.stdout = open(os.devnull, 'w')


def main():
    """
    Función principal donde se comprueban los parámetros de la función y
    se ejecutan las acciones acorde a estos.

    Los parámetros son:
        -u <url>            : URL (con http://) a la que se quiere hacer el crawling
        -i <input_file>     : Si se quieren leer urls de un archivo
        -c                  : Si se quieren borrar las carpetas y archivos ya creados
        -v                  : Activar el modo verboso

    """

    print(Fore.CYAN + """
██╗    ██╗███████╗██████╗      ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ 
██║    ██║██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ██████╔╝    ██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
██║███╗██║██╔══╝  ██╔══██╗    ██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
╚███╔███╔╝███████╗██████╔╝    ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
 ╚══╝╚══╝ ╚══════╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝
        """)

    url = ''

    argp = ArgumentParser(description = "Crawler de páginas web")

    argp.add_argument('-u', '--url', help = 'URL a la que se quiere hacer el crawling',
        required = False, default = "")

    argp.add_argument('-i', '--input_file', dest = 'FileName',
        help = 'Si se quiere indicar una lista de urls')

    argp.add_argument('-c', '--clean', action = 'store_true', default = False,
        dest = 'clean', help = 'Limpiar las carpetas y archivos')

    argp.add_argument('-v', '--verbose', action = 'store_true', default = False,
        dest = 'verbose', help = 'Mostrar la salida por la pantalla')


    argumentos = argp.parse_args()

    if argumentos.clean == True:
        clearFolders()

    if argumentos.verbose == False:
        blockPrintOutput()



    modo = 'Local'
    initFolders()

    if argumentos.url != "":

        try:
            if argumentos.url.split("/")[0] == "http:" or argumentos.url.split("/")[0] == "https:":
                print(Fore.GREEN + "URL OK")

            else:
                argumentos.url = "http://" + argumentos.url
                print("URL changed to " + argumentos.url)

            NumeroURLS = 0

            startTime = time.time()
            NumeroURLS = CrawlingIterative(argumentos.url, modo)
            EliminarArchivosInnecesarios()

        except:
            print(Fore.RED + "\nError en la url (enter http(s):// + domain)\n")


        print(Fore.LIGHTMAGENTA_EX + "\nEl programa ha tardado: " + str(time.time() - startTime) + " segundos")
        print("Se han escaneado: " + str(NumeroURLS) + " URLs")

    else:

        try:
            archivo = open(argumentos.FileName, "r")
            lineas = archivo.read().splitlines()

            Numero_linea = 0
            NumeroURLS = []
            urls_analizadas = set()

            for linea in lineas:
                if linea.split("/")[0] == "http:" or linea.split("/")[0] == "https:":
                    print(Fore.GREEN + "Formato URL okey")

                else:
                    linea = "http://" + linea
                    print("URL changed to " + linea)

                if linea not in urls_analizadas:

                    print(Fore.LIGHTBLUE_EX + "\n\nAnalizando URL {} de {}".format(Numero_linea+1, len(lineas)))

                    startTime = time.time()

                    try:

                        NumeroURLS.append(CrawlingIterative(linea, modo))
                        EliminarArchivosInnecesarios()

                        print(Fore.LIGHTMAGENTA_EX + "\nPara la URL {} el programa ha tardado: ".format(linea) +
                            str(time.time() - startTime) + " segundos")

                    except:
                        print("Hubo algún problema con la URL: " + linea)
                        NumeroURLS.append(0)

                    urls_analizadas.add(linea)
                    Numero_linea += 1

            print(Fore.LIGHTGREEN_EX + "\n\n____________________________________________\n")
            print(Fore.LIGHTCYAN_EX + "\t\tResumen: \n")

            for i in range(len(NumeroURLS)):
                print(Fore.LIGHTGREEN_EX + "URL: {} analizada, encontrados {} enlaces locales".format(
                    lineas[i], NumeroURLS[i], end = ""))
                print()

        except:
            print(Fore.RED + "Hay algún problema con el fichero de entrada")


if __name__ == "__main__":
    main()
