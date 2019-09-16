# Documents Scraping Tools (⚠️ Work in progress ⚠️)
_This is a toolkit to scrape different types of documents (images, pdfs, etc.) on an URL. All scripts are used in the same way with the same params._ 


## How does it works ⚙️
Depending on the type of documents you want to scrape, you should use one script or another according to this: 
  
  * Images: Use the "imageScraper.py"
  * Other type of files such as PDFs, DOCs, MP3 , etc(need some testing to see if it works correctly). : Use the "documentScraper.py"


## Installing 🔧
First clone the repo: 
```
https://github.com/Carliquiss/Document-scaping-Tool.git
```
Then run the following command to install needed libs:
```
pip3 install -r requirements.txt
```

## Usage ⌨️
The URL is given by the "-u" param: -u url (in format http://www.example.com)
  
If you want to scrape that URL for looking for the files: 
```
python3 script.py -u <url>
```
You can also use the "-c" param to clear all folders and files created by the scrapers 
```
python3 script.py -u <url> -c
```  
If you want to get the urls from a file just use "-i input_file":
```
python3 script.py -i <input_file>
```
For all the options you can add the verbose mode with "-v"
```
python3 script.py -u <url> -c
``` 
Or
```
python3 script.py -i <input_file> -vc
```
