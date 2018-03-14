# -*- coding: utf-8 -*-
import sys  
if 'threading' in sys.modules:
    del sys.modules['threading']
import os
from flask import Flask, render_template,send_from_directory, jsonify, request, session, json, Response
import requests
import server
import JSONEncoder
import time
from anime_rec import findSeasonRecs, batch_anime_scrape
from datetime import datetime
import random
import MalCoordinator
import CrunchyRoll
import Funimation
from bson.json_util import dumps
import ast
import importlib
from worker import *
from rq import Queue
import json

#importlib.reload(sys)  
#sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.secret_key = os.urandom(12)
database = server.get_db()
funi = Funimation.Funimation()

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/form")
def form():
	return render_template("form.html")
	

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error = "Sorry this page was not found. Why don't you go watch some anime instead?")

@app.errorhandler(500)
def page_not_found(e):
	return render_template('error.html', error = "Sorry some internal error going on. Life is short. Go checkout Crunchyroll instead.")

@app.route("/addNews", methods=["POST"])
def add_news():
	news = dict(request.form)
	news["date"]=time.strftime("%m/%d/%Y") 
	database.articles.insert_one(news)
	database.titles.insert_one({"title":news["title"],"date":news["date"]})
	return home()

@app.route("/addReview", methods=["POST"])
def add_review():
	news = dict(request.form)
	news["date"] = time.strftime("%m/%d/%Y") 
	database.reviews.insert_one(news)
	return "Success"

@app.route("/updateReview", methods=["POST"])
def update_review():
	review = request.get_json()
	review_query = {}
	review_query['title'] = review['title']
	review_query['anime_id'] = review['anime_id']
	database.reviews.update_one(review_query, {"$set": {"review":review["review"]}}, upsert=True)
	return "Success"

@app.route("/reviews", methods=["GET"])
def get_reviews():
	query = {}
	anime_id = request.args.get('anime_id')
	if anime_id is None:
		query = {}
	else:
		query = {'anime_id':anime_id}
	reviews = dumps(database.reviews.find(query))
	return jsonify(json.dumps(reviews))


@app.route('/status/<job_id>', methods=["GET"])
def job_status(job_id):
	#q = Queue()
    job = q.fetch_job(job_id)
    if job is None:
        response = {'status': 'unknown'}
    else:
        response = {
            'status': job.get_status(),
            'result': job.result,
        }
        if job.is_failed:
            response['message'] = job.exc_info.strip().split('\n')[-1]
    return jsonify(response)

@app.route("/recommendations", methods=["GET"])
def anime_recommendations():
	season = request.args.get('season')
	year = request.args.get('year')
	username = request.args.get('username')
	recs = ""
	job_id = ""
	if season is None or year is None:
		season = "spring"
		year = 2018
	if username is not None:
		user_data = database.mal.find_one({"username":username})
		print("Found user?")
		print(user_data)
		if user_data:
			print("Found data from db for this user!")
			genre_count = json.loads(user_data["genre_count"])
			studio_count = json.loads(user_data["studio_count"])
			recs = findSeasonRecs(username, season, year, genre_count, studio_count)
		elif user_data is None:
			recs = "Could not find an animelist associated with that user."
		else:
			job = q.enqueue(findSeasonRecs, username, season, year, timeout=700)
			job_id = job.get_id()

	return render_template('recommendations.html', job_id=job_id, recommendations=recs, season=season, year=year, username=username)

@app.route("/character_biometrics", methods=["GET"])
def character_biometrics():
	with open('data/new_cleaned_data.json') as file:
		text = file.read().replace('\n', '')
		info = ast.literal_eval(text)
		return render_template('anime_character_biostats.html', data = json.dumps(info))
	return page_not_found('No data found for anime character biometrics')

@app.route("/getNews", methods=["GET"])
def get_news():
	news = database.articles.find({})
	articles = []
	for doc in news:
		del doc["_id"]
		articles.append(doc)

	return jsonify(articles)


@app.route("/animeapplehipchat", methods=["GET"])
def jsonstuff():
	return app.send_static_file("animeapple.json")


@app.route("/myanimelist", methods = ["GET"])
def getMAL():
	username = request.args.get('username')
	if username is None:
		username = "Silent_Muse"
	coordinator = MalCoordinator.MalCoordinator()
	return jsonify(coordinator.fetch_animelist(username))

@app.route("/mal", methods = ["GET"])
def malVisualList():
	username = request.args.get('username')
	if username is None:
		username = "Silent_Muse"
	coordinator = MalCoordinator.MalCoordinator()
	return render_template('malVisual.html', malList = json.dumps(coordinator.fetch_animelist(username)))

# @app.route("/malVisual")
# def malVisual():
# 	return render_template("malVisual.html")

@app.route("/crunchyroll", methods = ["GET"])
def getCrunchy():
	username = request.args.get('username')
	if username is None:
		username = "KowaretaSekai"
	crunchy = CrunchyRoll.CrunchyRoll(username)
	return jsonify(crunchy.fetch_user_info())

@app.route("/funiLogin", methods = ["POST"])
def funiLogin():
	params = request.get_json()
	user = params["username"]
	passw = params["password"]
	response = funi.login(user, passw)
	auth_token = response["token"]
	#print auth_token
	#session['funiAuthToken'] = auth_token
	return jsonify(response)
	

@app.route("/funiQueue", methods = ["POST"])
def funi_queue():
	funi = Funimation.Funimation()
	auth_token = request.get_json()["funiAuthToken"]
	return jsonify(funi.get_my_queue(auth_token))


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	#app.run(host='0.0.0.0', port=port, debug=True)
	app.run(debug=True)
