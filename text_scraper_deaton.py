import urllib2
import urllib
import os
from bs4 import BeautifulSoup
from unidecode import unidecode

##############################################
# This script is used to scrape all papers 
# from economics professor Angus Deaton
##############################################

# assign url where all papers are listed to URL
URL = "http://scholar.princeton.edu/deaton/publications"

# Top-level domain where all papers are stored
TOP = "http://scholar.princeton.edu"

# Get current directory. Will be used later
DIR = os.getcwd()

# Start Souping ####################################
# Note: Note that BeautifulSoup usually can't read
# websites that don't end in .html - you need to use 
# urllib2 first to retrieve the HTML behind them. 
def Soupify(url):
	soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
	return soup

first_soup = Soupify(URL)
print first_soup.title

# See some functions we can use with soup
print "Our soup has " + str(len(dir(first_soup))) + " possible methods or attributes we can use with it. Wow!\n"
print "A few of them are: " + str(dir(first_soup)[15:20])

# Test some of the functions ####
# Check the <p> paragraph element
print first_soup.find_all("p")[1]

# get rid of html code
print first_soup.find_all("p")[1].text

#unidecode
print unidecode(first_soup.find_all("p")[1].text)

# Now get all paper links
links = first_soup.find_all("a")
print "There are " + str(len(links)) + " links here."

# Check
for link in links[0:10]:
	print link

# filter only links to publications page
def getPaperLinks(soup):
	# Save list of all spans of class "biblio-title
	# Should only be paper
	spans = soup.find_all(class_="biblio-title")

	# Empty array to put paper urls
	paper_links = []

	# Loop through each span, pull out <a> element, and add to paper_link
	for span in spans:
		link = span.find("a").get("href")
		paper_links.append(link)

	return paper_links

first_set_of_links = getPaperLinks(first_soup)

# Check if worked
print TOP + first_set_of_links[0]

#Create a list of all PDF links
def getPDFLinks(paper_links):
	# create empty array to hold pdf links
	pdfs = []

	# loop through all publication pages
	for link in paper_links:

		#soupify link
		link_soup = Soupify(TOP + link)

		# get links from that soup
		link_links = link_soup.find_all("a")

		# save pdf link to pdf list
		for pdf in link_links:
			if pdf.get("href") and "pdf" in pdf.get("href"):
				pdfs.append(str(pdf.get("href")))
	
	return pdfs

list_of_pdfs = getPDFLinks(first_set_of_links)

# Check
print list_of_pdfs[0:4]

## Look through PDFs, save to machine, strip text
def stripText(pdf_list, directory):
	# empty array to put pdf text
    text = []

    for pdf in pdf_list:
        if pdf[0:4]!= "http":
            pdf = TOP + pdf

        try:
            urllib2.urlopen(pdf)
            urllib.urlretrieve(pdf, directory + "/paper.pdf")

            # strip text  
            os.system("pdf2txt.py -o paper.txt -t text paper.pdf")
            raw = open(directory + "/paper.txt").read()
            text.append(raw)

        except:
            print "Problem with opening the URL."

    if os.path.isfile(directory + "/paper.pdf"):
        os.remove(directory + "/paper.pdf") 
    if os.path.isfile(directory + "/paper.txt"):
        os.remove(directory + "/paper.txt")
    
    return text

corpus = stripText(list_of_pdfs, DIR)

print len(corpus)




