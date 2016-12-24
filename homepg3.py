#import MySqlDb
import MySQLdb	
import random
import string
from flask import Flask, render_template,request,redirect,url_for
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/home/1')
def home():

	ret = MySQLdb.connect("localhost","root","empire","witty_blog" )
	recu = ret.cursor()
	recu.execute("SELECT * from blog_data ORDER BY submission DESC LIMIT 5  ")
	show = recu.fetchall();
	
	return render_template("homepg2.html",show = show)





@app.route('/input', methods = ['POST'])
def input():
	if request.method =='POST':
		title = request.form['blog_title']
		content = request.form['blog_content']
# check for the file and filter it
		f = request.files['file']
		if file_allowed(f.filename):
			print "file is an image"
		else:
			print "file is not an image"
# generate a random string to give a unique file name
		f_name = get_random_str(5) + "_" + f.filename
		f.save("/tmp/" + f_name ) 
# called the sql function to save the data		
		sqlFunction(title, content,f_name)
		print title,content,f_name
		return redirect(url_for("home"))

	return "Failed"
# function for generating a random string
def get_random_str(size):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

# filter the image type that r allowed to upload
def file_allowed(filename):
	# test.jpg
    return "." in filename and filename.rsplit(".", 1)[1] in DOCS_ACCEPT

# files extension
DOCS_ACCEPT = ("png","jpg","gif")

# database function
def sqlFunction(title, content,f_name):
	db = MySQLdb.connect("localhost","root","root","witty_blog")
	cursor = db.cursor()
	sql = """INSERT INTO `blog_data`(`title`, `content`, `image`) VALUES ( '%s','%s','%s')""" % (title, content,f_name)

	try:
		cursor.execute(sql)
		db.commit()
		res = "your data has been successfully submitted"
		#print "in try"
 	except:
 		db.rollback()
 		print "in except"
 		#res = "gone wrong"
	db.close()
	#return res