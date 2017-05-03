#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task in this exercise is to modify 'extract_carrier()` to get a list of
all airlines. Exclude all of the combination values like "All U.S. Carriers"
from the data that you return. You should return a list of codes for the
carriers.

All your changes should be in the 'extract_carrier()' function. The
'options.html' file in the tab above is a stripped down version of what is
actually on the website, but should provide an example of what you should get
from the full file.

Please note that the function 'make_request()' is provided for your reference
only. You will not be able to to actually use it from within the Udacity web UI.
"""
import requests
import os
from bs4 import BeautifulSoup
html_page = "flightsandcarriers.html"

site = 'https://www.transtats.bts.gov/Data_Elements.aspx?Data=2'

# Download site
def get_data(site):
  r = requests.get(site)
  soup = BeautifulSoup(r.text, 'html.parser')

  with open('flightsandcarriers.html','w') as f:
    f.write(r.text)

get_data(site)

# Build a list of all carrier and airport values
def extract_carriers(html_page):
    data = []

    with open(html_page, "r") as html:
        soup = BeautifulSoup(html, "html.parser") #, "lxml")
        carrier_list = soup.find(id = "CarrierList") # returns one element 
        b = carrier_list.find_all("option") # returns a result set of elements with the tag 'option'
        for item in b:
          data.append(item['value'])
    return data[3:]

#print extract_carriers(html_page)

def extract_airports(html_page):
    data = []
    with open(html_page, "r") as html:
        soup = BeautifulSoup(html, "html.parser")#"lxml")
        airport_list = soup.find(id = "AirportList")
        b = airport_list.find_all("option")
        for item in b:
          if len(item['value']) == 3:
            data.append(item['value'])
    return data[1:]

#print extract_airports(html_page)

# Get post info
def extract_post(site):
  s = requests.Session()

  r = s.get(site)
  soup = BeautifulSoup(r.text, 'html.parser')

  viewstate = soup.find(id = '__VIEWSTATE')['value']
  event_validation = soup.find(id = '__EVENTVALIDATION')['value']
  return viewstate, event_validation



def data_dict(html_page, site):
  data_dict = {}
  data_dict['airport'] = extract_airports(html_page)
  data_dict['carrier'] = extract_carriers(html_page)
  data_dict['eventvalidation'] = extract_post(site)
  data_dict['viewstate'] = extract_post(site)
  return data_dict

#print data_dict(html_page, site)

def make_request(data):
    output_path = ''

    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    
    for airport in data["airport"]:
      for carrier in data["carrier"]:
        s = requests.Session()
        r = s.post("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                   data = (("__EVENTTARGET", ""),
                           ("__EVENTARGUMENT", ""),
                           ("__VIEWSTATE", viewstate),
                           #("__VIEWSTATEGENERATOR",viewstategenerator),
                           ("__EVENTVALIDATION", eventvalidation),
                           ("CarrierList", carrier),
                           ("AirportList", airport),
                           ("Submit", "Submit")))
        fileName = "{}-{}.html".format(carrier, airport)
        with open(os.path.join('data',fileName), "w") as f:
          f.write(r.text)

make_request(data_dict(html_page, site))

'''
def test():
    data = extract_carriers(html_page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data

if __name__ == "__main__":
    test()

'''