# -*- coding: utf-8 -*-
# 
'''
WHAT SHOULD YOU WATCH NEXT SEASON? (More like, what would Lucy watch next season?)
Warning: not accurate
How to use:
1. Download 
2. pip install the following modules: requests, bs4, textblob
3. Run: python -m textblob.download_corpora
4. Run: python new_anime_rec.py
'''

import subprocess
import sys
from bs4 import BeautifulSoup
import requests
#from textblob import TextBlob
import operator
import random
import json
import MalCoordinator
import multiprocessing as mp
import importlib
import time
import math
from difflib import SequenceMatcher

#importlib.reload(sys)  
#sys.setdefaultencoding('utf8')

aniChartUrl="https://www.livechart.me/"
great_studios = ["MAPPA","A-1 Pictures","Bones","Madhouse"]
good_studios = ["ufotable","Production I.G","Brains Base", "Shaft","Wit Studio"]
ok_studios = ["Lerche"]

bad_tags = ["School", "Harem","Ecchi", "Kids"]
sort_of_bad_tags = ["Slice of Life", "Comedy","Historical"]
ok_tags = ["Action","Drama","Fantasy","Shounen"] 
good_tags = ["Psychological","Seinen","Horror","Mystery","Thriller","Supernatural"]

my_headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,am;q=0.7,zh-HK;q=0.3",
"Accept-Encoding": "gzip, deflate",
"Cookie": "PREF=ID=1111111111111111:FF=0:LD=en:TM=1439993585:LM=1444815129:V=1:S=Zjbb3gK_m_n69Hqv; NID=72=F6UyD0Fr18smDLJe1NzTReJn_5pwZz-PtXM4orYW43oRk2D3vjb0Sy6Bs_Do4J_EjeOulugs_x2P1BZneufegpNxzv7rkY9BPHcfdx9vGOHtJqv2r46UuFI2f5nIZ1Cu4RcT9yS5fZ1SUhel5fHTLbyZWhX-yiPXvZCiQoW4FjZd-3Bwxq8yrpdgmPmf4ufvFNlmTd3y; OGP=-5061451:; OGPC=5061713-3:",
"Connection": "keep-alive"}


output = mp.Queue()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# parse relevant info from scraped labels
def parse_relevant_info(labels, return_data):
	for label in labels:
		label_lower = label.text.lower()
		#print(label_lower)
		if 'genre' in label_lower: 
			parent = label.parent
			return_data["genre"] = [value.text for value in parent.find_all("a")]
		if 'studios' in label_lower:
			parent = label.parent
			return_data["studio"] = [value.text for value in parent.find_all("a")]
			#print(return_data["studio"])
		if 'score' in label_lower:
			if label.parent.find("span",{"itemprop":"ratingValue"}) is not None:
				return_data["public_score"] = label.parent.find("span",{"itemprop":"ratingValue"}).text

	return return_data

def find_anime_labels(anime_id):
	url = 'https://myanimelist.net/anime/' + str(anime_id)
	r = requests.get(url, headers=my_headers)
	data = r.text
	soup = BeautifulSoup(data,  "html.parser")
	labels = soup.find_all("span",{"class":"dark_text"})
	return labels

def scrape_anime_info(anime_id, user_score, output):
	#print(anime_id)
	# url = 'https://myanimelist.net/anime/' + str(anime_id)
	# r = requests.get(url, headers=my_headers)
	# data = r.text
	# soup = BeautifulSoup(data,  "html.parser")
	labels = find_anime_labels(anime_id) #soup.find_all("span",{"class":"dark_text"})
	#print(labels)
	return_data = {"genre":None, "studio":None, "public_score":None, "user_score":None,"anime_id":anime_id}
	return_data["user_score"] = user_score
	return_data = parse_relevant_info(labels, return_data)
	# for label in labels:
	# 	label_lower = label.text.lower()
	# 	#print(label_lower)
	# 	if 'genre' in label_lower: 
	# 		parent = label.parent
	# 		return_data["genre"] = [value.text for value in parent.find_all("a")]
	# 	if 'studios' in label_lower:
	# 		parent = label.parent
	# 		return_data["studio"] = [value.text for value in parent.find_all("a")]
	# 		#print(return_data["studio"])
	# 	if 'score' in label_lower:
	# 		if label.parent.find("span",{"itemprop":"ratingValue"}) is not None:
	# 			return_data["public_score"] = label.parent.find("span",{"itemprop":"ratingValue"}).text
	if return_data["genre"] is None and return_data["studio"] is None and return_data["public_score"] is None:
		# probably too many requests if we're not getting the data, we'll need to stall
		print("STALL too many requests")
		time.sleep(30) # I don't actually know what the rate limit for MAL is :/
		# Try again, but only once more, else I don't care. No recursion. That could go into dangerous territories.
		labels = find_anime_labels(anime_id)
		return_data = parse_relevant_info(labels, return_data)

	if output is not None:
		output.put(return_data)
	return return_data

def batch_scrape_anime_info(data_chunk, output):
	print("BATCH")
	return_data = []
	for data in data_chunk:
		return_data.append(scrape_anime_info(data["anime_id"], data["user_score"], None))
	print(return_data)
	print("------------------")
	output.put(return_data) # an array of dictionaries 

def batch_anime_scrape(data_list, do_parallel=True):
	results = []
	# TODO: split into 4 processes ONLY
	num_cores = mp.cpu_count()
	chunk_size = int(math.ceil(len(data_list)/num_cores)) #TODO: don't have a set chunk size, evenly distribute this instead so that one chunk doesn't have a single chunk of data
	print("Chunk size: " + str(chunk_size))
	#remainder = len(data_list)%num_cores
	# if (remainder*2 < chunk_size):
	# 	num_cores+=1
	# 	chunk_size = int(len(data_list)/num_cores)
	chunked_data = [data_list[i:i + chunk_size] for i in range(0, len(data_list), chunk_size)]
	#print("CHUNKED DATA")
	#print(chunked_data)

	if do_parallel:
		start_time = time.time()
		processes = [mp.Process(target=batch_scrape_anime_info, args=(data, output)) for data in chunked_data]
		for p in processes:
			p.start()
		for p in processes:
			p.join()
		elapsed_time = time.time() - start_time
		print("----Chunk size: "+str(chunk_size)+", Elapsed time: " + str(elapsed_time))

		lists = [output.get() for p in processes]
		results = [item for sublist in lists for item in sublist] #append the list of lists into 1 list
		return results
	else:
		print('Don\'t do parallel')
		start_time = time.time()
		for data in data_list:
			results.append(scrape_anime_info(data["anime_id"], data["user_score"], None))
		elapsed_time = time.time() - start_time
		print("----Sequential elapsed time: " + str(elapsed_time))
		return results

# TODO: make this parallel too           
def analyze_MAL(username):
	genre_count = {}
	studio_count = {}
	coordinator = MalCoordinator.MalCoordinator()
	data_list = coordinator.fetch_animelist(username)
	if "error" in data_list:
		return "error",data_list["error"]

	anime_data = batch_anime_scrape(data_list)
	for data in anime_data:
		# if user's score is below 5, it's negative
		original_score = data["user_score"]
		if original_score >= 8:
			genre_score = original_score * 0.5
			studio_score = original_score*3
		elif original_score <=5:
			genre_score = original_score * -0.5
			studio_score = original_score * -1
		else:
			genre_score = original_score * 0.2
			studio_score = original_score * 0.5

		if data["genre"] is not None:
			for genre in data["genre"]:
				if genre in genre_count:
					genre_count[genre] += genre_score
				else:
					genre_count[genre] = genre_score

		# I feel like it's less applicable to studios, so weighted less
		if data["studio"] is not None:
			for studio in data["studio"]:
				if studio in studio_count:
					studio_count[studio] += studio_score
				else:
					studio_count[studio] = studio_score

	print("--------------------")
	print(genre_count)
	print(studio_count)
	return (genre_count, studio_count, data_list)

	

def findSeasonRecs(username, season, year, genre_count = None, studio_count = None, mal_list = None, output_format = 'html'):
	print('FIND SEASON RECS')

	if username is None:
		username = "Silent_Muse"
	if genre_count is None or studio_count is None:
		if username:
			genre_count, studio_count, mal_list = analyze_MAL(username)
			if genre_count == "error":
				return studio_count #the error message

	final_mal_list = []
	if mal_list is None:
		coordinator = MalCoordinator.MalCoordinator()
		final_mal_list = coordinator.fetch_animelist(username)
	else:
		final_mal_list = mal_list

	season_anime = {}
	scores = {}
	url = aniChartUrl + str(season) + "-" + str(year) + "/tv"
	#print(url)
	r = requests.get(url)
	data = r.text
	#print(data)
	soup = BeautifulSoup(data,  "html.parser")
	animez = soup.find_all("div", {"class": "anime-card"})
	for anime in animez:
		titlez = anime.find_all("h3",{"class":"main-title"})[0]
		title = (titlez.text).strip().replace('"', "'") 
		#print(title)
		print_data = (title == "Cutie Honey Universe")

		scores[title] = 0 #each show starts off with 0


		########## check title ###########
		if "death" in title:
			scores[title]+=2


		########### check the tag/genre ##########
		tags = [tag.text for tag in anime.find_all("ol",{"class":"anime-tags"})[0].find_all("li")]
		for tag in tags:
			value = 0
			if tag in genre_count:
				value = int(genre_count[tag])
			# default to Lucy's tastes
			elif tag in good_tags:
				value = 6
			elif tag in sort_of_bad_tags:
				value = -3
			elif tag in bad_tags:
				value = -10
			elif tag in ok_tags:
				value =2

			scores[title]+= value

			if print_data:
				print('Genre score value increment: ' + str(value) +', '+ tag)

		season_anime[title] = {"tags":tags}
		studios = anime.find_all("ul",{"class":"anime-studios"})

		############ check the studios #############
		parsed_studios = []
		for studio in studios:
			if studio.find_all("a"):
				stud = studio.find_all("a")[0].text
				value = 0
				if stud in studio_count:
					value = studio_count[stud]
				# default to Lucy's tastes
				elif stud in great_studios:
					value = 6
				elif stud in good_studios:
					value = 3
				elif stud in ok_studios:
					value = 1
				scores[title] += value

				if print_data:
					print('Studio score value increment: ' + str(value) +', '+ stud)
				parsed_studios.append(stud)
			else:
				parsed_studios.append(studio.find_all("li")[0].text)
		season_anime[title]["studios"]=parsed_studios

		############### check description ###################
	
		description = anime.find_all("div",{"class":"anime-synopsis"})[0].find("p").text
		if "death" in description:
			scores[title]+=2
		season_anime["description"] = description

		# blob = TextBlob(title + ". " + description)
		# for sentence in blob.sentences:
		# 	#The polarity score is a float within the range [-1.0, 1.0]
		# 	print(-100*sentence.sentiment.polarity)
		# 	scores[title]+=(-100*sentence.sentiment.polarity)
		
		########## check sequels ###########
		for mal_anime in final_mal_list:
			mal_title = mal_anime["title"].lower()
			similar_score = similar(title.lower(), mal_title)
			if title.lower() in mal_title or similar_score > 0.75:
				print("---Sequel: " + title + ", " + mal_title + ", " + str(similar_score))
				mal_score = mal_anime["user_score"]
				if similar_score == 1:
					# identical, the anime is already on user's MAL list, shoot it to the top
					print("******BOOST sequel already on LIST: " + title + ", " + mal_title)
					scores[title] *= 10
				elif mal_score == 10:
					print("******BOOST sequel 10: " + title + ", " + mal_title)
					scores[title] *= 5 # Sequels are important
				elif mal_score == 9:
					print("******BOOST sequel 9: " + title + ", " + mal_title)
					scores[title] *= 2
				elif mal_score == 8:
					print("******BOOST sequel 8: " + title + ", " + mal_title)
					scores[title] *= 1.5
				elif mal_score == 7:
					print("******BOOST sequel 7: " + title + ", " + mal_title)
					scores[title] *= 1.05

	
	#print season_anime
	anime_return = None
	sorted_anime = sorted(scores.items(), key=operator.itemgetter(1))

	if username is None:
		username = "Lucy"
	print('-------------------RECOMMENDATION-------------------')
	i=0
	if output_format == 'html':
		anime_return = "<h1>Anime of " + season +" " + str(year) + " for " + username + "</h1><ol>" 
		
		for anime in reversed(sorted_anime):
			i += 1
			title,score = anime 
			anime_return += "<li>" + title+", "+str(score) + "</li>"

		print("-------------")
		#print(season_anime)
		anime_return += "</ol>"
		print(anime_return)
	elif output_format == 'text':
		anime_return = ""
		for anime in reversed(sorted_anime):
			title,score = anime 
			i += 1
			anime_return += str(i) + ": " + title+", "+str(score) + "\n"
	
		print("-------------")
		#print(anime_return)
	return anime_return


if __name__ == '__main__':
	print("Do nothing")
