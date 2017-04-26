import requests
from bs4 import BeautifulSoup

s = requests.Session()

r = s.get('https://www.transtats.bts.gov/Data_Elements.aspx?Data=2')
soup = BeautifulSoup(r.text, 'html.parser')

#print r.text # string of text

viewstate_element = soup.find(id = '__VIEWSTATE')
viewstate = viewstate_element['value']
event_validation_element = soup.find(id = '__EVENTVALIDATION')
event_validation = event_validation_element['value']

r = s.post('https://www.transtats.bts.gov/Data_Elements.aspx?Data=2',
                    data = {'AirportList' : "BOS",
                    'CarrierList' : "VX",
                    'Submit' : 'Submit',
                    '__EVENTTARGET' : '',
                    '__EVENTARGUMENT' : '',
                    '__EVENTVALIDATION' : event_validation,
                    '__VIEWSTATE' : viewstate
                    })

#print r.text
f = open('virgin_and_logan_airport2.html','w')
f.write(r.text)
