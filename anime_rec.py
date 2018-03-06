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

reload(sys)  
sys.setdefaultencoding('utf8')

aniChartUrl="https://www.livechart.me/"
great_studios = ["MAPPA","A-1 Pictures","Bones","Madhouse"]
good_studios = ["ufotable","Production I.G","Brains Base", "Shaft","Wit Studio"]
ok_studios = ["Lerche"]

bad_tags = ["School", "Harem","Ecchi", "Kids"]
sort_of_bad_tags = ["Slice of Life", "Comedy","Historical"]
ok_tags = ["Action","Drama","Fantasy","Shounen"] 
good_tags = ["Psychological","Seinen","Horror","Mystery","Thriller","Supernatural"]



output = mp.Queue()

def scrape_anime_info(anime_id, user_score, output):
	#print(anime_id)
	url = 'https://myanimelist.net/anime/' + str(anime_id)
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data,  "html.parser")
	labels = soup.find_all("span",{"class":"dark_text"})
	return_data = {"genre":None, "studio":None, "public_score":None, "user_score":None}
	return_data["user_score"] = user_score
	for label in labels:
		label_lower = label.text.lower()
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
	if output is not None:
		output.put(return_data)
	return return_data

def batch_anime_scrape(data_list, do_parallel=False):
	results = []
	if do_parallel:
		processes = [mp.Process(target=scrape_anime_info, args=(data["anime_id"], data["user_score"], output)) for data in data_list]
		for p in processes:
			p.start()
		for p in processes:
			p.join()
		results = [output.get() for p in processes]
		return results
	else:
		print('Don\'t do parallel')
		for data in data_list:
			results.append(scrape_anime_info(data["anime_id"], data["user_score"], None))
		return results

# TODO: make this parallel too           
def analyze_MAL(username):
	genre_count = {}
	studio_count = {}
	coordinator = MalCoordinator.MalCoordinator()
	data_list = coordinator.fetch_animelist(username)
	#print(data_list)
	#anime_ids = [data["anime_id"] for data in data_list]
	#print(anime_ids)
	anime_data = batch_anime_scrape(data_list)
	for data in anime_data:
		# if user's score is below 5, it's negative
		original_score = data["user_score"]
		if original_score >= 8:
			genre_score = original_score * 3
			studio_score = genre_score#original_score * 3
		elif original_score <=5:
			genre_score = original_score * -0.8
			studio_score = original_score * -0.5
		else:
			genre_score = original_score
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

	print(genre_count)
	print(studio_count)
	return (genre_count, studio_count)
	# sorted_genres = sorted(genre_count.items(), key=operator.itemgetter(1))
	# sorted_studios = sorted(studio_count.items(), key=operator.itemgetter(1))
	# print("------")
	# print(sorted_genres.reverse())
	# print(sorted_studios.reverse())
	

def findSeasonRecs(username, season, year, output_format = 'html'):
	genre_count = {}
	studio_count = {}
	if username:
		genre_count, studio_count = analyze_MAL(username)
	season_anime = {}
	scores = {}
	url = aniChartUrl + str(season)+"-"+str(year)+"/tv"
	#print(url)
	r = requests.get(url)
	data = r.text
	#print(data)
	soup = BeautifulSoup(data,  "html.parser")
	animez = soup.find_all("div", {"class": "anime-card"})
	for anime in animez:
		titlez = anime.find_all("h3",{"class":"main-title"})[0]
		title = (titlez.text).encode('utf-8').strip().replace('"', "'") 
		print(title)
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
		#blob = TextBlob(description)
		#for sentence in blob.sentences:
			#print(sentence.sentiment.polarity)
		#	scores[title]+=(-5*sentence.sentiment.polarity)
	
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
			i+=1
			anime_return += "<li>" + anime[0]+", "+str(anime[1]) + "</li>"
			print(anime_return)
		print("-------------")
		#print(season_anime)
		anime_return += "</ol>"
		print(anime_return)
	elif output_format == 'text':
		anime_return = scores#sorted_anime#json.dumps(reversed(sorted_anime))
		print("-------------")
		#print(sorted_anime)
		#anime_return = anime_return + "</ol>"
	return anime_return


if __name__ == '__main__':
	#analyze_MAL('Silent_Muse')
	print(findSeasonRecs('Silent_Muse','spring', 2018))
