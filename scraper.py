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

now = datetime.now()
urlRoot = "dcjobs.com"
pagesToRead = 3 #change to process n pages
pageLinks = []
csvFile = str(now.date())+".csv"
titles = ['Data', 'Program', 'Manager', 'Business', 'Analyst', 'Engineer']
clearance = ['Security','Clearance','Certification']

print(os.getcwd())
print(os.listdir())

for i in range(0,pagesToRead+1):
  if i == 0:
    link = "https://www.dcjobs.com/jobs.asp?pagemode=20&domain_state_code=DC&location_name_1=Washington%2C+DC&location_id_1=528&location_type_1=C&qs_domain_id=33&keywords=&client_location_name_1=Washington%2C+DC"
  else:
    link = "https://www.dcjobs.com/jobs.asp?pagemode=13&nav=3&page="+str(i+1)+"&pf=1&agent_category_id=-1&pbid=-1&job_code=-1&category_id=&company_id=&job_type_id=3&city_id=-1&location_id_1=528&location_type_1=C&location_name_1=Washington,%20DC&location_radius_1=50&location_id_2=&location_type_2=&location_name_2=&location_radius_2=50&location_id_3=&location_type_3=&location_name_3=&location_radius_3=50&domain_id=-1&keywords=&order_by=relevance&direction=DESC&date_field=updated&changed=-1&is_staff_provider=-1&degree_id=&experience_years_min=-1&experience_years_max=-1&wage_class=-1&security_clearance_id=-1&co_id_int_list=&is_federal_contractor=-1"
  pageLinks.append(link)

for pageLink in pageLinks:
  pageSoup = pageResponse(pageLink)
  allPageLinks = pageSoup.find_all('a')

  jobLinks = []

  for pageLink in allPageLinks:
    pageHREF = pageLink.get('href')
    if '/job/detail/' in pageHREF:
      jobLinks.append(pageHREF)

  for jobLink in jobLinks:
    jobLinkToRead = "https://www."+urlRoot+jobLink+"/"
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