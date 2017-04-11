#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import sys

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv[1])
# url_input = ""

try:
    url_input = str(sys.argv[1])
except:
    print "Error in arguments. Set the url to scrawl as first argument"
    exit(-1)

outfile = open('cars_more.csv', 'w')
outfile.write('MODEL;PRICE;LOCATION;YEAR;DETAIL_1;DETAIL_2;DETAIL_3;DETAIL_4;DETAIL_5;\n')

totalCarsScrapped = 0
## Looping two links...
for url_page in range(3038, 3041):
    # print url_page

    websiteUrl = url_input + repr(url_page)
    #print repr("Scrapping ") + websiteUrl
    try:
        reqToWeb = requests.get(websiteUrl)
        #reqToWeb = requests.get("http://www.mierdaquenovaestecodi.com")
        if reqToWeb.status_code != 200:
            print "No OK Response for " + " Response code -> " + repr(reqToWeb.status_code)
            print "Failed loop page was  " + repr(url_page)
            exit(1)
    except requests.exceptions.ConnectionError as e:
        print "No connection -> " + repr(e.message)
        exit(-1)

    #print "Headers -> " + str(reqToWeb.request.headers)

    # Get HTTP content
    # reqToWeb.content

    # HTML object
    soup = BeautifulSoup(reqToWeb.content, "html.parser")

    # Easy to read code
    # print soup.prettify()

    allCars = soup.find("div", {"id": "listingData"})
    # for index, car_item in enumerate(allCars, start=0):
    # print(index, item)

    #for index, car_item in enumerate(allCars.contents, start=0):
    for car_item in allCars.contents:

        # Skipping empty divs...
        if(car_item == "\n"):
            continue
        skip = None

        # Skipping promoted ads
        for className in car_item.attrs['class']:
            if(className == "upsellAd"):
                skip = True
                break

        if(skip):
            continue

        car_data_found = car_item.find_all("div", {"class", "width_full"})
        if(len(car_data_found) == 0 ):
            continue

        div_widthFull = car_item.find_all("div", {"class", "width_full"})[0]
        carItem = div_widthFull.find_all("div", {"class", "data_box"})[0]

        car_model = carItem.find_all("div", {"class", "make_model_link"})[0].text
        #print repr("Model ") + car_model

        car_more_data = carItem.find_all("div", {"class", "clearfix_nett"})[0]
        price = car_more_data.find_all("div", {"class", "price_block"})[0].find_all("div", {"class", "main_price"})[0].text
        price = price[:-2]
        #print repr("Price ") + price

        car_localization = car_more_data.find_all("div", {"class", "info_block"})[0].find_all("div", {"class", "location_info cleafix_nett"})[0].find_all("span", {"class", "list_seller_info"})[0].find_all("b", {"class", "gray_text"})[0].text
        car_localization = car_localization[:-2]
        #print repr("Location ") + car_localization

        car_specs = car_more_data.find_all("div", {"class", "info_block"})[0].find_all("div", {"class", "vehicle_other_info clearfix_nett"})[0].find_all("ul")[0]
        car_details = car_specs.find_all("li")

        outfile.write('%s;%s;%s;' % (car_model.encode('utf-8').strip(), price.encode('utf-8').strip(), car_localization.encode('utf-8').strip()))

        detail_num = 1
        for detail in car_details:
            #print repr("Detail ") + repr(detail_num) + " " + detail.text
            outfile.write('%s;' % (detail.text))
            detail_num += 1

        outfile.write('\n')

        totalCarsScrapped += 1
        #print ""

    # Random time 5secs
    sleeping_time = 3
    # print repr("Stopping thread " + repr(sleeping_time) + " secs")
    print repr("UTM - Total cars scrapped ") + repr(totalCarsScrapped) + " loop -> " + str(url_page)
    time.sleep(sleeping_time)  # delays for 3 seconds
    # print repr("Resuming thread")

print repr("END - Total cars scrapped ") + repr(totalCarsScrapped)
