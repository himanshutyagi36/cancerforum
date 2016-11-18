# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

from cancerforum.items import CancerForumItem
from cancerforum.items import PostItem

class CancerforumPipeline(object):
    def __init__(self):
		self.conn = MySQLdb.connect(user='root', passwd='1590', host='localhost', db='cancerforum')
		self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if (spider.name == "mainpage_spider"):
			try:
				self.cursor.execute("REPLACE INTO `frontPage` (`thread_title`, `thread_title_link`, `author`,`replies`, `views`, `lastuser`, `lastuser_link`,"
					" `lastpost_link`, `lastpost_datetime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
				(item['thread_title'], item['thread_title_link'],item['author'], item['replies'], item['views'], item['lastuser'], item['lastuser_link'], item['lastpost_link'],
				item['lastpost_datetime']))
				self.conn.commit()
			except MySQLdb.Error, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					pass
        elif (spider.name == "post_spider"):
			try:
				self.cursor.execute("REPLACE INTO `posts` (`postDate`, `postTime`, `post_content`, `signature_content`, `username`, `userlink`,"
					" `usertitle`, `userrank`, `user_joindate`, `user_location`, `user_NumberOfPosts`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
				(item['postDate'], item['postTime'], item['post_content'], item['signature_content'], item['username'], item['userlink'], item['usertitle'],
				item['userrank'], item['user_joindate'], item['user_location'], item['user_NumberOfPosts']))
				self.conn.commit()
			except MySQLdb.Error, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					pass
