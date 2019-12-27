from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
from scrapy.http import TextResponse
from scrapy.crawler import CrawlerProcess
import scrapy
import unicodecsv as csv
import requests
from datetime import date
from datetime import datetime

class Dice(scrapy.Spider):
    name = 'Dice'
    allowed_domains = ['dice.com']
    start_urls=['https://www.dice.com/jobs/q-Python-limit-120-l-New york,NY-radius-30-startPage-1-limit-120-jobs?searchid=291607343849']
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def parse(self, response):
        self.driver.get(response.url)
        urls = []
        properties_list = []
        for i in range(1,10):
            AllResult=self.driver.find_elements_by_class_name("complete-serp-result-div")
            i1=0
            for AR in AllResult:
                ii1=str(i1)
                path="//*[@id='position"+ii1+"']/span"
                path1="//*[@id='position"+ii1+"']"
                title=''
                
                try:
                    title=AR.find_element_by_xpath(path).text
                except Exception as d:
                    print('')
                link=''
                
                try:
                    link=AR.find_element_by_xpath(path1).get_attribute("href")
                except Exception as d:
                    print('')
                company=''
                
                try:
                    company=AR.find_element_by_class_name("compName").text
                except Exception as d:
                    print('')
                location=''
                
                try:
                    location=AR.find_element_by_class_name("jobLoc").text
                except Exception as d:
                    print('')
                posted_time=''
                try:
                    posted_time=AR.find_element_by_class_name("posted").text
                except Exception as d:
                    print('')
                description=''
                try:
                    description=AR.find_element_by_class_name("shortdesc").text
                except Exception as d:
                    print('')
        
                data = {'title' : title,'company':company,'location':location,'posted_time':posted_time,'description':description,'link':link}
                properties_list.append(data)
                i1=i1+1
            try:
                next_page = self.driver.find_element_by_xpath('//*[@title="Go to next page"]')
                next_page.click()
            except Exception as d:
                print('')
            # next_page = self.driver.find_element_by_xpath('//*[@title="Go to next page"]')
            # next_page.click()
        day = date.today().day
        hour = datetime.now().hour
        times = datetime.now().minute
        filename=str(day)+"-"+str(hour)+"-"+str(times)
        with open(""+filename+".csv" , 'wb') as csvfile:
            fieldnames = ['title','company','location','posted_time','description','link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in properties_list:
                writer.writerow(row)
        self.driver.close()

# Category=input("Enter Job Type You want to scrap : ")
# Location=input("Enter Job Location : ")
# URL=['https://www.dice.com/jobs/q-'+Category+'-limit-120-l-'+Location+'-radius-30-startPage-1-limit-120-jobs?searchid=291607343849']
process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
process.crawl(Dice)
process.start()
