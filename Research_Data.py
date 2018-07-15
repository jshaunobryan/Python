# This script looks at a webpage with search results, copies the source
# code, writes it to a text file, and then looks for elemets within the HTML
# with a designated tag and returns the contents to a formatted spreadsheet

#import modules

import selenium, time
import html5lib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# Open chrome
br = webdriver.Chrome()

# 
raw_input("Navigate to search resutls page and then type ready into here: ")
# write initial results to 
pg_src = br.page_source.encode("utf")

soup = BeautifulSoup(pg_src) 

# get the max page number from the search results

max_page = soup.find('span',{'class':'data-page-max'}).text
print max_page

maxPgNum = int(max_page)
#open a text doc to write the results to
print pg_src

f = open(r'C:\Users\user\Documents\GIS DataBase\web_resutls_raw_new.html', 'w')

# write results pag by page until max page number is reached

pg_cnt = 1 # start on 1 since as we should already have the first page
while pg_cnt < maxPgNum:
	f.write(str(pg_src))
	time.sleep(5)
	pg_cnt +=1
	br.find_element_by_xpath("//*[@id='searchResults']/div[1]/div/div[1]/div[2]/div[3]").click()
	time.sleep(5)
	pg_src = br.page_source.encode("utf") 

f.close()

f1 = open(r'C:\Users\user\Documents\GIS DataBase\web_resutls_raw_refined.txt', 'w')
data = open(r"C:\Users\user\Documents\GIS DataBase\web_resutls_raw_new.html",'r').read()
soup = BeautifulSoup(str(data), 'html.parser')
tbl = soup.findAll('tbody', id='searchResultsPage')
soup = BeautifulSoup(str(tbl))
res = soup.text
x = res.replace('\\n','|')
y = x.replace('Check Box','*')
records = y
print "hey"
records = records[1:]
records = records[:-1]
records = records.split("*")
for rec in records:
	f1.write(rec + "\n")
f1.close()

print "Done sucka!"

