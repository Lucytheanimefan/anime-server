import os
from flask import Flask, render_template,send_from_directory, jsonify, request
import requests
import server

app = Flask(__name__)
database = server.get_db()

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/addNews", methods=["POST"])
def add_news():
	print "ADD NEWS"
	news = request.form
	database.articles.insert_one(dict(news))
	return "DONE"


@app.route("/getNews", methods=["GET"])
def get_news():
	news = request.get_json()
	print news




if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
