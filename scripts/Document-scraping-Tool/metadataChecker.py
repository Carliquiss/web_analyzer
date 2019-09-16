from argparse import ArgumentParser
from colorama import init, Fore

import exiftool
import os
import sys
import shutil

init(autoreset=True)  # Para que los colores se reseten tras un print

PATH_METADATA = "./Metadata/"


def initFolders():
    if not os.path.exists(PATH_METADATA[:-1]):
        os.mkdir(PATH_METADATA[:-1])


def createFolder(nombre):
    nombreCarpeta = PATH_METADATA + nombre + "/"

    try:
        if not os.path.exists(nombreCarpeta):
            os.mkdir(nombreCarpeta)

    except:
        print("La carpeta ya existe")

    return nombreCarpeta


def clearFolders():
    if os.path.exists(PATH_METADATA[:-1]):
        shutil.rmtree(PATH_METADATA[:-1])

    initFolders()


def getMetadata(file):
    with exiftool.ExifTool() as met:
        metadata = met.get_metadata(file)

    saveName = metadata['SourceFile'].split('/')
    saveName = saveName[len(saveName) - 2]

    print(Fore.WHITE + 'Analyzing ' + metadata['SourceFile'], end='')
    file2 = open(PATH_METADATA + "Data_" + saveName + '.txt', 'a')

    file_added_toInform = False

    valid_fields = ['File', 'ExifTool', 'SourceFile']

    for field, data in metadata.items():
        short_field = field.split(":")[0]

        file2.write(str(field) + '==>' + str(data) + '\n')

        if short_field not in valid_fields and file_added_toInform == False:
            file_added_toInform = True

            with open(PATH_METADATA + "Inform_" + saveName + '_sensibleMetadata.txt', 'a') as file3:
                file3.write(metadata['SourceFile'] + "\n")

    file2.write('--------------------------------------------\n')
    file2.close()

    print(Fore.GREEN + ' OK')


def getFilesFromFolder(path):
    for r, d, f in os.walk(path):
        for file in f:
            getMetadata(os.path.join(r, file))


def blockPrintOutput():
    sys.stdout = open(os.devnull, 'w')


def main():
    """
        Función principal donde se comprueban los parámetros de la función y
        se ejecutan las acciones acorde a estos.

        Los parámetros son:
            -f <file_path>      : Si se quiere analizar los metadatos de un archivo en concreto
            -d <Dir_path>     : Directory to analyze
            -c                  : Si se quieren limpiar las carpetas y archivos ya creados
            -v                  : Activar el modo verboso
        """

    print(Fore.CYAN +
          """
███╗   ███╗███████╗████████╗ █████╗ ██████╗  █████╗ ████████╗ █████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██╔████╔██║█████╗     ██║   ███████║██║  ██║███████║   ██║   ███████║    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║  ██║██╔══██║   ██║   ██╔══██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║██████╔╝██║  ██║   ██║   ██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                                                 
""")

    argp = ArgumentParser(description="Metadata Checker")

    argp.add_argument('-f', '--file', dest='FileName', help='File to analyze')

    argp.add_argument('-d', '--dir', dest='DirName', help='Directory to analyze')

    argp.add_argument('-c', '--clean', action='store_true', default=False,
                      dest='clean', help='Clean Metadata folder')

    argp.add_argument('-q', '--quiet', action='store_true', default=False,
                      dest='quiet', help='Quiet mode')

    args = argp.parse_args()

    if args.clean:
        clearFolders()

    initFolders()

    if args.quiet:
        blockPrintOutput()

    if args.FileName:
        getMetadata(args.FileName)

    if args.DirName:
        if os.path.exists(args.DirName):
            getFilesFromFolder(args.DirName)


if __name__ == "__main__":
    main()
