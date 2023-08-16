 # import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response,jsonify
from werkzeug import secure_filename
from datetime import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from schemes import predScheme
from sms import sendSMS

login_status = 0
#------------------------App Code--------------------------------------------------------

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	error = ""
	global login_status
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			email = request.form['email']
			password = request.form['password']	
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			cursorObj.execute(f"SELECT Email from dairygroup WHERE Email='{email}' AND Password = '{password}';")

			if(cursorObj.fetchone()):
				login_status = 1
				if(email == 'admin@gov.in'):
					return redirect(url_for('home'))
				else:
					return redirect(url_for('dairycattle'))
			else:
				error = "Invalid Credentials Please try again..!!!"
	return render_template('signup.html',error=error)

@app.route('/dairyfarmer', methods=['GET', 'POST'])
def dairyfarmer():
	global name
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	
	conn = sqlite3.connect('connect.db', isolation_level=None,
						detect_types=sqlite3.PARSE_COLNAMES)
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			fname = request.form['fname']
			dname = request.form['dname']
			year = request.form['year']
			state = request.form['state']
			dist = request.form['dist']
			adhar = request.form['adhar']
			cow = request.form['cow']
			cowmilk = request.form['cowmilk']
			buffalo = request.form['buffalo']
			buffalomilk = request.form['buffalomilk']

			print(buffalomilk)
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO Farmer VALUES(?,?,?,?,?,?,?,?,?,?)",(fname,adhar,cow,cowmilk,buffalo,buffalomilk,year,state,dist,dname))
			con.commit()
			db_df = pd.read_sql_query(f"SELECT * from Farmer", conn)
			return render_template('dairyfarmer.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding')])

	db_df = pd.read_sql_query(f"SELECT * from Farmer", conn)
	
	return render_template('dairyfarmer.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding')])

@app.route('/dairycattle', methods=['GET', 'POST'])
def dairycattle():
	global name
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	
	conn = sqlite3.connect('connect.db', isolation_level=None,
						detect_types=sqlite3.PARSE_COLNAMES)
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			date = request.form['date']
			cowmilk = request.form['cowmilk']
			buffalomilk = request.form['buffalomilk']
	

			print(buffalomilk)
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO  cattleprocurement VALUES(?,?,?)",(date,cowmilk,buffalomilk))
			con.commit()
			db_df = pd.read_sql_query(f"SELECT * from cattleprocurement", conn)
			return render_template('dairycattle.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding all-order-th')])

	db_df = pd.read_sql_query(f"SELECT * from cattleprocurement", conn)
	
	return render_template('dairycattle.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding all-order-th')])

@app.route('/dairyassets', methods=['GET', 'POST'])
def dairyassets():
	global name
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	
	conn = sqlite3.connect('connect.db', isolation_level=None,
						detect_types=sqlite3.PARSE_COLNAMES)
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			date = request.form['date']
			asset = request.form['asset']
			quantity = request.form['quantity']
			dname = request.form['dname']
			state = request.form['state']
			dist = request.form['dist']
	
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO  dairysectionassets VALUES(?,?,?,?,?,?)",(date,asset,quantity,dname,state,dist))
			con.commit()
			db_df = pd.read_sql_query(f"SELECT * from dairysectionassets", conn)
			return render_template('dairyassets.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding')])

	db_df = pd.read_sql_query(f"SELECT * from dairysectionassets", conn)
	
	return render_template('dairyassets.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding')])


@app.route('/order', methods=['GET', 'POST'])
def order():
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			state = request.form['state']
			district = request.form['district']
			dairy = request.form['dairy']
			print(state,district,dairy)
			email = 'admin@gov.in'
			password = 'admin1'
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			df = pd.read_sql_query(f"SELECT * from dairygroup WHERE Email='{email}' AND Password = '{password}';",con)
			print(df)
	return render_template('dashboard.html')

@app.route('/schemes_inner_dairy', methods=['GET', 'POST'])
def schemes_inner_dairy():
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			return redirect(url_for('assets'))	
	return render_template('schemes_inner_dairy.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
	global login_status
	login_status = 0
	return redirect(url_for('/'))

@app.route('/home', methods=['GET', 'POST'])      #ministry Dashboard
def home():
	'''
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	'''
	con = sqlite3.connect('connect.db')
	cursorObj = con.cursor()
	df1 = pd.read_sql_query(f"SELECT * from Farmer;",con)

	cows1 = 	df1[['noofCows']].values.astype(int).sum()
	buffalos1 = df1[['noofbuffaloes']].values.astype(int).sum()
	cowmilk1 = df1[['avgcowmilkproduction']].values.astype(int).sum()
	buffalomilk1 = df1[['avgbuffalomilkproduction']].values.astype(int).sum()
	farmers1 = len(df1.index)
	cattles = cows1+buffalos1
	milk = cowmilk1+buffalomilk1
	df3 = pd.read_sql_query(f"SELECT * from dairygroup;",con)
	dairies = len(df3.index)-1
	df4 = pd.read_sql_query(f"SELECT * from dairysectionassets;",con)
	assets = len(df4.index)

	if request.method == 'POST':
		if request.form['sub']=='Submit':
			state = request.form['state']
			#state = 'Gujarat'
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			df = pd.read_sql_query(f"SELECT * from Farmer WHERE state='{state}';",con)
	
			cows = 	df[['noofCows']].values.astype(int).sum()
			buffalos = df[['noofbuffaloes']].values.astype(int).sum()
			cowmilk = df[['avgcowmilkproduction']].values.astype(int).sum()
			buffalomilk = df[['avgbuffalomilkproduction']].values.astype(int).sum()
			farmers = len(df.index)
			df2 = pd.read_sql_query(f"SELECT * from dairygroup WHERE state='{state}';",con)
			dairies = len(df2.index)
			y = [cows,buffalos,cowmilk,buffalomilk,farmers,dairies]
			x = ['Cows','Buffaloes','CowMilk','BuffaloMilk','Farmers','Dairies']
			plt.figure(figsize=(10, 6))
			plt.bar(x,y,color=['red', 'blue', 'green','yellow','pink','purple'])
			plt.xlabel('State Details')
			plt.ylabel('Quantity')
			plt.title(state+" Information")
			plt.legend()
			plt.savefig('static/img/dash.png')
			plt.close()
			return render_template('ministrydashboard.html',milk=milk,cattles=cattles,farmers=farmers1,dairies=dairies, tables=[df.to_html(index=False,classes='w3-table-all w3-hoverable w3-padding')])
	return render_template('ministrydashboard.html',milk=milk,cattles=cattles,farmers=farmers1,dairies=dairies,assets=assets)

@app.route('/cattle', methods=['GET', 'POST'])      #ministry Dashboard
def cattle():
	'''
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	'''
	con = sqlite3.connect('connect.db')
	cursorObj = con.cursor()
	df1 = pd.read_sql_query(f"SELECT * from Farmer;",con)

	cows1 = 	df1[['noofCows']].values.astype(int).sum()
	buffalos1 = df1[['noofbuffaloes']].values.astype(int).sum()
	cowmilk1 = df1[['avgcowmilkproduction']].values.astype(int).sum()
	buffalomilk1 = df1[['avgbuffalomilkproduction']].values.astype(int).sum()
	farmers1 = len(df1.index)
	cattles = cows1+buffalos1
	milk = cowmilk1+buffalomilk1
	

	if request.method == 'POST':
		if request.form['sub']=='Submit':
			state = request.form['state']
			#state = 'Gujarat'
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			df = pd.read_sql_query(f"SELECT * from Farmer WHERE state='{state}';",con)

			'''
			cows = 	df[['noofCows']].values.astype(int).sum()
			buffalos = df[['noofbuffaloes']].values.astype(int).sum()
			cowmilk = df[['avgcowmilkproduction']].values.astype(int).sum()
			buffalomilk = df[['avgbuffalomilkproduction']].values.astype(int).sum()
			
			farmers = len(df.index)
			y = [cows,buffalos,cowmilk,buffalomilk,farmers,farmers]
			x = ['Cows','Buffaloes','CowMilk','BuffaloMilk','Farmers','Dairies']
			plt.figure(figsize=(10, 6))
			plt.bar(x,y,color=['red', 'blue', 'green','yellow','pink','purple'])
			plt.xlabel('State Details')
			plt.ylabel('Quantity')
			plt.title(state+" Information")
			plt.legend()
			plt.savefig('static/img/dash.png')
			plt.close()
			'''
			return render_template('cattledash.html',cowmilk1=cowmilk1,buffalomilk1=buffalomilk1,cows1=cows1,buffalos1=buffalos1,tables=[df.to_html(index=False,classes='w3-table-all w3-hoverable w3-padding')])
	return render_template('cattledash.html',cowmilk1=cowmilk1,buffalomilk1=buffalomilk1,cows1=cows1,buffalos1=buffalos1)

@app.route('/asset', methods=['GET', 'POST'])      #ministry Dashboard
def asset():
	'''
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	'''
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			state = request.form['state']
			#state = 'Gujarat'
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			df = pd.read_sql_query(f"SELECT * from dairysectionassets WHERE state='{state}';",con)

			return render_template('assetdash.html',tables=[df.to_html(index=False,classes='w3-table-all w3-hoverable w3-padding')])
	return render_template('assetdash.html')

@app.route('/schemepred', methods=['GET', 'POST'])      #ministry Dashboard
def schemepred():
	'''
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	'''
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			state = request.form['state']
			#state = 'Gujarat'
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			df = pd.read_sql_query(f"SELECT * from Farmer WHERE state='{state}';",con)

			cows = 	df[['noofCows']].values.astype(int).sum()
			buffalos = df[['noofbuffaloes']].values.astype(int).sum()
			cowmilk = df[['avgcowmilkproduction']].values.astype(int).sum()
			buffalomilk = df[['avgbuffalomilkproduction']].values.astype(int).sum()
			farmers = len(df.index)

			df1 = pd.read_sql_query(f"SELECT * from dairygroup WHERE state='{state}';",con)
			dairies = len(df1.index)
			test_sample = [[cows,buffalos,cowmilk,buffalomilk,farmers,dairies]]
			proposedScheme = predScheme(test_sample)

			return render_template('schemepreddash.html',proposedScheme=proposedScheme, tables=[df.to_html(index=False,classes='w3-table-all w3-hoverable w3-padding')])
	return render_template('schemepreddash.html')

@app.route('/dairymarketing', methods=['GET', 'POST'])
def dairymarketing():
	global login_status
	if(login_status != 1):
		return redirect(url_for('/'))
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			nums = request.form['number'].split(',')
			print(nums)
			msg = request.form['msg']
			for num in nums:
				sendSMS(num, msg)
	return render_template('dairymarketing.html')

@app.route('/schemes', methods=['GET', 'POST'])
def schemes():
	global login_status
	if(login_status != 1):
		return redirect(url_for('landing'))
	return render_template('schemes.html')

@app.route('/schemes_inner', methods=['GET', 'POST'])
def schemes_inner():
	global login_status
	if(login_status != 1):
		return redirect(url_for('landing'))
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			return redirect(url_for('assets'))	
	return render_template('schemes-inner.html')

@app.route('/assets', methods=['GET', 'POST'])
def assets():
	global login_status
	if(login_status != 1):
		return redirect(url_for('landing'))
	return render_template('assets_of_schemes.html')

@app.route('/dairygroup', methods=['GET', 'POST'])
def dairygroup():
	global name
	global login_status
	if(login_status != 1):
		return redirect(url_for('landing'))

	conn = sqlite3.connect('connect.db', isolation_level=None,
						detect_types=sqlite3.PARSE_COLNAMES)
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			dairyname = request.form['dairyname']
			headquarter = request.form['headquarter']
			state = request.form['state']
			dairytype = request.form['dairytype']
			email = request.form['email']
			number = request.form['number']
			password = request.form['password']
			print(dairyname,headquarter,state,dairytype,email,number,password)

			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
			con = sqlite3.connect('connect.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS dairygroup (Date text,DairyName text,Headquarter text,State text,Email text,Number text,Password text)")
			cursorObj.execute("INSERT INTO dairygroup VALUES(?,?,?,?,?,?,?)",(dt_string,dairyname,headquarter,state,email,number,password))
			con.commit()

	db_df = pd.read_sql_query(f"SELECT * from dairygroup", conn)
	db_df = db_df.iloc[:,1:6]
	print(db_df)
	return render_template('dairygroup.html',tables=[db_df.to_html(index=False,border=0,header=False, classes='w3-table-all w3-hoverable w3-padding')])



# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)
