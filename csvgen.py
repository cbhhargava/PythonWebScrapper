from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os

driver  = webdriver.Chrome("C:/Python27/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe")
print "Browser driver loaded"
driver.get("https://www.fpi.nsdl.co.in/web/Reports/Archive.aspx")
print "Page loaded"
assert "Archive" in driver.title
gdate = input("Please enter a date in dd-Mmm-yyyy format in Quotations \"\" - (Eg : \"31-Dec-2015\") : ")
print "Setting date"
driver.execute_script("document.getElementById('txtDate').setAttribute('value','" + gdate + "')")
driver.execute_script("document.getElementById('hdnDate').setAttribute('value','" + gdate + "')")
print "Done"
link = driver.find_element_by_link_text('Submit')
link.click()
print "Submitted"
assert "No results found." not in driver.page_source
content = driver.find_element_by_class_name("tbls01").get_attribute('innerHTML')
driver.close()
print "Read table data"

soup = BeautifulSoup(content)
table = soup.find('tbody')
headers = [header.text for header in table.find_all('th')]
rows = []
for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8') for val in row.find_all('td')])
print "Generating CSV"
with open(''+gdate+'.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)
print gdate+".csv saved at "+os.getcwd()
