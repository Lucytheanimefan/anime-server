import requests
from bs4 import BeautifulSoup

base_url = "http://www.crunchyroll.com/user/"

class CrunchyRoll(object):
	def __init__(self, username):
		self.username = username

	def fetch_user_info(self):
		url = 'http://www.crunchyroll.com/user/{}'.format(self.username)
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data,  "html.parser")
		userinfo = soup.find_all("table", {"class": "user-profile-interests"})[0]
		i = 0
		key = ""
		to_ret = {}
		for info in userinfo.find_all("td"):
			if i%2 == 0:
				key = info.find_all("span")[0].text
				to_ret[key] = None
			else:
				to_ret[key] = info.find_all("a")[0].text
			i += 1
		return to_ret



if __name__ == '__main__':
	crunchy = CrunchyRoll("KowaretaSekai")
	print(crunchy.fetch_user_info())

