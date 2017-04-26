import os
from flask import Flask, render_template,send_from_directory, jsonify
import requests
import server

app = Flask(__name__)


@app.route("/addNews", methods=["POST"])
def add_news():
	news = request.get_json()
	print news




if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
