# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_pymongo import PyMongo
import requests
import os

# -- Initialization section --
app = Flask(__name__)
app.secret_key = os.urandom(32)

# name of database
app.config['MONGO_DBNAME'] = 'music'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://mongod:r1rrDIG#ta5s@cluster0.3yk6e.mongodb.net/music?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


# ADD SONGS

@app.route('/add',methods=["POST","GET"])
def add():
    songs = mongo.db.songs
    songName = request.form['song']
    artistName = request.form['artist']
    description = request.form['description']
    if len(list(songs.find({"song":songName,"artist":artistName}))) == 0 :
        songs.insert({'song':songName,'artist':artistName,'description':description})
    listsongs= list(songs.find({}).sort("song",1))
    listsongs= listsongs
    return render_template("songs.html",songs=listsongs)


@app.route('/artist/<artistName>')
def songsBy(artistName):
    songs = mongo.db.songs
    listsongs= list(songs.find({"artist":artistName}).sort("song",1))
    return render_template("artistName.html",songs=listsongs)

@app.route('/artistSearch',methods=["POST","GET"])
def getArtist():
    artist = request.form['artist']
    return redirect(url_for('songsBy',artistName=artist))

@app.route('/login',methods=["POST","GET"])
def validate():
    users = mongo.db.users
    username = request.form['username']
    password = request.form['password']
    if len(list(users.find({'username':username}))) == 0:
        flash("That username was not found")
        return render_template("index.html")
    if len(list(users.find({'username':username,"password":password}))) == 0:
        flash("Incorrect Password")
        return render_template("index.html")
    return render_template("addsong.html",user=username)

@app.route('/createUser',methods=["POST","GET"])
def create():
    users = mongo.db.users
    username = request.form['username']
    password0 = request.form['password0']
    password1 = request.form['password1']
    if len(list(users.find({'username':username}))) > 0:
        flash("That username is already in use")
        return render_template("signup.html")
    if not password0 == password1:
        flash("Passwords did not match")
        return render_template("signup.html")
    users.insert({"username":username,"password":password0})
    flash("Account Created!")
    return redirect(url_for("index"))

@app.route('/newAccount')
def newaccount():
    return render_template("signup.html")
