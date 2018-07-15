# This script looks at a webpage with search results, copies the source
# code, writes it to a text file, and then looks for elemets within the HTML
# with a designated tag and returns the contents to a formatted spreadsheet

#import modules

import re
import selenium, time
import html5lib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import string

# open chrome
br = webdriver.Chrome()

# make a list for search criteria - This wikipedia page sorts pages alphabetically
SrLst = list(string.ascii_uppercase)
print SrLst

# make the basename for the url - the script will loop through the SrLst and place each element at the end of this for a complete url
urlBase = r"https://en.wikipedia.org/w/index.php?title=Category:Unincorporated_communities_in_California&from="
comLst = []
crdLst = []
f = open(r"C:\Users\user\Documents\GIS DataBase\com_coords.txt", 'w')
nuBase = r"https://en.wikipedia.org"



# loop through the A-Z pages
for letter in SrLst:
	url = urlBase + letter
	br.get(url)
	pg_src = br.page_source.encode("utf")
	soup = BeautifulSoup(pg_src, "lxml")
	hrefLst = soup.find_all(href=re.compile(",_California"))
	lnkLst = []
	nuLst = []
	for i in hrefLst:
		lnkLst.append(i.get('href'))
	for i in lnkLst:
		if i.split("/")[2].startswith(letter): # This gets rid of communities starting with the next letter in the list that are on the same index page
			nuLst.append(i)
	# Loop through the community pages for the current letter
	for i in nuLst:
		comLst.append(i.split("/")[2]) # this splits up the format /wiki/community_name,_California so it just includes comunity_name,_California
		url = nuBase + str(i) # this constructs the community url
		br.get(url)
		pg_src = br.page_source.encode("utf")
		soup = BeautifulSoup(pg_src) 
		x = soup.select_one("span[class='geo']") # These are where the coordinates are stored
		crdLst.append(x)

z = zip(comLst, crdLst)
for i in z:
	f.write(str(i) + "\n")
f.close()

print "Done sucka!"

