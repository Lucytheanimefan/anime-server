import requests

base_url = "https://prod-api-funimationnow.dadcdigital.com/api/"
funi_recs = "fun/modules/?territory=en-US&inclusion=Regions|US&slug=pi-schedule-shows&user_id=d812ecb2-8cbe-11e7-861d-22000b56051a&session_id=d812f2c0-8cbe-11e7-861d-22000b56051a"
my_queue = "source/funimation/queue"#/?flat=true"

class Funimation(object):

	def __init__(self, username=""):
		self.username = username
		self.auth_token = None
		self.csrftoken = None

	def info_for_title(self, title):
		endpoint = "source/catalog/title/{}".format(title)
		url = base_url + endpoint
		r = requests.get(url)
		json_entries = r.json()
		print json_entries

	def login(self, username, password):
		endpoint = "auth/login/"
		headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Territory': 'US'
        }
		r = requests.post(base_url + endpoint, data = {'username':username,'password':password}, headers = headers, verify=False)
		print r.headers
		print "------------------"
		self.csrftoken = r.headers['Set-Cookie'].split(';')[0].split('=')[1]
		self.auth_token = r.json()["token"]
		return r.json()

	def get_my_queue(self):
		if self.auth_token:
			headers = {"Authorization":"Token " + self.auth_token}#, "x-csrftoken":self.csrftoken, "territory":"US", "accept-language":"en-US,en;q=0.8"}
			r = requests.get(base_url + my_queue, headers = headers, verify=False)
			return r.json()
		else:
			return "No auth token, could not proceed with getting Funimation anime queue"



if __name__ == '__main__':
	funi = Funimation()
	#funi.get_my_queue()
	


