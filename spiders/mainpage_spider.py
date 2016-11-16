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
from cancerforum.items import CancerForumItem

class CancerForumSpider(scrapy.Spider):
	name = "mainpage_spider"
	allowed_domains = ["cancerforums.net"]
	start_urls = [
		"http://www.cancerforums.net/forums/14-Prostate-Cancer-Forum"
	]
	def __init__(self,*args,**kwargs):
		print("----------------inside init----------------")
		self.browser=webdriver.Firefox()
		self.browser.get("http://www.cancerforums.net/forums/14-Prostate-Cancer-Forum")
		print "----------------Going to sleep------------------"
		time.sleep(5)


	def __exit__(self):
		print "------------Exiting----------"
		self.browser.quit()

	def parse(self,response):
		print "----------------Inside Parse------------------"
		item = CancerForumItem()
		temp = self.browser.find_element_by_xpath("//div[@class='threadpagenav']").text.encode("utf-8")
		temp = temp.split("\n")
		temp1 = temp[0].split(" ")
		l = len(temp1)
		counter = int(temp1[l-1])
		## this for loop navigates between the head forum pages (1-99)
		for j in range(0,counter):
			print "----------------"+str(j)+"-----------------"
			sticky_list = self.browser.find_elements_by_xpath('//div[@class="rating0 sticky"]')
			for i in range(0,len(sticky_list)):
				try:
					thread_data=[]
					# thread_title = thread_list[i].find_element_by_xpath('//a[@class="title"]').text.encode("utf-8")
					thread_title = sticky_list[i].find_element_by_xpath('.//h3[@class="threadtitle"]').text.encode("utf-8")
					# print thread_title
					thread_title_link = sticky_list[i].find_element_by_xpath('.//a[@class="title"]').get_attribute('href').encode("utf-8")
					authorCol = sticky_list[i].find_element_by_xpath('.//div[@class="author"]').text.encode("utf-8")
					author = authorCol.split()[2].strip(',')
					# print author
					author_link = sticky_list[i].find_element_by_xpath('.//a[@class="username understate"]').get_attribute('href').encode('utf-8')
					## get the raw data for replies tab. ( In the format of "Replies: 82")
					meta_raw = sticky_list[i].find_element_by_xpath('.//ul[@class="threadstats td alt"]').text.encode("utf-8")
					## get the replies and views string in meta list
					meta = meta_raw.split('\n')
					## break the string based on ':' operator. Get the second entry and strip of whitespace to get the number of replies.
					if len(meta)>0:
						replies = meta[0].split(':')[1].strip()
						views = meta[1].split(':')[1].strip()
					else:
						replies=0
						views=0
					# print views
					lastuser_meta =sticky_list[i].find_element_by_xpath('.//dl[@class="threadlastpost td"]')
					lastuser = lastuser_meta.find_element_by_xpath('.//dd').text.encode("utf-8")
					lastuser_link = lastuser_meta.find_element_by_xpath('.//a[@class="username offline popupctrl"]').get_attribute('href').encode("utf-8")
					lastpost_link = lastuser_meta.find_element_by_xpath('.//a[@class="lastpostdate understate"]').get_attribute('href').encode("utf-8")
					lsm_text = lastuser_meta.text.encode("utf-8")
					lastpost_datetime = lsm_text.split('\n')[1]

					item['thread_title'] = thread_title
					item['thread_title_link'] = thread_title_link
					item['author'] = author
					item['replies'] = replies
					item['views'] = views
					item['lastuser'] = lastuser
					item['lastuser_link'] = lastuser_link
					item['lastpost_link'] = lastpost_link
					item['lastpost_datetime'] = lastpost_datetime
					yield item
					# thread_data.append(thread_title)
					# thread_data.append(thread_title_link)
					# thread_data.append(author)
					# thread_data.append(replies)
					# thread_data.append(views)
					# thread_data.append(lastuser)
					# thread_data.append(lastuser_link)
					# thread_data.append(lastpost_link)
					# thread_data.append(lastpost_datetime)
					#
					# ## write to csv file
					# with open("mainpage.csv",'a') as csvfile:
					# 	filewriter = csv.writer(csvfile,quoting=csv.QUOTE_ALL)
					# 	filewriter.writerow(thread_data)
					# csvfile.close()

				except NoSuchElementException:
					print "---------Element not found(Sticky list)-----------"
					pass

			thread_list = self.browser.find_elements_by_xpath('//div[@class="rating0 nonsticky"]')
			for i in range(0,len(thread_list)):
				try:
					thread_title = thread_list[i].find_element_by_xpath('.//h3[@class="threadtitle"]').text.encode("utf-8")
				except NoSuchElementException:
					print "---------Element not found - Thread Title-----------"
					thread_title = "Not Found"
					pass
				print thread_title
				try:
					thread_title_link = thread_list[i].find_element_by_xpath('.//a[@class="title"]').get_attribute('href').encode("utf-8")
				except NoSuchElementException:
					print "---------Element not found - Thread Title Link-----------"
					thread_title_link = "Not Found"
					pass
				# print thread_title_link
				try:
					authorCol = thread_list[i].find_element_by_xpath('.//div[@class="author"]').text.encode("utf-8")
					author = authorCol.split()[2].strip(',')
				except NoSuchElementException:
					print "---------Element not found - Author-----------"
					author = "Not Found"
					pass
				# print author
				try:
					author_link = thread_list[i].find_element_by_xpath('.//a[@class="username understate"]').get_attribute('href').encode('utf-8')
				except NoSuchElementException:
					print "---------Element not found - Author Link-----------"
					author_link = "Not Found"
					pass
				# print author_link
				# get the raw data for replies tab. ( In the format of "Replies: 82")
				try:
					meta_raw = thread_list[i].find_element_by_xpath('.//ul[@class="threadstats td alt"]').text.encode("utf-8")
					# get the replies and views string in meta list
					if meta_raw.find("Replies") != -1:
						meta = meta_raw.split('\n')
						# break the string based on ':' operator. Get the second entry and strip of whitespace to get the number of replies.
						replies = meta[0].split(':')[1].strip()
						views = meta[1].split(':')[1].strip()
					else:
						replies = 0
						views = 0
				except NoSuchElementException:
					print "---------Element not found - Meta-----------"
					replies = "Not Found"
					views = "Not Found"
					pass
				flag = 0
				try:
					lastuser_meta =thread_list[i].find_element_by_xpath('.//dl[@class="threadlastpost td"]')
					lp = lastuser_meta.text.encode("utf-8")
					if lp.find("\n") != -1:
						flag=1
				except NoSuchElementException:
					print "---------Element not found - lastuser_meta-----------"
					lastuser_meta = ""
					pass
				if flag==1:
					try:
						lastuser = lastuser_meta.find_element_by_xpath('.//dd').text.encode("utf-8")
					except NoSuchElementException:
						print "---------Element not found - lastuser-----------"
						lastuser = "Not Found"
						pass
					user_onoff_flag = 0
					try:
						lastuser_link = lastuser_meta.find_element_by_xpath('.//a[@class="username offline popupctrl"]').get_attribute('href').encode("utf-8")
						user_onoff_flag=1
					except NoSuchElementException:
						print "---------Element not found - username offline popupctrl-----------"
						pass
					if not user_onoff_flag:
						lastuser_link = lastuser_meta.find_element_by_xpath('.//a[@class="username online popupctrl"]').get_attribute('href').encode("utf-8")
					try:
						lastpost_link = lastuser_meta.find_element_by_xpath('.//a[@class="lastpostdate understate"]').get_attribute('href').encode("utf-8")
					except NoSuchElementException:
						print "---------Element not found - lastpost_link-----------"
						lastpost_link = "Not Found"
						pass
					lsm_text = lastuser_meta.text.encode("utf-8")
					lastpost_datetime = lsm_text.split('\n')[1]
				else:
					lastuser = "Not Found"
					lastuser_link = "Not Found"
					lastpost_link = "Not Found"
					lastpost_datetime = "Not Found"


				item['thread_title'] = thread_title
				item['thread_title_link'] = thread_title_link
				item['author'] = author
				item['replies'] = replies
				item['views'] = views
				item['lastuser'] = lastuser
				item['lastuser_link'] = lastuser_link
				item['lastpost_link'] = lastpost_link
				item['lastpost_datetime'] = lastpost_datetime
				yield item

			## Navigate to the other pages containing threads lists.
			next = self.browser.find_element_by_xpath("//a[@rel='next']").get_attribute('href')
			self.browser.get(next)
		print "------------Exiting----------"
		self.browser.quit()
