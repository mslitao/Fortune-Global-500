#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TencentCrawler module of general functions
# by Jiaheng Zhang, all rights reserved.

import os
import json
import urllib
import requests
import datetime
import codecs

#configurations
data_dir_name = "data"
page_list_dir_name = "page_list"
proxy_address = None
push_address = None
request_timeout = None

# read the list of page to get info from
def get_list_from_file(file_name):

	the_file = codecs.open(file_name, encoding = 'utf-8')
	the_list = the_file.readlines()

	for i in range(len(the_list))[::-1]:
		the_list[i] = the_list[i].strip()
		if the_list[i] == '' or the_list[i][0] == '#':
			del the_list[i]

	return the_list

# initialize the data dir, if exists, do nothing, else create a new
def init_dir(dir_name):

	is_exists = os.path.exists(dir_name)
	if not is_exists:
		os.makedirs(dir_name)

def url_open(url, post_args = None, additional_headers = None, cookies = None, use_proxy = True, from_encoding = None):

	# set up the proxy
	if proxy_address and use_proxy:
		proxy = {"http": proxy_address}
	else:
		proxy = None

	headers = {'User-Agent': 'Mozilla/5.0'}
	if additional_headers != None:
		headers.update(additional_headers)

	if post_args != None:
		req = requests.post(url, data = post_args, headers = headers, cookies = cookies, \
			proxies = proxy, timeout = 10)
	else:
		req = requests.get(url, headers = headers, cookies = cookies, proxies = proxy, \
			timeout = 10)

	if from_encoding:
		req.encoding = from_encoding

	return req.text

def get_beijing_time():

	return datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
