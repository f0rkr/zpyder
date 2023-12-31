#!/usr/bin/env python

from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urljoin
from colorama import Fore, Style
from bs4 import BeautifulSoup
import validators
import traceback
import argparse
import requests
import os.path
import urllib
import random
import string
import signal
import sys


allowed_extension = ['PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg', 'GIF', 'gif', 'BMP', 'bmp']


# Handling SIGINT signal
def signal_handler(sig, frame):
    logger_info("Signal caught: Exiting")
    sys.exit(0)

# Defining Loggers
def logger_error(string):
    print(f"{Fore.RED}[?]{Style.RESET_ALL} Error: " + string)

def logger_info(string):
    print(f"{Fore.YELLOW}[!] "+string+f"{Style.RESET_ALL}")

def logger_valid(string):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {Style.BRIGHT}{string}{Style.RESET_ALL}")

# -*- coding: utf-8 -*-
def print_banner():
    print('''                                                                                                                  
    ███▀▀▀██████▀▀▀██▄▀███▀   ▀██▀███▀▀▀██▄ ▀███▀▀▀███▀███▀▀▀██▄  
    █▀   ███  ██   ▀██▄ ███   ▄█   ██    ▀██▄ ██    ▀█  ██   ▀██▄ 
    ▀   ███   ██   ▄██   ███ ▄█    ██     ▀██ ██   █    ██   ▄██  
       ███    ███████     ████     ██      ██ ██████    ███████   
      ███   ▄ ██           ██      ██     ▄██ ██   █  ▄ ██  ██▄   
     ███   ▄█ ██           ██      ██    ▄██▀ ██     ▄█ ██   ▀██▄ 
    █████████████▄       ▄████▄  ▄████████▀ ▄██████████████▄ ▄███▄
                                                              
                                                         
    Welcome to the Zpyder Program :)
    Author: f0rkr

    This program downloads all images recursively from a website,
    This program will only download images that have the following extensions: .jpg/jpeg, .png, .gif, and .bmp.
  ''')

# Get_image_name function
# Returns image name from image_object using alt tag
# or else getting the name from the src url
def get_image_name(image_object, path):
    # filename = os.path.basename(''.join(random.choice(string.ascii_lowercase) for i in range(16)) + "." +
    # src.split('.')[-1])
    # if image_object.get('alt'):
    #     extension = image_object.get('src').split('.')[-1]
    #     image_name = image_object['alt'].replace(' ', '-').replace('/', '').split('.')[0]
    #     return image_name + "." + extension
    file_path = os.path.join(path, os.path.basename(image_object['src']))
    if os.path.exists(file_path):
        return os.path.basename(''.join(random.choice(string.ascii_lowercase) for i in range(16)) + "." +image_object['src'].split('.')[-1])
    return os.path.basename(image_object['src'])


# Download_image function
# Get the url and image_object then it extract the image from
# the website and save it to a file
def download_image(url, image_object, path, level):
    filename = get_image_name(image_object, path)
    filepath = os.path.join(path, filename)
    full_url = urllib.parse.urljoin(url, image_object['src'])
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} LEVEL: {Fore.GREEN}{level}{Style.RESET_ALL} Downloading image: {Fore.GREEN}{filename}{Style.RESET_ALL}, from url: {Style.BRIGHT}{Fore.BLUE}{url}{Style.RESET_ALL}")
    response = requests.get(full_url)
    with open(filepath, 'wb') as f:
        f.write(response.content)
        f.close()


def extracting_images(url, level, path, soup, recursive=False):
    # Extracting all img tag in the html parsed data
    images = soup.find_all('img')
    linked_pages = soup.find_all('a')

    # Looping through all images and start extracting them
    for image_object in images:
        if image_object.get('src'):
            if image_object['src'].split("/")[-1].split(".")[-1] in allowed_extension:
                download_image(url, image_object, path, level)
    # Recursively extract all images from linked links to the base website
    if level > 0 and recursive:
        for page in linked_pages:
            if page.get('href'):
                try:
                    next_url = urllib.parse.urljoin(url, page['href'])
                    logger_info(f"Next url: {next_url}".format(next_url))
                    run_spider(next_url, level - 1, path, recursive)
                except Exception as exception:
                    logger_error(f"on line {Fore.RED}{sys.exc_info()[-1].tb_lineno}{Style.RESET_ALL}: {exception}")


def run_spider(url, level, path, recursive=False):
    # Requesting the html of the website page
    hdr = {'User-Agent': 'Mozilla/5.0'}
    proxy_host = '158.69.53.98:9300'

    try:
        http_data = Request(url, headers=hdr)
    except urllib.error.URLError as e:
        logger_error(f"{e.read().decode('utf8', 'ignore')}")
    # Parsing the html page with BeautifulSoup
    soup = BeautifulSoup(urlopen(http_data), features="html.parser")

    # Extract all images using the images object found in the parse html request
    extracting_images(url, level, path, soup, recursive)

if __name__ == "__main__":
    # Display program banner
    print_banner()

    # Signal Handler
    signal.signal(signal.SIGINT, signal_handler)

    # TO-DO: Parsing arguments using argparse
    parser = argparse.ArgumentParser(
        prog='./spider', description='The spider program allow you to extract all the images from a website, '
                                     'recursively, by providing a url as a parameter.')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively downloads the images in a URL received as a parameter.')
    parser.add_argument('-l', '--level', type=int, default=5, help='Indicates the maximum depth level of the '
                                                                   'recursive download. If not indicated, it will be '
                                                                   '5.')
    parser.add_argument('-p', '--path', type=str, default='./data/', help='Indicates the path where the downloaded '
                                                                          'files will be saved. If not specified, '
                                                                          './data/ will be used.')
    parser.add_argument('URL', type=str, help='URL to extract all the images recursively from.')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        os.mkdir(args.path)
    try:
        logger_info("Running with the following arguments.")
        logger_valid(f"{Style.BRIGHT}url: {Fore.BLUE}{args.URL}{Style.RESET_ALL}, level: {Fore.GREEN}{args.level}{Style.RESET_ALL}, path: {Fore.GREEN}{args.path}{Style.RESET_ALL}, recursive: {Fore.GREEN}{args.recursive}{Style.RESET_ALL}")
        validation = validators.url(args.URL)

        if not validation:
            raise ValueError(f"Url {Style.BRIGHT}{Fore.BLUE}{args.URL}{Style.RESET_ALL} is invalid.")
        run_spider(args.URL, args.level, args.path, args.recursive)
    except Exception as e:
        logger_error(f"on line {Fore.RED}{sys.exc_info()[-1].tb_lineno}{Style.RESET_ALL}: {e}")
# EOF
