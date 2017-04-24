""" Scrapes Gab.ai posts. """

import argparse
import json
import os
import random
import sys
import time
import traceback
import mechanize


def shuffle_posts(min_num, max_num):
	""" Generates a scraping order. """
	post_numbers = range(min_num, max_num)
	random.shuffle(post_numbers)
	return post_numbers

def login(username="", password=""):
	""" Login to gab.ai. """
	if not len(username) or not len(password):
		auth_data = json.load(open("auth.json"))
		try:
			username = auth_data["username"]
		except:
			print "No username specified."
			return

		try:
			password = auth_data["password"]
		except:
			print "No password specified."
			return

	b = mechanize.Browser()
	b.set_handle_robots(False)
	b.set_handle_refresh(False)
	b.addheaders = [("User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")]
	r = b.open("https://gab.ai/auth/login")

	b.select_form(nr = 0)
	b["username"] = username 
	b["password"] = password
	r = b.submit()

	print r.read()[0:500]

	return b

def process_posts(b, post_numbers):
	""" Scrapes the specified posts. """

	j = 0
	k = 0
	for i in post_numbers:
		# Check if the post already exists.
		num = str(i)
		ones = num[-1]
		tens = num[-2:]
		hundreds = num[-3:]

		if os.path.isfile("posts/" + ones + "/" + tens + "/" + hundreds + "/" + str(i) + ".json"):
			if random.randint(1, 10) == 10:
				print "Skipping "  + str(i)
			continue
		
		# Make directory structure if necessary.
		if not os.path.exists("posts"):
			os.makedirs("posts")
		if not os.path.exists("posts/" + ones):
			os.makedirs("posts/" + ones)
		if not os.path.exists("posts/" + ones + "/" + tens):
			os.makedirs("posts/" + ones + "/" + tens)
		if not os.path.exists("posts/" + ones + "/" + tens + "/" + hundreds):
			os.makedirs("posts/" + ones + "/" + tens + "/" + hundreds)

		# Read the post
		try:
			r = b.open("https://gab.ai/posts/" + str(i))
			d = r.read()
			f = open("posts/" + ones + "/" + tens + "/" + hundreds + "/" + str(i) + ".json","w")
			f.write(d)
			f.close()
			print d
			print i
			print ""
		# Error handling.
		except mechanize.HTTPError as e:
			if isinstance(e.code, int) and e.code == 404:
				print "Gab post deleted or ID not allocated"
				print i
			elif isinstance(e.code, int) and e.code == 400:
				print "Invalid request -- possibly a private Gab post?"
				print i
			else:
				print e.code
				print traceback.format_exc()
				print "ERROR: DID NOT WORK"
				print i
		except:
			print traceback.format_exc()
			print "ERROR: STILL DID NOT WORK"
			print i

		# Pausing between jobs.
		pause_timer = random.randint(1, 10)
		if pause_timer == 10:
			print "Waiting..."
			time.sleep(random.randint(2, 3))
		elif pause_timer == 1 or pause_timer == 2:
			time.sleep(0.1)

		k = k + 1
		j = j + 1
		if j >= 5000:
			print "Medium length break."
			time.sleep(random.randint(10, 20))
			j = 0
		if k >= 51000:
			print "Long break."
			time.sleep(random.randint(60, 90))
			k = 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Gab.ai scraper.")
	parser.add_argument("-u", "--username", action="store", dest="username", help="Specify a username", default="")
	parser.add_argument("-p", "--password", action="store", dest="password", help="Specify a password", default="")
	parser.add_argument("num_limits", nargs="*", help="Minimum and maximum post numbers.")
	args = vars(parser.parse_args())
	if len(args["num_limits"]) != 2:
		min_num = 1
		max_num = 1000000
		print "Failed to get post number limits."
	else:
		try:
			min_num = int(args["num_limits"][0])
			max_num = int(args["num_limits"][1])
		except:
			print "Failed to get post number limits."
			min_num = 1
			max_num = 1000000

	post_order = shuffle_posts(min_num, max_num)
	browser = login(args["username"], args["password"])

	if browser is not None:
		process_posts(browser, post_order)
	else:
		print "Failed login."
