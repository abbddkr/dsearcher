#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import random 
from progressbar import ProgressBar
import sys

#define usage
def usage():
	print("dsearcher.py [-k]")
	print("-k  Keyword: can be anything like username or etc..")

# define sys.argv

arg = sys.argv

# define progress bar
progsessbar = ProgressBar()


# flickr function
# website functions
def flickr():
	page = requests.get("https://www.flickr.com/search/?text="+arg[2]+'&view_all=1')
	soup = BeautifulSoup(page.content, 'html.parser')
	#print(soup.prettify())
	userDir = arg[2]
	html = list(soup.children)[2]
	img = soup.find_all('div',{"class":"photo-list-photo-view"})
	if os.path.isdir(userDir):
			os.chdir(userDir)
	else:
			os.mkdir(userDir)
			os.chdir(userDir)        
	for allimgs in progsessbar(img):
			styleSource = allimgs.get('style')
			getImg = styleSource.find('url(')
			fullImg = styleSource[4+getImg:-1:]
			urllib.request.urlretrieve(fullImg,fullImg[-10:])

def yahoo():
	page = requests.get("https://images.search.yahoo.com/search/images?p="+arg[2])
	soup = BeautifulSoup(page.content, 'html.parser')
	#print(soup.prettify())
	html = list(soup.children)[2]
	img = soup.find_all('img',{"class":"process"})
	for allimgs in progsessbar(img):
			html_content = str(allimgs)
			findSrc = html_content.find('src=')
			findStyle = html_content.find('style')
			rmExtra   = html_content.find('&amp;pid=Api&amp;P=0&amp;w=300&amp;h=300')
			fullImg = html_content[findSrc:findStyle][5:-2]
			save = urllib.request.urlretrieve(fullImg[:-40],fullImg[40:]+'.png')

# if first arg == user and arg == website
try:
	if arg[1] == "-k":
		if arg[2] != "":
			flickr()
			yahoo()
# call the website function
except:
	usage()
