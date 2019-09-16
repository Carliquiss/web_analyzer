import os
import sys
import shutil
import requests
import hashlib

from argparse import ArgumentParser
from colorama import init, Fore

SPIDER_PATH = './scripts/Spider/'
DOCUMENT_SCRAPING_PATH = './scripts/Document-scraping-Tool/'

init(autoreset=True)  # Para que los colores se reseten tras un print


def getFilesFromFolder(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    return files


def adjustURL(url):
    if not (url.split("/")[0] == "http:" or url.split("/")[0] == 'https:'):
        url = "http://" + url

    return url


def main():
    print(Fore.CYAN + '''
██╗    ██╗███████╗██████╗      █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ 
██║    ██║██╔════╝██╔══██╗    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ██████╔╝    ███████║██╔██╗ ██║███████║██║   ╚████╔╝   ███╔╝ █████╗  ██████╔╝
██║███╗██║██╔══╝  ██╔══██╗    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗
╚███╔███╔╝███████╗██████╔╝    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████╗███████╗██║  ██║
 ╚══╝╚══╝ ╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
    ''')

    argp = ArgumentParser(description="Scraper de imágenes")

    argp.add_argument('-u', '--url', help='URL to analyze')

    argp.add_argument('-c', '--clean', action='store_true', default=False, dest='clean', help='Clear folders')

    argp.add_argument('-q', '--quiet', action='store_true', default=False, dest='quiet', help='Quiet mode')

    args = argp.parse_args()

    if args.url:
        url = adjustURL(args.url)
        Launch_spider = 'python3 ' + SPIDER_PATH + "spider.py -u {}".format(url)
        Launch_documentScraper = 'python3 ' + DOCUMENT_SCRAPING_PATH + 'documentScraper.py'
        Launch_metadata = 'python3 ' + DOCUMENT_SCRAPING_PATH + 'metadataChecker.py -d ./Documents'

        if not args.quiet:
            Launch_spider += " -v"
        else:
            Launch_documentScraper += ' -q'
            Launch_metadata += ' -q'

        if args.clean:
            Launch_spider += ' -c'
            Launch_documentScraper += ' -c'
            Launch_metadata += ' -c'

        os.system(Launch_spider)

        urls_lists = getFilesFromFolder('./URLS_locales/')

        for file in urls_lists:
            Launch_documentScraperIterative = Launch_documentScraper + ' -i ' + file
            os.system(Launch_documentScraperIterative)

        os.system(Launch_metadata)

    else:
        print(Fore.RED + 'No URL provided')


if __name__ == '__main__':
    main()


