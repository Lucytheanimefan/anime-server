import requests

base_url = "https://prod-api-funimationnow.dadcdigital.com/api/"
class Funimation(object):

	def __init__(self, username=""):
		self.username = username

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
		return r.json()


if __name__ == '__main__':
	funi = Funimation()
	#funi.info_for_title("tokyo-ghoul")
	


