from bs4 import BeautifulSoup
import requests
import re
import json
import urllib
import ast

#characters = ['Shiki Ryougi', 'Haruhi Fujioka', 'Nanami Momozono', 'Saber', 'Rei Kiriyama', 'Mikasa Ackerman', 'Hori Kyouko', 'Miyamura_Izumi', 'Yuuki Asuna', 'Yukino_Yukinoshita', 'Misaki_Ayuzawa', 'Touka_Kirishima', 'Akatsuki no Yona Yona', 'Inori_Yuzuriha', 'Misa Amane', 'Historia Reiss', 'Chise Hatori', 'Izaya Orihara', 'Celty Sturluson', 'Rin Tousaka', 'Lawliet death note','Light Yagami', 'Lelouch', 'Mitsuha','Ciel Phantomhive', 'Yuna Gasai', 'Nana osaki', 'Hiyori noragami', 'Holo spice and wolf','Kaori Miyazono', 'Lisa Mishima', 'Rintaro Okabe', 'Levi Attack on Titan', 'Hachmian Hikigaya', 'Sasuke Uchiha', 'Kirito', 'Rem Rezero', 'Yato Noragami', 'Sebastian Black butler', 'Heiwajima Shizuo', 'Usui Takumi', 'Hisoka Hunter', 'Haruhi Suzumiya', 'Oreki Houtarou', 'Lucy Elfen Lied', 'Asuka Evangelion', 'Emiya Kiritsugu', 'Ryuuko Matoi', 'Chitoge Kirisaki', 'Suou Tamaki', 'Kaname Kuran', 'Yuuki Kuran', 'Kiryuu Zero', 'Hyuga Hinata', 'Shinji Ikari', 'Natsume Takashi', 'Gilgamesh Fate', ' Ulquiorra', 'Kougami Shinya', 'Makishima Shougo', 'Dazai bungou', 'Juuzou Suzuya','Tsunayoshi Sawada','Aomine Daiki', 'Tomoe kamisama', 'Kuroki Tomoko', 'Hinata Shouyou', 'Kurapika', 'Sagara Sousuke', 'Inuyasha', 'Nishimiya Shouko', 'Kuriyama Mirai', 'Misaki Mei','Iwakura Lain', 'Sawako', 'Madoka', 'Ikuto Shugo chara', 'Akashi Kuroko', 'Rena Higurashi', 'Sesshoumaru', 'Shiro Deadman', 'Saeko Busujima', 'Mogami Kyouko', 'Nakano Azusa', 'Chitanda', 'Honma Anohana','Makoto Tachibana', 'Katou Megumi']


characters = ['naruto uzumaki', 'kakashi hatakue', 'sakata gintoki', 'Kaneki Ken', 'vegeta','Tomoya Okazaki', 'Okumura Rin', 'Walker Allen', 'Yukihira Souma', 'Takanashi Rikka', 'Kyon Haruhi', 'Gremory Rias', 'Death the Kid', 'Kurumi Tokisaki', 'Akiyama Mio', 'Ayanami Rei', 'Hirasawa Yui', 'furukawa nagisa', 'nagato yuki','Natsu fairy tail', 'son goku', 'edward elric','roy mustang','Keima Katsuragi', 'Kae Serinuma','Hei darker than black','Tatsuya Shiba','Alucard','Guts Berserk','Spike Spiegel','Kyoya Hibari','Edward Newgate','Mugen samurai champloo', 'akame akame ga kill', 'Motoko Kusanagi','Clare claymore','Seras Victoria','Minene Uryu', 'Shana Shakugan no shana', 'Mikoto Misaka','kaga kouko','orihime','yukari paradise kiss','Senjougahara hitagi','kallen code geass','kaname chidori','Kotonoha Katsura', 'ai enma', 'rika furude','Rena Ryuuguu','Miyako hidamari sketch', 'Poplar Taneshima', 'Chiri Kitsu','Tomoko Kuroki','Kino Kino journey', 'Ayu Tsukimiya','Fuuko Ibuki','Konata Izumi','Himeko Inaba','Rakka haibane', 'Rei Ayanami','Yuuko Ichihara', 'Nanami Aoyama', 'kagura gintama', 'akane tsunemori', 'revy black lagoon', 'ezra scarlet']

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

def shorten(s, subs):
    i = s.index(subs)
    return s[:i+len(subs)]

def clean_data_string(data):
	#string = data.sub(r"\(.*\)", "")  #get rid of anything in parentheses
	return re.sub(r'\[(.*\])', '', data).strip('\n').rstrip().lstrip()
	
def remove_special_chars(string):
	return ''.join(e for e in string if e.isalnum())

def super_clean_string(string):
	return remove_special_chars(clean_data_string(string))

def calculate_bmi(height, weight):
	return weight/(height*height * 0.0001)

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
		key = remove_special_chars(clean_data_string(label.text.lower()))
		if key in relevant_values:
			return_data[key] = clean_data_string(label.findNext('div').text)


	if "weight" not in return_data or "height" not in return_data:
		td_labels = soup.find_all("td")
		for td in td_labels:
			label = clean_data_string(td.get_text().lower())
			if label in relevant_values:
				return_data[label] = clean_data_string(td.findNext('td').text)

	return return_data

def write_to_file(data, filename):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


if __name__ == '__main__':
	scrape_data = False
	clean_data = True
	filename = "../data/anime_character_stats2.json"
	if scrape_data is True:
		data = []
		for character in characters:
			url = find_anime_character_url(character)
			#print url
			if url:
				data.append(scrape_weight(url))
		write_to_file(data, filename)
		print 'Done'
	if clean_data:
		print 'Cleaning data'
		with open(filename) as file:
			new_data = []
			text = file.read().replace('\n', '')
			info = ast.literal_eval(text)
			for character in info:
				if "weight" in character:
					character["weight"] = clean_data_string(character["weight"].split("kg",1)[0].split("lb",1)[0])
				if "height" in character:
					character["height"] = clean_data_string(character["height"].split("cm",1)[0])
				if "age" in character:
					character["age"] = super_clean_string(character["age"].split(" ")[0].split("-")[0])#character["age"].split(" ", 1)[0]
				#print character
				new_data.append(character)
			write_to_file(new_data, "../data/cleaned_data3.json")


