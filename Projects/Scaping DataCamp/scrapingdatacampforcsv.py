### A python script to collect all of the .csv files from DataCamp ###
### and copy them to a folder named Data in the currect directory. ###
### Created 3/3/18 by David coxon ###

# Import packages
import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd

codebook='Data/Csv/importedcsv.txt'
now = datetime.datetime.now()
now = str(now)
# Specify url
url = 'https://www.datacamp.com/courses'
# Package the request, send the request and catch the response: r
r = requests.get(url)
html_doc = r.text

# create a BeautifulSoup object from the HTML: soup
soup = BeautifulSoup(html_doc, "lxml")

# Find all 'a' tags (which define hyperlinks): a_tags
a_tags=soup.find_all('a')

# Extract the /courses pages
courses=[]
pattern = re.compile("/courses//*")
for link in a_tags:
    match = re.findall(pattern, str(link))
    if match:
        courses.append(link.get('href'))   

# iterate over list of courses getting links to csv files
csv=[]     
for course in courses:    
    
    # Specify url
    url = "https://datacamp.com"+course    
    # Package the request, send the request and catch the response: r
    r = requests.get(url)
    # Extracts the response as html: html_doc
    html_doc = r.text

    # create a BeautifulSoup object from the HTML: soup
    soup = BeautifulSoup(html_doc, "lxml")
    
    # Find all 'a' tags (which define hyperlinks): a_tags
    a_tags1=soup.find_all('a')

    # append the URLs to csv list
    pattern = re.compile("csv/*")        
    for link in a_tags1:
        match = re.findall(pattern, str(link))
        if match:
            csv.append(link.get('href')) 

# open Csv files and copy to Local device           
for file in csv:
    y=file.split('/')
    destination='Data/Csv/'+(y[-1])
    df=pd.read_csv(file)
    df.to_csv(destination)

    # Document which files were collected
    with open(codebook, "a") as f:
        f.write("\nsource : " + file + " dated collected : " + now)
print(str(len(csv)) + " csv files checked!")