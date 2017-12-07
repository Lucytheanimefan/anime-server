import os
from flask import Flask, render_template,send_from_directory, jsonify, request, session, json
import requests
import server
import JSONEncoder
import time
from anime_rec import findSeasonRecs
from datetime import datetime
import random
import MalCoordinator
import CrunchyRoll
import Funimation
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.secret_key = os.urandom(12)
database = server.get_db()
funi = Funimation.Funimation()

@app.route("/")
def home():
	return "Hello world"
	#return render_template("index.html")
	#

@app.errorhandler(404)
def page_not_found(e):
    return "Sorry this page was not found. Why don't you go watch some anime instead?"

@app.errorhandler(500)
def page_not_found(e):
    return "Sorry some internal error going on. I don't have enough time to fix this because I'm watching anime."

@app.route("/addNews", methods=["POST"])
def add_news():
	news = dict(request.form)
	news["date"]=time.strftime("%m/%d/%Y") 
	database.articles.insert_one(news)
	database.titles.insert_one({"title":news["title"],"date":news["date"]})
	return home()

@app.route("/animerec", methods=["POST", "GET"])
def animerec():
	seasons = ["fall","winter","summer","spring"]
	today = datetime.today()
	year = str(random.randint(2007,int(today.year)))
	season = random.choice(seasons)
	return jsonify({"message_format":"html","year": year, "season":season,"message":findSeasonRecs(season,year)})

@app.route("/recommendations", methods=["GET"])
def anime_recommendations():
	season = request.args.get('season')
	year = request.args.get('year')
	return render_template('recommendations.html', recommendations = findSeasonRecs(season,year))


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
