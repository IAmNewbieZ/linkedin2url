import requests
from bs4 import BeautifulSoup
import re
import pyperclip
import pyfiglet
import argparse

def clipboard_func():
    content = pyperclip.paste()
    return content

def file_func(filename):
    with open(filename) as file:
        content = file.read()
        return content

f = pyfiglet.figlet_format("linkedin2url", font="slant")
print(f)

parser = argparse.ArgumentParser(description='Process Linkedin shortened urls to original urls.')
parser.add_argument('--clipboard','-c',action='store_true',
                    help='Use clipboard')
parser.add_argument('--file', '-f',
                    help='Use file')
parser.add_argument('--output', '-o',
                    help='Write to file')

args = parser.parse_args()

content = ""
result_url = []

if(args.clipboard and args.file): print("Use only 1 option")
elif(args.clipboard): content = clipboard_func()
elif(args.file): content = file_func(args.file)
else: print(parser.print_help())

list_url = re.findall("https://.*", content)
for url in list_url:
    if("lnkd.in" in url):
        url = url.strip()
        res = requests.get(url,timeout=20,allow_redirects=False)
        if(res.status_code == 200):
            html_doc = res.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            result = soup.find('a', attrs={'data-tracking-control-name': 'external_url_click'}).get_text()
            if(args.output): result_url.append(result.strip())
            print(result.strip())
        else:
            location=res.headers['Location']
            if(args.output): result_url.append(location)
            print(location)
    else:
        if(args.output): result_url.append(url)
        print(url)

if(args.output):
    with open(args.output, "w") as write_file:
        write_file.write("\n".join(result_url)) 
    write_file.close()        