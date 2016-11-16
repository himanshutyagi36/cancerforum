__author__ = 'tyagi'
import scrapy
import MySQLdb
import time
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from cancerforum.items import PostItem
from selenium.webdriver.common.by import By

def IsElementPresent(self,locater):
    try:
        self.browser.find_element_by_xpath(locator)
    except NoSuchElementException:
        print ('No such thing')
        return False
    return True
class PostSpider(scrapy.Spider):
    name = "post_spider"
    allowed_domains=["cancerforums.net"]
    start_urls = [
        "http://www.cancerforums.net/forums/14-Prostate-Cancer-Forum"
    ]
    def __init__(self,*args,**kwargs):
        print("------------inside init----------")
        self.browser = webdriver.Firefox()
        self.browser.get("http://www.cancerforums.net/forums/14-Prostate-Cancer-Forum")
        self.db = MySQLdb.connect("localhost","root","1590","cancerforum")
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT frontPage.thread_title_link FROM frontPage;")
    def __exit__(self):
		print "------------Exiting----------"
		self.browser.quit()
    def __exit__(self):
		print "------------Exiting----------"
		self.browser.quit()

    def parse(self,response):
        item = PostItem()
        for temp in self.cursor.fetchall():
            try:
                link = temp[0]
                self.browser.get(link)
                print (link)
                time.sleep(5)
                navigation_flag = 0
                try:
                    temp = self.browser.find_element_by_xpath("//div[@class='pagination_top']").text.encode("utf-8")
                    temp = temp.split("\n")
                    temp1 = temp[0].split(" ")
                    l = len(temp1)
                    counter = int(temp1[l-1])
                    nextpage = self.browser.find_element_by_xpath("//a[@rel='next']").get_attribute('href')
                    navigation_flag = 1
                except NoSuchElementException:
                    counter = 1
                    pass
                # print "******************"+str(counter)+"*****************"
                for j in range(0,counter):
                    posts_list = self.browser.find_elements_by_xpath('//div[@class="postdetails"]')
                    dateNtime_list = self.browser.find_elements_by_xpath("//span[@class='postdate old']")
                    try:
                        for i in range(0,len(posts_list)):
                            tempList = dateNtime_list[i].text.encode("utf-8")
                            tempList = tempList.split(',')
                            postDate = tempList[0]
                            postTime = tempList[1]
                            # content_list = posts_list[i].find_elements_by_xpath('.//div[@class="content"]')
                            # post_content = content_list[0].text.encode("utf-8")
                            post_content = posts_list[i].find_elements_by_xpath('.//div[@class="postbody"]')[0].find_element_by_xpath('.//div[@class="content"]').text.encode("utf-8")
                            # signature_contentList = posts_list[i].find_elements_by_xpath('.//div[@class="signaturecontainer"]')
                            # signature_content = signature_contentList[0].text.encode("utf-8")
                            try:
                                signature_content = posts_list[i].find_elements_by_xpath('.//div[@class="postbody"]')[0].find_element_by_xpath('.//div[@class="after_content"]').text.encode("utf-8")
                            except NoSuchElementException:
                                print "------------Inside Signature Content Exception--------------"
                                signature_content = ""
                                pass
                            print "------------outside signature content exception-----------"
                            username = posts_list[i].find_element_by_xpath(".//a[starts-with(@class, 'username')]").text.encode("utf-8")
                            userlink = posts_list[i].find_element_by_xpath(".//a[starts-with(@class, 'username')]").get_attribute('href').encode('utf-8')
                            try:
                                usertitle = posts_list[i].find_element_by_xpath(".//span[@class='usertitle']").text.encode("utf-8")
                            except NoSuchElementException:
                                print "-------------inside user title exception------------"
                                usertitle=""
                                pass
                            userrank = posts_list[i].find_element_by_xpath(".//span[@class='rank']").text.encode("utf-8")
                            user_joindate = posts_list[i].find_elements_by_xpath('.//dd')[0].text.encode("utf-8")
                            # user_location = posts_list[i].find_elements_by_xpath('.//dd')[1].text.encode("utf-8")
                            # try:
                            #     user_NumberOfPosts = posts_list[i].find_elements_by_xpath('.//dd')[2].text.encode("utf-8")
                            # except NoSuchElementException:
                            #     user_NumberOfPosts=0
                            #     pass
                            temp = posts_list[0].find_element_by_xpath(".//dl[@class='userinfo_extra']").text.encode("utf-8")
                            temp = temp.split("\n")
                            if temp[0]=='Join Date':
                                user_joindate = temp[1]
                            else:
                                user_joindate="Not Found"
                            if temp[2]=='Posts':
                                user_NumberOfPosts = temp[3]
                                user_location = "Not Found"

                            else:
                                user_location = temp[3]
                                user_NumberOfPosts = temp[5]
                            print postDate
                            print postTime
                            print username
                            print userlink
                            print usertitle
                            print userrank
                            print user_joindate
                            print user_location
                            print user_NumberOfPosts

                            item['postDate'] = postDate
                            item['postTime'] = postTime
                            item['post_content'] = post_content
                            item['signature_content'] = signature_content
                            item['username'] = username
                            item['userlink'] = userlink
                            item['usertitle'] = usertitle
                            item['userrank'] = userrank
                            item['user_joindate'] = user_joindate
                            item['user_location'] = user_location
                            item['user_NumberOfPosts'] = user_NumberOfPosts
                            yield item
                            print "------------------Items yieled to database--------------"
                    except NoSuchElementException:
                        print "---------Exception in inner for loop--------"
                        continue
                    ## Navigate to the other pages containing threads lists.
                    if navigation_flag == 1:
                        self.browser.get(nextpage)
                    else:
                        continue
            except NoSuchElementException:
                print "---------Element not found-----------"
                continue
            # self.browser.quit()
