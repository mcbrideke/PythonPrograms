import requests
import json
from bs4 import BeautifulSoup

URL = 'https://catalog.ufl.edu/graduate/courses-az/'
page = requests.get(URL)
courses = []
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='textcontainer')
for link in results.find_all('a'):
    if str(link.get('href')).find('courses') != -1:
        courses.append('https://catalog.ufl.edu' + str(link.get('href')))
courseListingsInfo = []

for course in courses:
        coursePage = requests.get(course)
        soup = BeautifulSoup(coursePage.content, 'html.parser')
        courseListings = soup.find_all('p', class_='courseblocktitle noindent')
        for courseListing in courseListings:
            info = str(courseListing.text.strip()).split()
            i = 2
            courseTitle = ''
            while i < len(info)-3:
                courseTitle+=info[i]
                courseTitle+=' '
                i+=1
            courseTitle+=info[len(info)-3]
            reducedInfo = [info[0], info[1], courseTitle, info[len(info)-2]]
            # print(reducedInfo)
            courseListingsInfo.append(reducedInfo)
        

data = {}
data['courses'] = []

for courseListingInfo in courseListingsInfo:
    data['courses'].append({
        'course_code': courseListingInfo[0],
        'course_number': courseListingInfo[1],
        'course_name': courseListingInfo[2],
        'credits': courseListingInfo[3]
    })

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
