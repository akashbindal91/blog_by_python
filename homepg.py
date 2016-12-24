import MySQLdb	
import random
import string
from flask import Flask,render_template, request, redirect, url_for
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/home/' )
def home():
	ret = MySQLdb.connect("localhost","root","root","witty_blog" )
	recu = ret.cursor()
	recu.execute("SELECT * from blog_data ORDER BY submission DESC ")
	show = recu.fetchall();
	
	return render_template("homepg.html",show = show)

@app.route('/intake',methods=['POST'])
def intake():

	if request.method == 'POST':
		f = request.files['file']
		print "file name: "
		print f.filename

		if allowed_file(f.filename):
			print "file is an image"
		else:
			print "file is not an image"

		f.save("/tmp/" + get_random_str(10) + "_" + f.filename) 

		title = request.form['blog_title']
		content = request.form['blog_content']
		res = blog_dataentry(title, content,f)
		return redirect(url_for("home"))

	return "Failed"

DOCS_ACCEPT = ("png", "jpg")

def allowed_file(filename):
	# test.jpg
    return "." in filename and filename.rsplit(".", 1)[1] in DOCS_ACCEPT


def get_random_str(size):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def blog_dataentry(title, content,f): 
# Open database connection
	db = MySQLdb.connect("localhost","root","empire","witty_blog" )
# prepare a cursor object using cursor() method
	cursor = db.cursor()
# Prepare SQL query to INSERT a record into the database.
	sql = """INSERT INTO `blog_data`(`title`, `content`, 'image') VALUES ( '%s','%s' ,'%s')""" % (title,content,f)

	try:
		cursor.execute(sql)
# Commit your changes in the database
		db.commit()
		res = "your data has been successfully submitted"
		print "in try"
 	except:
 		db.rollback()
 		print "in except"
 		res = "gone wrong"

# disconnect from server
	db.close()
	return res

#@app.route('/repl/')
#def repl():
	
