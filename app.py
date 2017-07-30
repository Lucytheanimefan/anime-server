import os
from flask import Flask, render_template,send_from_directory, jsonify, request
import requests
import server
import JSONEncoder
import time
from anime_rec import findSeasonRecs

app = Flask(__name__)
database = server.get_db()

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/addNews", methods=["POST"])
def add_news():
	news = dict(request.form)
	news["date"]=time.strftime("%m/%d/%Y") 
	database.articles.insert_one(news)
	database.titles.insert_one({"title":news["title"],"date":news["date"]})
	return home()

@app.route("/animerec", methods=["POST"])
def animerec():
	return jsonify({"message":findSeasonRecs("summer","2016")})


@app.route("/getNews", methods=["GET"])
def get_news():
	news = database.articles.find({})
	articles = []
	for doc in news:
		del doc["_id"]
		articles.append(doc)

	return jsonify(articles)



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
