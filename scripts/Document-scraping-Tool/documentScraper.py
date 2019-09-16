import os
import sys
import shutil
import requests
import hashlib

from argparse import ArgumentParser
from colorama import init, Fore
from urllib.parse import urlsplit

init(autoreset=True)  # Para que los colores se reseten tras un print

BLOCKSIZE = 65536
hasher = hashlib.md5()

PATH_DOCUMENTS = "./Documents/"


def initFolders():
    if not os.path.exists(PATH_DOCUMENTS[:-1]):
        os.mkdir(PATH_DOCUMENTS[:-1])


def createFolder(nombre):
    nombreCarpeta = PATH_DOCUMENTS + nombre + "/"

    try:
        if not os.path.exists(nombreCarpeta):
            os.mkdir(nombreCarpeta)

    except:
        print("La carpeta ya existe")

    return nombreCarpeta


def clearFolders():
    if os.path.exists(PATH_DOCUMENTS[:-1]):
        shutil.rmtree(PATH_DOCUMENTS[:-1])

    initFolders()


def md5(file):
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()


def adjustURL(url):
    if not (url.split("/")[0] == "http:" or url.split("/")[0] == 'https:'):
        url = "http://" + url

    return url


def scanURLlist(file):
    archivo = open(file, 'r')
    urls = archivo.readlines()

    for url in urls:
        url = url.split("\n")[0]
        saveIfFile(adjustURL(url))


def saveIfFile(url):
    print("Analyzing " + url, end='')

    subdir = urlsplit(url).netloc
    createFolder(subdir)

    try:
        response = requests.get(url)

        if 'application' in response.headers['content-type']:

            file_type = response.headers['content-type'].split("/")[1]
            print(Fore.GREEN + " FILE FOUND " + file_type)

            file_path = PATH_DOCUMENTS + subdir + "/"
            file_name = "file." + file_type
            downloaded_file = file_path + file_name

            file = open(file_path + file_name, 'wb')
            file.write(response.content)

            new_name = md5(downloaded_file)

            os.rename(downloaded_file, file_path + new_name + "." + file_type)

            with open(file_path + 'Urls_from_names.txt', 'a') as file2:
                file2.write(url + " >>>>> " + new_name + "\n")

        else:
            print(Fore.WHITE + " No file type")

    except Exception as e:
        print(Fore.RED + "\n------------------ ERROR ---------------------")
        print(Fore.RED + "Error requesting the URL " + url)
        print(Fore.RED + str(e))


def blockPrintOutput():
    sys.stdout = open(os.devnull, 'w')


def main():
    """
    Función principal donde se comprueban los parámetros de la función y
    se ejecutan las acciones acorde a estos.

    Los parámetros son:
        -u <url>            : URL (con http://) a la que se quiere hacer el scrapeo
        -i <input_file>     : Si se quieren leer urls de un archivo
        -c                  : Si se quieren limpiar las carpetas y archivos ya creados
        -v                  : Activar el modo verboso
    """

    print(Fore.CYAN + """
██████╗  ██████╗  ██████╗██╗   ██╗███╗   ███╗███████╗███╗   ██╗████████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██╔════╝██║   ██║████╗ ████║██╔════╝████╗  ██║╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██║     ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║   ██║       ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║  ██║██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║       ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║   ██║       ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                                                    
""")

    argp = ArgumentParser(description="Scraper de imágenes")

    argp.add_argument('-u', '--url', help='URL a la que se quiere hacer el scrape',
                      required=False, default="")

    argp.add_argument('-i', '--input_file', dest='FileName', help='Si se quiere indicar una lista de urls')

    argp.add_argument('-c', '--clean', action='store_true', default=False,
                      dest='clean', help='Limpiar las carpetas y archivos')

    argp.add_argument('-q', '--quiet', action='store_true', default=False,
                      dest='quiet', help='Quiet mode')

    args = argp.parse_args()

    if args.clean:
        clearFolders()

    initFolders()

    if args.quiet:
        blockPrintOutput()

    if args.clean:
        clearFolders()

    if args.url:
        saveIfFile(adjustURL(args.url))

    if args.FileName:
        print(Fore.CYAN + "Opening file: " + args.FileName + "\n")
        scanURLlist(args.FileName)


if __name__ == '__main__':
    main()
