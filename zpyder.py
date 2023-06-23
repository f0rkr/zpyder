#!/usr/bin/env python
import os.path
import sys
import traceback
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen, HTTPError
import urllib
import argparse
import re
import threading
import validators

allowed_extension = ['PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg', 'GIF', 'gif', 'BMP', 'bmp']


# -*- coding: utf-8 -*-
def print_banner():
    print('''
     ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄
    █       █       █   █      ██       █   ▄  █
    █  ▄▄▄▄▄█    ▄  █   █  ▄    █    ▄▄▄█  █ █ █
    █ █▄▄▄▄▄█   █▄█ █   █ █ █   █   █▄▄▄█   █▄▄█▄
    █▄▄▄▄▄  █    ▄▄▄█   █ █▄█   █    ▄▄▄█    ▄▄  █
     ▄▄▄▄▄█ █   █   █   █       █   █▄▄▄█   █  █ █
    █▄▄▄▄▄▄▄█▄▄▄█   █▄▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄▄█  █▄█

    Welcome to the Spider Program
    Author: f0rkr

    This program downloads all images recursively from a website,
    This program will only download images that have the following extensions: .jpg/jpeg, .png, .gif, and .bmp.
  ''')


# Get_encoding function
# Return the encoding type for the http response
def get_encoding(header):
    encoding = header['Content-Type'].split('charset=')[-1]
    return encoding


# Get_base_url function
# get the base url from the full url and returns it
def get_base_url(url):
    match = re.match(r'(https?://[^/]+)/?', url)
    if match:
        return match.group(1)
    else:
        return None


# Get_image_name function
# Returns image name from image_object using alt tag
# or else getting the name from the src url
def get_image_name(image_object):
    # filename = os.path.basename(''.join(random.choice(string.ascii_lowercase) for i in range(16)) + "." +
    # src.split('.')[-1])
    # if image_object.get('alt'):
    #     extension = image_object.get('src').split('.')[-1]
    #     image_name = image_object['alt'].replace(' ', '-').replace('/', '').split('.')[0]
    #     return image_name + "." + extension
    return os.path.basename(image_object['src'])


# Download_image function
# Get the url and image_object then it extract the image from
# the website and save it to a file
def download_image(url, image_object, path, level):
    filename = get_image_name(image_object)
    filepath = os.path.join(path, filename)
    full_url = urllib.parse.urljoin(url, image_object['src'])
    print("[+] LEVEL: {0} Downloading image: {1}, from url: {2}".format(level, filename, url))
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
                next_url = urllib.parse.urljoin(url, page['href'])
                print("NEXT URL: {0}".format(next_url))
                try:
                    run_spider(next_url, level - 1, path, recursive)
                except Exception as exception:
                    print("[?] Error: on line {0}: {1}".format(sys.exc_info()[-1].tb_lineno, exception))


def run_spider(url, level, path, recursive=False):
    # Requesting the html of the website page
    hdr = {'User-Agent': 'Mozilla/5.0'}
    proxy_host = '158.69.53.98:9300'

    http_data = Request(url, headers=hdr)

    # Parsing the html page with BeautifulSoup
    soup = BeautifulSoup(urlopen(http_data), features="html.parser")

    # Extract all images using the images object found in the parse html request
    extracting_images(url, level, path, soup, recursive)


if __name__ == "__main__":
    # Display program banner
    print_banner()

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
        print("[!] Running with the following arguments.")
        print("[+] url: {0}, level: {1}, path: {2}, recursive: {3}".format(args.URL, args.level, args.path,
                                                                           args.recursive))
        validation = validators.url(args.URL)

        if not validation:
            raise ValueError("Url {0} is invalid.".format(args.URL))
        run_spider(args.URL, args.level, args.path, args.recursive)
    except Exception as e:
        print("[?] Error: on line {0}: {1}".format(sys.exc_info()[-1].tb_lineno, e))
# EOF
