#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
from bs4 import BeautifulSoup
import requests
import re
import json
import urllib
import ast
import multiprocessing as mp

characters = ['Shiki Ryougi', 'Haruhi Fujioka', 'Nanami Momozono', 'Saber', 'Rei Kiriyama', 'Mikasa Ackerman', 'Hori Kyouko', 'Miyamura_Izumi', 'Yuuki Asuna', 'Yukino_Yukinoshita', 'Misaki_Ayuzawa', 'Touka_Kirishima', 'Akatsuki no Yona Yona', 'Inori_Yuzuriha', 'Misa Amane', 'Historia Reiss', 'Chise Hatori', 'Izaya Orihara', 'Celty Sturluson', 'Rin Tousaka', 'Lawliet death note','Light Yagami', 'Lelouch', 'Mitsuha','Ciel Phantomhive', 'Yuna Gasai', 'Nana osaki', 'Hiyori noragami', 'Holo spice and wolf','Kaori Miyazono', 'Lisa Mishima', 'Rintaro Okabe', 'Levi Attack on Titan', 'Hachmian Hikigaya', 'Sasuke Uchiha', 'Kirito', 'Rem Rezero', 'Yato Noragami', 'Sebastian Black butler', 'Heiwajima Shizuo', 'Usui Takumi', 'Hisoka Hunter', 'Haruhi Suzumiya', 'Oreki Houtarou', 'Lucy Elfen Lied', 'Asuka Evangelion', 'Emiya Kiritsugu', 'Ryuuko Matoi', 'Chitoge Kirisaki', 'Suou Tamaki', 'Kaname Kuran', 'Yuuki Kuran', 'Kiryuu Zero', 'Hyuga Hinata', 'Shinji Ikari', 'Natsume Takashi', 'Gilgamesh Fate', ' Ulquiorra', 'Kougami Shinya', 'Makishima Shougo', 'Dazai bungou', 'Juuzou Suzuya','Tsunayoshi Sawada','Aomine Daiki', 'Tomoe kamisama', 'Kuroki Tomoko', 'Hinata Shouyou', 'Kurapika', 'Sagara Sousuke', 'Inuyasha', 'Nishimiya Shouko', 'Kuriyama Mirai', 'Misaki Mei','Iwakura Lain', 'Sawako', 'Madoka', 'Ikuto Shugo chara', 'Akashi Kuroko', 'Rena Higurashi', 'Sesshoumaru', 'Shiro Deadman', 'Saeko Busujima', 'Mogami Kyouko', 'Nakano Azusa', 'Chitanda', 'Honma Anohana','Makoto Tachibana', 'Katou Megumi','naruto uzumaki', 'kakashi hatake', 'sakata gintoki', 'Kaneki Ken', 'vegeta','Tomoya Okazaki', 'Okumura Rin', 'Walker Allen', 'Yukihira Souma', 'Takanashi Rikka', 'Kyon Haruhi', 'Gremory Rias', 'Death the Kid', 'Kurumi Tokisaki', 'Akiyama Mio', 'Ayanami Rei', 'Hirasawa Yui', 'furukawa nagisa', 'nagato yuki','Natsu fairy tail', 'son goku', 'edward elric','roy mustang','Keima Katsuragi', 'Kae Serinuma','Hei darker than black','Tatsuya Shiba','Alucard','Guts Berserk','Spike Spiegel','Kyoya Hibari','Edward Newgate','Mugen samurai champloo', 'akame akame ga kill', 'Motoko Kusanagi','Clare claymore','Seras Victoria','Minene Uryu', 'Shana Shakugan no shana', 'Mikoto Misaka','kaga kouko','orihime','yukari paradise kiss','Senjougahara hitagi','kallen code geass','kaname chidori','Kotonoha Katsura', 'ai enma', 'rika furude','Rena Ryuuguu','Miyako hidamari sketch', 'Poplar Taneshima', 'Chiri Kitsu','Tomoko Kuroki','Kino Kino journey', 'Ayu Tsukimiya','Fuuko Ibuki','Konata Izumi','Himeko Inaba','Rakka haibane', 'Rei Ayanami','Yuuko Ichihara', 'Nanami Aoyama', 'kagura gintama', 'akane tsunemori', 'revy black lagoon', 'ezra scarlet']


#characters = ['naruto uzumaki', 'kakashi hatake', 'sakata gintoki', 'Kaneki Ken', 'vegeta','Tomoya Okazaki', 'Okumura Rin', 'Walker Allen', 'Yukihira Souma', 'Takanashi Rikka', 'Kyon Haruhi', 'Gremory Rias', 'Death the Kid', 'Kurumi Tokisaki', 'Akiyama Mio', 'Ayanami Rei', 'Hirasawa Yui', 'furukawa nagisa', 'nagato yuki','Natsu fairy tail', 'son goku', 'edward elric','roy mustang','Keima Katsuragi', 'Kae Serinuma','Hei darker than black','Tatsuya Shiba','Alucard','Guts Berserk','Spike Spiegel','Kyoya Hibari','Edward Newgate','Mugen samurai champloo', 'akame akame ga kill', 'Motoko Kusanagi','Clare claymore','Seras Victoria','Minene Uryu', 'Shana Shakugan no shana', 'Mikoto Misaka','kaga kouko','orihime','yukari paradise kiss','Senjougahara hitagi','kallen code geass','kaname chidori','Kotonoha Katsura', 'ai enma', 'rika furude','Rena Ryuuguu','Miyako hidamari sketch', 'Poplar Taneshima', 'Chiri Kitsu','Tomoko Kuroki','Kino Kino journey', 'Ayu Tsukimiya','Fuuko Ibuki','Konata Izumi','Himeko Inaba','Rakka haibane', 'Rei Ayanami','Yuuko Ichihara', 'Nanami Aoyama', 'kagura gintama', 'akane tsunemori', 'revy black lagoon', 'ezra scarlet']

#characters = ['Yukihira Soma']

output = mp.Queue()

def find_anime_characters(limit=50):
	lim = 0
	text = []
	while lim <= limit:
		url = 'https://myanimelist.net/character.php?limit=' + str(lim)
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data,  "html.parser")
		characters = soup.find_all('a', {'class':'fs14'})
		text = text + [character.text for character in characters]
		lim += 50
	print text
	return text

def find_anime_characters_single(pos, limit, output):
	print limit
	text = []
	url = 'https://myanimelist.net/character.php?limit=' + str(limit)
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data,  "html.parser")
	characters = soup.find_all('a', {'class':'fs14'})
	text = text + [character.text for character in characters]
	output.put(text)

def begin_parallel():
	processes = [mp.Process(target=find_anime_characters_single, args=(x, 50*x, output)) for x in range(1)]
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	results = [output.get() for p in processes]
	print(results)
	print('LENGTH')
	print(len(results))

def find_anime_character_url(character_name):
	print character_name
	name = urllib.quote(character_name.encode('utf8', errors = 'ignore'))
	#print name
	if len(name) > 0:
		url = 'https://www.google.com/search?q=' + name
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data,  "html.parser")
		results = soup.find_all("a", href=True)
		#print results
		for link in results:
			if 'wikia' in link['href']: #/url?q=
				return link['href'][7:].split('&', 1)[0]
		return ''
	else:
		print 'ENCODING ERROR FOR ' + character_name
	
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

# NOT WORKING FOR NARUTO WIKIA
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
	relevant_values = ["weight", "height", "gender", "age", "status", "date of death", "date of birth", "occupation"]

	for i, label in enumerate(labels):
		key = remove_special_chars(clean_data_string(label.text.lower()))
		if key in relevant_values:
			if label=='weight' or label=='height' or label=='age':
				value = clean_data_string(label.findNext('div').text)
			else:
				value = label.findNext('div').text
			return_data[key] = value


	if "weight" not in return_data or "height" not in return_data:
		td_labels = soup.find_all("td")
		for td in td_labels:
			label = super_clean_string(td.get_text().lower())
			if label in relevant_values:
				if label=='weight' or label=='height' or label=='age':
					value = clean_data_string(td.findNext('td').text)
				else:
					value = td.findNext('td').text
				return_data[label] = value

	return return_data

def write_to_file(data, filename):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


if __name__ == '__main__':
	do_parallel = True
	find_characters = True
	scrape_data = True
	clean_data = True
	write_file = True
	filename = "../data/anime_character_stats3.json"

	if do_parallel is True:
		begin_parallel()
	else:
		if find_characters is True:
			characters = find_anime_characters(250)
		if scrape_data is True:
			data = []
			for character in characters:
				url = find_anime_character_url(character)
				print(url)
				if len(url) > 0:
					data.append(scrape_weight(url))
			if write_file is True:
				write_to_file(data, filename)
			else:
				print data
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
						character["age"] = super_clean_string(character["age"].split(" ")[0].split("-")[0])
					new_data.append(character)
				write_to_file(new_data, "../data/cleaned_data3.json")


