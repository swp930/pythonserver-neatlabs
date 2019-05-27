import os
import json
import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book, MoodData, UserData

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add")
def add_book():
    name=request.args.get('name')
    author=request.args.get('author')
    published=request.args.get('published')
    try:
        book=Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        books=Book.query.all()
        return  jsonify([e.serialize() for e in books])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/getalldata")
def get_all_data():
	try:
		mooddata=MoodData.query.all()
		return jsonify([e.serialize() for e in mooddata])
	except Exception as e:
		return(str(e))

@app.route("/getuserdata/<id_>")
def getuserdata(id_):
    try:
        userData=MoodData.query.filter_by(uniqueidentifier=id_).all()
        return jsonify([e.serialize() for e in userData])
    except Exception as e:
	    return(str(e))

@app.route("/getdatabetween")
def get_data_between():
    date1 = datetime.datetime(2019, 5, 22, 12, 00, 0)
    date2 = datetime.datetime(2019, 5, 22, 15, 00, 0)
    try:
        mooddata=MoodData.query.filter(MoodData.date>=date1).filter(MoodData.date<=date2)
        return jsonify([e.serialize() for e in mooddata])
    except Exception as e:
        return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name=request.form.get('name')
        author=request.form.get('author')
        published=request.form.get('published')
        try:
            book=Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/addwakesleeptime", methods=['GET', 'POST'])
def addwakesleeptime():
    if request.method == 'POST':
        uniqueidentifier=request.form.get('uniqueidentifier')
        waketime=request.form.get('waketime')
        sleeptime=request.form.get('sleeptime')
        try:
            user=UserData.query.filter_by(uniqueidentifier=uniqueidentifier).first()
            print(user)
            if(user is not None):
                user.waketime=waketime
                user.sleeptime=sleeptime
                db.session.commit()
                return render_template("addwakesleep.html")
        except Exception as e:
            return(str(e))
        try:
            user=UserData(
                uniqueidentifier=uniqueidentifier,
                waketime=waketime,
                sleeptime=sleeptime
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return(str(e))
    return render_template("addwakesleep.html")

@app.route("/makenewuserform", methods=['GET'])
def makenewuserform():
    return render_template("addnewuser.html")

@app.route("/makenewuser", methods=['POST'])
def makenewuser():
    if request.method == 'POST':
        print(request.get_json())
    return 'completed'

@app.route("/getallusers")
def get_all_users():
	try:
		users=UserData.query.all()
		return jsonify([e.serialize() for e in users])
	except Exception as e:
		return(str(e))

@app.route("/getuserinfo/<id_>")
def getuserinfo(id_):
    try:
        user=UserData.query.filter_by(uniqueidentifier=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/postbreath",methods=['POST'])
def submit_post_breath():
    if request.method == 'POST':
        print(request.get_json()["breaths"])
        print(request.get_json()["uniqueidentifier"])
        print("POST BREATH")
        waketime = ""
        sleeptime = ""
        try:
            user=UserData.query.filter_by(uniqueidentifier=request.get_json()["uniqueidentifier"]).first()
            waketime = user.waketime
            sleeptime = user.sleeptime
        except Exception as e:
	        return(str(e))
        waketimedata = waketime.split(":")
        sleeptimedata = sleeptime.split(":")
        waketimehr = int(waketimedata[0], 10)
        waketimemin = int(waketimedata[1], 10)
        sleeptimehr = int(sleeptimedata[0], 10)
        sleeptimemin = int(sleeptimedata[1], 10)
        now = datetime.datetime.now()
        now = now.astimezone(timezone('US/Pacific'))
        wakedate = datetime.datetime(now.year, now.month, now.day, waketimehr, waketimemin, 0)
        sleepdate = datetime.datetime(now.year, now.month, now.day, sleeptimehr, sleeptimemin, 0)
        print("Now post breath: ", now)
        print("Wakedate: ", wakedate)
        print("Sleepdate: ", sleepdate)
        if(now < wakedate or now > sleepdate):
            return "False out of range"
        diff = abs(sleepdate - wakedate)
        increment = diff/5
        intervalStart = wakedate

        while(intervalStart + increment <= sleepdate and not(now >= intervalStart and now <= (intervalStart + increment))):
            intervalStart += increment
        startTime = intervalStart
        endTime = intervalStart + increment

        try:
            mooddata=MoodData.query.filter_by(uniqueidentifier=request.get_json()["uniqueidentifier"]).\
            filter(MoodData.date>=startTime).filter(MoodData.date<=endTime).all()
            if(len(mooddata) > 0):
                print("Invalid submission!")
                return "False already submitted"
        except Exception as e:
            print(str(e))
            return(str(e))

        print(startTime)
        print(endTime)

        try:
            md = MoodData(
				data=json.dumps(request.get_json()["breaths"]),
                date=datetime.datetime.now(),
                uniqueidentifier=request.get_json()["uniqueidentifier"]
			)
            db.session.add(md)
            db.session.commit()
            return "True"
        except Exception as e:
            return(str(e))    
        return 'completed'

if __name__ == '__main__':
    app.run()
