""" Scrapes Gab.ai posts. """

# pylint: disable=unsubscriptable-object
import argparse
import json
import os
import random
import sys
import time
import traceback
import mechanize


def shuffle_users(user_names):
	""" Generates a scraping order. """
	random.shuffle(user_names)
	return user_names


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

	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_refresh(False)
	browser.addheaders = [("User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")]
	r = browser.open("https://gab.ai/auth/login")

	browser.select_form(nr=0)
	browser["username"] = username
	browser["password"] = password
	r = browser.submit()

	print r.read()[0:500]

	return browser


def process_users(browser, user_names):
	""" Scrapes the specified posts. """

	j = 0
	k = 0
	for i in user_names:
		high_intensity_user = 0

		# Check if the post already exists.
		prefix = i[0:2].lower()

		if os.path.isfile("users/" + prefix + "/" + i + ".json"):
			print "Already have user " + i + ". Skipping."
			continue

		# Make directory structure if necessary.
		if not os.path.exists("users"):
			os.makedirs("users")
		if not os.path.exists("users/" + prefix):
			os.makedirs("users/" + prefix)

		# Read the user
		try:
			print str(i), "user page"
			r = browser.open("https://gab.ai/users/" + str(i))
			user_data = json.loads(r.read())
			r = browser.open("https://gab.ai/users/" + str(i) + "/followers")
			print str(i), "follower page"
			follower_data = json.loads(r.read())
			if not follower_data["no-more"]:
				page = 1
				done = 0
				while not done and page < 1500:
					min_back = page * 30
					r = browser.open("https://gab.ai/users/" + str(i) + "/followers?before=" + str(min_back))
					page = page + 1
					follower_page = json.loads(r.read())
					if follower_page["no-more"]:
						done = 1
					follower_data["data"].extend(follower_page["data"])

					if page % 10 == 1:
						print str(i), "follower page", str(page)
						time.sleep(5)
						high_intensity_user = 1
					else:
						time.sleep(0.5)

			r = browser.open("https://gab.ai/users/" + str(i) + "/following")
			print str(i), "following page"
			following_data = json.loads(r.read())
			if not following_data["no-more"]:
				page = 1
				done = 0
				while not done and page < 1500:
					min_back = page * 30
					r = browser.open("https://gab.ai/users/" + str(i) + "/following?before=" + str(min_back))
					page = page + 1
					following_page = json.loads(r.read())
					if following_page["no-more"]:
						done = 1
					following_data["data"].extend(following_page["data"])

					if page % 10 == 1:
						print str(i), "following page", str(page)
						time.sleep(5)
						high_intensity_user = 1
					else:
						time.sleep(0.5)

			data = {"user": user_data, "followers": follower_data, "following": following_data}

			with open("users/" + prefix + "/" + str(i) + ".json", "w") as f:
				json.dump(data, f)

			print data
			print i
			print ""
		# Error handling.
		except mechanize.HTTPError as error_code:
			if isinstance(error_code.code, int) and error_code.code == 429:
				print "TOO MANY REQUESTS. SHUT DOWN."
				print i
				sys.exit(-1)
				return
			elif isinstance(error_code.code, int) and error_code.code == 404:
				print "Gab post deleted or ID not allocated"
				print i
			elif isinstance(error_code.code, int) and error_code.code == 400:
				print "Invalid request -- possibly a private Gab post?"
				print i
			else:
				print error_code.code
				print traceback.format_exc()
				print "ERROR: DID NOT WORK"
				print i
		except:
			print traceback.format_exc()
			print "ERROR: STILL DID NOT WORK"
			print i

		# Pausing between jobs.
		pause_timer = random.randint(1, 10)
		if pause_timer >= 6:
			print "Waiting..."
			time.sleep(random.randint(2, 3))
		elif pause_timer <= 2:
			time.sleep(0.2)

		k = k + 1
		j = j + 1
		if j >= 1000:
			print "Medium length break."
			time.sleep(random.randint(10, 20))
			j = 0
		if k >= 10000:
			print "Long break."
			time.sleep(random.randint(60, 90))
			k = 0
		if high_intensity_user:
			print "Tough job, time to take a break."
			time.sleep(random.randint(30, 60))


def process_args():
	""" Reads command line arguments for what users file to use. """
	parser = argparse.ArgumentParser(description="Gab.ai scraper.")
	parser.add_argument("-u", "--username", action="store", dest="username", help="Specify a username", default="")
	parser.add_argument("-p", "--password", action="store", dest="password", help="Specify a password", default="")
	parser.add_argument("-f", "--filename", action="store", dest="filename", help="Specify a filename", default="names.txt")
	args = vars(parser.parse_args())

	user_names = [x.strip() for x in open(args["filename"], "r").read().split("\n") if len(x.strip())]

	user_order = shuffle_users(user_names)
	browser = login(args["username"], args["password"])

	if browser is not None:
		process_users(browser, user_order)
	else:
		print "Failed login."


if __name__ == "__main__":
	process_args()
