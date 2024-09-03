import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def pageResponse(link):
  response = requests.get(pageLink)
  if response.status_code == 200:
    return BeautifulSoup(response.text, 'html.parser')
  else:
    return(f"Failed to retrieve the webpage. Status code: {response.status_code}")

i = 0 
j = 0
now = datetime.now()
urlRoot = "diversityjobs.com"
pagesToRead = 5 #change to process n pages
pageLinks = []
jobLinks = []
csvFile = str(now.date())+".csv"
titles = ['Data', 'Program', 'Manager', 'Business', 'Analyst', 'Engineer']
clearance = ['Security','Clearance','Certification']

for j in range(0,pagesToRead+1):
  if j == 0:
    link = "https://diversityjobs.com/candidate/job_search/quick/results?&f642=8qzstzs5yv&f28=1481&f714=2297&f70=120m"
  else:
    link = "https://diversityjobs.com/candidate/job_search/quick/results/"+str(j+1)+"?&f642=8qzstzs5yv&f28=1481&f714=2297&f70=120m"
  j += 1
  pageLinks.append(link)

for pageLink in pageLinks:
  pageSoup = pageResponse(pageLink)
  allPageLinks = pageSoup.find_all('a')

  for pageLink in allPageLinks:
    #print(pageLink)
    try:
      pageHREF = pageLink.get('href')
      if '/career/' in pageHREF:
        jobLinks.append(pageHREF)
    except:
      continue
  
#jobs
for jobLink in jobLinks:
  jobLinkToRead = "https://www."+urlRoot+jobLink
  response = requests.get(jobLinkToRead)
  soup = BeautifulSoup(response.text, 'html.parser')

  jobTitle = soup.find('title').getText()

  if not any(word in jobTitle for word in titles):
    continue

  jobText = soup.getText()

  if any(word in jobText for word in clearance):
    continue
  
  data = [str(i),now,jobTitle,jobLinkToRead]

  with open(csvFile, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data)

  print(str(i), now, jobTitle, jobLinkToRead)

  i += 1