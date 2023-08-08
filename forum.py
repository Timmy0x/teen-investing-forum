import csv
import json
import random
from datetime import datetime

import requests

def get_user(name=None, email=None, password=None):
	return requests.get(f"https://teen-investing-usermanagement.timmym.repl.co/get_user?name={name}&email={email}&password={password}").text

class ForumController:
	def add_post(self, text=None, name=None, email=None, password=None):
		if get_user(name=name, email=email, password=password) != None:
			random.seed = [text, name, email]
			id = random.randrange(1, 100000000)
			data = json.loads(open("data/posts.json").read())
			data.append({
				"id": id,
				"text": text,
				"author": name,
				"date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
			})
			open("data/posts.json", "w").write(json.dumps(data, indent=4))
			return True
		else:
			return 102
	def get_feed(self):
		with open("data/posts.json", "r") as f:
			data = json.load(f)
		sorted_data = sorted(data, key=lambda x: x["date"], reverse=True)
		return json.dumps(sorted_data, indent=4)