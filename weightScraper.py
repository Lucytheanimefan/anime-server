from bs4 import BeautifulSoup
import requests
import re
import json
import urllib


characters = ['Shiki Ryougi', 'Haruhi Fujioka', 'Nanami Momozono', 'Saber', 'Rei Kiriyama', 'Mikasa Ackerman', 'Hori Kyouko', 'Miyamura_Izumi', 'Yuuki Asuna', 'Yukino_Yukinoshita', 'Misaki_Ayuzawa', 'Touka_Kirishima', 'Akatsuki no Yona Yona', 'Inori_Yuzuriha', 'Misa Amane', 'Historia Reiss', 'Chise Hatori', 'Izaya Orihara', 'Celty Sturluson', 'Rin Tousaka', 'Lawliet death note','Light Yagami', 'Lelouch', 'Mitsuha','Ciel Phantomhive', 'Yuna Gasai', 'Nana osaki', 'Hiyori noragami', 'Holo spice and wolf','Kaori Miyazono', 'Lisa Mishima', 'Rintaro Okabe', 'Levi Attack on Titan', 'Hachmian Hikigaya', 'Sasuke Uchiha', 'Kirito', 'Rem Rezero', 'Yato Noragami', 'Sebastian Black butler', 'Heiwajima Shizuo', 'Usui Takumi', 'Hisoka Hunter', 'Haruhi Suzumiya', 'Oreki Houtarou', 'Lucy Elfen Lied', 'Asuka Evangelion', 'Emiya Kiritsugu', 'Ryuuko Matoi', 'Chitoge Kirisaki', 'Suou Tamaki', 'Kaname Kuran', 'Yuuki Kuran', 'Kiryuu Zero', 'Hyuga Hinata', 'Shinji Ikari', 'Natsume Takashi', 'Gilgamesh Fate', ' Ulquiorra', 'Kougami Shinya', 'Makishima Shougo', 'Dazai bungou', 'Juuzou Suzuya','Tsunayoshi Sawada','Aomine Daiki', 'Tomoe kamisama', 'Kuroki Tomoko', 'Hinata Shouyou', 'Kurapika', 'Sagara Sousuke', 'Inuyasha', 'Nishimiya Shouko', 'Kuriyama Mirai', 'Misaki Mei','Iwakura Lain', 'Sawako', 'Madoka', 'Ikuto Shugo chara', 'Akashi Kuroko', 'Rena Higurashi', 'Sesshoumaru', 'Shiro Deadman', 'Saeko Busujima', 'Mogami Kyouko', 'Nakano Azusa', 'Chitanda', 'Honma Anohana','Makoto Tachibana', 'Katou Megumi']

#characters = ['Rintaro Okabe']

def find_anime_character_url(character_name):
	url = 'https://www.google.com/search?q=' + urllib.quote(character_name)
	print url
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data,  "html.parser")
	results = soup.find_all("a", href=True)
	#print results
	for link in results:
		if 'wikia' in link['href']: #/url?q=
			return link['href'][7:].split('&', 1)[0]
	
	return ''

def clean_data_string(data):
	regex = re.compile(".*?\((.*?)\)")
	return re.sub(r'\[.*\]', '', data).strip('\n').rstrip().lstrip()

def scrape_weight(url):
	return_data = {}
	return_data['url'] = url
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data,  "html.parser")
	name = soup.find("h2", {"class": "pi-title"})
	if name is not None:
		return_data["name"] = name.text
	else:
		return_data["name"] = url.rsplit('/', 1)[-1]

	association = soup.find("div", {"class":"wds-community-header__sitename"})
	title = association.find("a").text
	return_data["title"] = title
	labels = soup.find_all("h3", {"class": "pi-data-label"})
	values = soup.find("div", {"class" : "pi-data-value"})
	relevant_values = ["weight", "height", "gender", "age"]
	for i, label in enumerate(labels):
		if label.text.lower() in relevant_values:
			return_data[label.text.lower()] = clean_data_string(label.findNext('div').text)


	if "weight" not in return_data or "height" not in return_data:
		td_labels = soup.find_all("td")
		for td in td_labels:
			label = clean_data_string(td.get_text().lower())
			if label in relevant_values:
				return_data[label] = clean_data_string(td.findNext('td').text)


	return return_data

def write_to_file(data, filename):
	with open(filename + '.txt', 'w') as outfile:
		json.dump(data, outfile)


if __name__ == '__main__':
	data = []
	for character in characters:
		url = find_anime_character_url(character)
		print url
		if url:
			data.append(scrape_weight(url))
	write_to_file(data, "data/anime_character_stats")

