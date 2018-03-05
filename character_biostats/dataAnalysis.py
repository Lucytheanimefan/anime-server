import ast
import pandas
import numpy as np
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import statsmodels.api as sm

def writeToCSV(filename):
	with open(filename) as file:
		new_data = []
		info = ast.literal_eval(file.read())
		with open("../data/data_new.csv", "w+") as write_file:
			write_file.write("name,gender,height,weight,bmi,status\n")
			for data in info:
				if "weight" in data and "height" in data:
					if len(data["height"])>0 and len(data["weight"])>0:
						height = float(data["height"])
						weight = float(data["weight"])
						bmi = weight/(height * height * 0.0001)
						print bmi
						status = 1
						#-1=dead, 1=alive, 0=undefined
						if "status" in data:
							if "alive" in data["status"].lower():
								status = 1
							elif "deceased" in data["status"].lower():
								status = -1
						write_file.write(data["name"] + "," + data["gender"] + "," + str(height) + "," 
							+ str(weight)+","+str(bmi) + "," + str(status) + "\n")
			write_file.close()


def analyze(filename='../data/data.csv'):
	data = pandas.read_csv(filename, sep=',')
	groupby_gender = data.groupby('gender')
	print(groupby_gender.mean())

	groupby_status = data.groupby('status')
	print(groupby_status.mean())

	print("---------------------------------")
	# ordinary least squares
	#model = ols("height ~ weight", data).fit()
	model = ols("status ~ bmi", data).fit()
	#print(model.summary())
	print(model.rsquared)
	# scatter-plot data
	# 
	fig, ax = plt.subplots(figsize=(12,8))
	fig = sm.graphics.influence_plot(model, ax=ax, criterion="cooks")
	fig.savefig("../data/ols_bmi_status.png")
	
	#for gender, value in groupby_gender['bmi']:
		#print((gender,value))


if __name__ == '__main__':
	writeToCSV("../data/new_cleaned_data.json")
	analyze('../data/data_new.csv')
