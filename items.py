# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CancerForumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    thread_title = scrapy.Field()
    thread_title_link = scrapy.Field()
    author = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    lastuser = scrapy.Field()
    lastuser_link = scrapy.Field()
    lastpost_link = scrapy.Field()
    lastpost_datetime = scrapy.Field()
    pass

class PostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    postDate = scrapy.Field()
    postTime = scrapy.Field()
    post_content = scrapy.Field()
    signature_content = scrapy.Field()
    username = scrapy.Field()
    userlink = scrapy.Field()
    usertitle = scrapy.Field()
    userrank = scrapy.Field()
    user_joindate = scrapy.Field()
    user_location = scrapy.Field()
    user_NumberOfPosts = scrapy.Field()
    pass
