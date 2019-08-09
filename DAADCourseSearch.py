from selenium import webdriver
import csv
from time import sleep
import math
from os import stat,path
keyword = input('Enter your desired course Name: ')

fileName = 'uni.txt'
if(path.exists(fileName) and stat(fileName).st_size > 0 ):
    f = open(fileName,'w')
    f.write('')
    f.close()

URL = 'https://www.daad.de/deutschland/studienangebote/international-programmes/en/result/?q='+keyword+'&degree[]=2&lang[]=2&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn[]=&cit[]=&tyi[]=1&ins[]=&fee=0&bgn[]=&dur[]=&sort=4&subjects[]=&limit=10&offset=&display=list'

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(options=option)
driver.get(URL)
sleep(5)
next_url_selector = '//*[@id="result-list"]/div/div[2]/div/div/div[2]/a[2]'

number_of_course_selector = '#searchForm > div:nth-child(3) > div > div > div > div > h2'

def course_finder():
    numberOfCourses = driver.find_element_by_css_selector(number_of_course_selector)
    print(numberOfCourses.text)
    numberYouWant = input('How many results do you need : ')
    for i in range(0,math.ceil(int(numberYouWant)/10)):
        courseNames = driver.find_elements_by_css_selector('#result-list > div > div:nth-child(1) > div > div.c-result-list__content.c-masonry.js-result-list-content > div > div > div > div > div > div > div.col-12.c-ad-carousel__content.c-ad-carousel__content > div > a > span.c-ad-carousel__title.c-ad-carousel__title--small')
        uniNames = driver.find_elements_by_css_selector('.position-relative > div > div:nth-child(1) > div > div.c-result-list__content.c-masonry.js-result-list-content > div > div > div > div > div > div > div.col-12.c-ad-carousel__content.c-ad-carousel__content > div > a > span:nth-child(2)')

        links = driver.find_elements_by_css_selector('#result-list > div > div:nth-child(1) > div > div.c-result-list__content.c-masonry.js-result-list-content > div > div > div > div > div > div > div.col-12.c-ad-carousel__content.c-ad-carousel__content > div > a')

        names = [name.text.strip('•') for name in uniNames]
        cnames= [cname.text.strip('•') for cname in courseNames]
        courseLinks= [x for x in links]

        with open('uni.txt', 'a+') as uni:
            for name,cname,courseLink in zip(names,cnames,courseLinks):
                uni.write(f"University Name : {name}\n")
                uni.write(f"Course Name: {cname}\n")
                uni.write(f"URL:  {courseLink.get_attribute('href')}\n")
                uni.write("\n")
        driver.find_element_by_xpath(next_url_selector).click()
        sleep(5)

if __name__=='__main__':
    course_finder()
    driver.close()
    print('Succeed')
