
# -*- coding: utf-8 -*-

import bs4, csv, os, time, re
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

usr = "janjansen@customerview.nl"
pwd = "facebook214"
count = 1

path = os.getcwd()

path = path + "\\chromedriver.exe"

with open("VarsScrapy.txt", 'r') as f:
    for line in f:
        line = line.strip()
        plaats, count = line.split(",")
        count = int(count)


        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        # prefs = {"profile.default_content_setting_values.notifications" : 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        chromeOptions.add_argument("--disable-extensions")
        driver = webdriver.Chrome(path, chrome_options=chromeOptions)

        driver.get("http://www.facebook.com")
        assert "Facebook" in driver.title
        elem = driver.find_element_by_id("email")
        elem.send_keys(usr)
        elem = driver.find_element_by_id("pass")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)

        driver.get("http://www.facebook.com/search/in-future/date/events/str/" + plaats + "/pages-named/events-at/intersect/")


        def convert(string):

            s = string.replace("{", "");
            finalstring = s.replace("}", "");

            # Splitting the string based on , we get key value pairs
            lists = finalstring.split(",")

            dict = {}
            for i in lists:
                # Get Key Value pairs separately to store in dictionary
                keyvalue = i.split(":")

                # Replacing the single quotes in the leading.
                try:
                    m = keyvalue[0].strip('\'')
                    m = m.replace("\"", "")
                    dict[m] = keyvalue[1].strip('"\'')
                except IndexError:
                    continue
            return dict


        csv_header = ("ID")

        for ix in range(count):
            driver.execute_script("window.scrollTo(0, 126000);")
            # time.sleep(5)
            time.sleep(3)

        innerHTML = driver.execute_script("return document.body.innerHTML")
        htmlCode = bs4.BeautifulSoup(innerHTML, "lxml")

        data1 = htmlCode.select('div[style="-webkit-line-clamp: 2;"] a')
        data2 = htmlCode.select('div[class="_pac"]')
        # data3 = htmlCode.select('div[class="_52eh"]')
        data4 = htmlCode.select('div[class="_3u1 _gli _uvb"]')

        driver.quit()

        for j in range(len(data1)):
            # link = 'facebook.com' + data1[j].attrs['href']
            # name = data1[j].getText()
            # details = data2[j].getText()
            # interest = data3[j].getText()
            idd = data4[j].attrs['data-bt']
            idd1 = convert(idd)
            idd2 = idd1['id']
            # var = ([idd2, name, link, details])
            var = ([idd2])
            try:
                # with open("output.csv", 'a', newline='', encoding="iso-8859-1") as f:
                with open("output.csv", 'a', newline='', encoding="cp1252") as f:

                    writer = csv.writer(f)
                    writer.writerow(var)

            except UnicodeEncodeError:
                sss1 = re.compile(r'‘')
                sss2 = re.compile(r'’')
                sss3 = re.compile(r'“')
                sss4 = re.compile(r'”')
                name = sss1.sub("\'", name)
                name = sss2.sub("\'", name)
                name = sss3.sub("\'", name)
                name = sss4.sub("\'", name)
                var = ([name, idd2, link, details])
                # with open("output.csv", 'a', newline='', encoding="iso-8859-1") as f:
                with open("output.csv", 'a', newline='', encoding="cp1252") as f:
                    writer = csv.writer(f)
                    writer.writerow(var)
