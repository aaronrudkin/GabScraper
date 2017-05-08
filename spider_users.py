""" Takes existing user JSON data and finds usernames not already on the users list. """

import json


def spider():
	""" Main spidering code, searches for everyone who follows or is following anyone in current user list. """
	existing = [x.strip() for x in open("names.txt", "r").read().split("\n") if len(x.strip())]
	new = []

	for i in existing:
		prefix = i[0:2].lower()
		data_file = json.loads(open("users/" + prefix + "/" + i + "/json", "r").read())
		for user in data_file["following"]["data"]:
			if user["username"] not in existing and user["username"] not in new:
				new.append(user["username"])
		for user in data_file["followers"]["data"]:
			if user["username"] not in existing and user["username"] not in new:
				new.append(user["username"])

	with open("names.txt", "w") as f:
		for user in existing:
			f.write(user)
		for user in new:
			f.write(new)

	print len(new), "new users discovered."
	print len(existing) + len(new), "total users"


if __name__ == "__main__":
	spider()
