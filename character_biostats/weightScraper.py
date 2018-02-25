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
import thread, threading
import itertools, time


output = mp.Queue()

class CharacterScraperThread (threading.Thread):
   def __init__(self, threadID, character):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.character = character
      self.character_data = None
   def run(self):
      print "Starting " + self.name
      # Get lock to synchronize threads
      #threadLock.acquire()
      self.character_data = scrape_weight_for_character(self.character)
      time.sleep(3)
      #self.data.append(character_data)
      # Free lock to release next thread
      #threadLock.release()



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
	text = [character.text for character in characters]
	#output.put(text)
	return text

def find_anime_character_url(character_name):
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

def clean_string(string):
	return string.replace('\n', '').rstrip().lstrip()

def clean_data_string(data):
	#string = data.sub(r"\(.*\)", "")  #get rid of anything in parentheses
	return re.sub(r'\[(.*\])', '', data)#.strip('\n').rstrip().lstrip()
	#return rid_unit(re.sub(r'\[(.*\])', '', data).strip('\n').rstrip().lstrip())
	
def remove_special_chars(string):
	# only include the numbers, get rid of letters
	return ''.join(e for e in string if e.isalnum())

def rid_unit(string):
	i = 0
	numeric = '0123456789'
	for j,c in enumerate(string):
		i += 1
		if not c.isdigit():
			break
	return string[:i]

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

	data_values = ["weight", "height","age"]
	for i, label in enumerate(labels):
		key = remove_special_chars(clean_data_string(label.text.lower()))
		if key in relevant_values:
			if label in data_values:
				value = clean_data_string(label.findNext('div').text)
			else:
				value = clean_string(label.findNext('div').text)
			return_data[key] = value


	if "weight" not in return_data or "height" not in return_data:
		td_labels = soup.find_all("td")
		th_labels = soup.find_all("th")
		for td in td_labels:
			label = super_clean_string(td.get_text().lower())
			if label in relevant_values:
				value = clean_string(td.findNext('td').text)
				if label in data_values:
					value = clean_data_string(value).split('\n')[-1]
				return_data[label] = value
		for th in th_labels:
			label = super_clean_string(th.get_text().lower())
			if label in relevant_values:
				value = th.findNext('td').text
				if label in data_values:
					value = clean_data_string(value).split('\n')[-1]
				value = clean_string(value)
				return_data[label] = value

	return return_data

def write_to_file(data, filename):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


def scrape_weight_for_character(character):
	url = find_anime_character_url(character)
	if len(url) > 0:
		return scrape_weight(url)
	return None

def batch_character_weight_process(pos, limit, output):
	threads = []
	characters = find_anime_characters_single(pos, limit, output) #output not needed in here anymore
	data = []
	#threads = []
	for i, character in enumerate(characters):
		#print character
		#thread.start_new_thread( print_time, ("Thread-1", 2, ) ) TODO: use threads
		thread = CharacterScraperThread(i, character)
		thread.setDaemon(True)
		thread.start()
		threads.append(thread)
		#character_data = scrape_weight_for_character(character)
		#if character_data:
		#	data.append(character_data)
	
	for t in threads:
		t.join()
		data.append(t.character_data)
		if not t.isAlive():
			print(t.name + ' is dead')
			#break
	print('----------Exiting main thread')
	print data
	output.put(data)
	return data

def begin_parallel(filename):
	limit = 2 #3*50 = 150 characters
	start_time = time.time()
	processes = [mp.Process(target=batch_character_weight_process, args=(x, 50*x, output)) for x in range(limit)]
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	results = [output.get() for p in processes]
	final_results = list(itertools.chain.from_iterable(results))
	elapsed_time = time.time() - start_time
	print('-----Parallel elapsed time: ' + str(elapsed_time))
	print('LENGTH')
	print(len(final_results))
	write_to_file(final_results, filename)

if __name__ == '__main__':
	debug = False
	do_parallel = True
	do_sequential = False;
	find_characters = True
	scrape_data = True
	clean_data = False
	write_file = False
	filename = "../data/parallel_character.json"#"../data/anime_character_stats3.json"

	if debug is True:
		print scrape_weight_for_character("gaara")
	elif do_parallel is True:
		begin_parallel(filename)
	elif do_sequential is True:
		start_time = time.time()
		if find_characters is True:
			characters = find_anime_characters(100)
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
				print('Length: ')
				print(len(data))
			elapsed_time = time.time() - start_time
			print('-----Sequential elapsed time: ' + str(elapsed_time))
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
			if write_file is True:
				write_to_file(new_data, "../data/cleaned_data"+str(time.time())+".json")


