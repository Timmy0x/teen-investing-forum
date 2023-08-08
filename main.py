from flask import Flask, redirect, request, render_template, url_for, send_file, make_response, Response
from flask_cors import CORS

import csv
import json
import os
import time
from datetime import datetime, timedelta

import requests

from forum import ForumController

forum_con = ForumController()

user_list = []

app = Flask(__name__)
CORS(app)

########## Static ##########
@app.route("/")
def index():
    if json.loads(request.cookies.get("user")) not in user_list:
        user_list.append(json.loads(request.cookies.get("user")))
    return open("static/index.html").read()
@app.route("/profile/<name>")
def profile(name):
    posts = json.loads(open("data/posts.json").read())
    users = json.loads(requests.get("https://teen-investing-usermanagement.timmym.repl.co/get_users").text)
    user_posts = ""
    for row in users:
        if str(row.get("name")) == str(name):
            user = row
    for row in posts:
        if str(row.get("author")) == str(name):
            user_posts+=f"<div><b>{row.get('author')}   </b><i>{row.get('date')}</i><p>{row.get('text')}</p></div>"
    return render_template("profile.html", name=name, description=user.get("description"), posts=user_posts)
    

@app.route("/forum.css")
def styles_css():
    return Response(open("static/forum.css").read(), mimetype="text/css")
@app.route("/core.css")
def core_css():
    return Response(requests.get("https://teen-investing.onrender.com/app/styles/core.css").text, mimetype="text/css")
@app.route("/forum.js")
def scripts_js():
    return Response(open("static/forum.js").read(), mimetype="text/javascript")
@app.route("/core.js")
def core_js():
    return Response(requests.get("https://teen-investing.onrender.com/scripts/core.js").text, mimetype="text/javascript")
@app.route("/identity.js")
def identity_js():
    return Response(requests.get("https://teen-investing.onrender.com/scripts/identity.js").text, mimetype="text/javascript")

@app.route("/chat/room.css")
def room_css():
    return Response(open("static/chat/room.css").read(), mimetype="text/css")
@app.route("/chat/home.css")
def home_get_css():
    return Response(open("static/chat/home.css").read(), mimetype="text/css")
@app.route("/chat/create.css")
def create_css():
    return Response(open("static/chat/create.css").read(), mimetype="text/css")


########## Chat ##########
@app.route("/chat")
def chat_home():
    if not json.loads(json.dumps(request.cookies)).get("user"):
        return "<p>Please sign in to continue</p>"
    else:
        rooms = ""
        for room in os.listdir("chats"):
            rooms += "<div onclick='window.location.href=\"/chat/room/" + room.replace(".txt", "").replace("room.", "") + "\"'><h1>" + room.replace(".txt", "").replace("room.", "") + "</h1></div>"
        return render_template("home.html", rooms=rooms)

@app.route("/chat/create/<name>", methods=['GET'])
def chat_create(name):
    new_file_room = open(f"chats/room.{name}.txt", "w")
    new_file_room.write("")
    new_file_room.close()
    return redirect(f"/chat/room/{name}")
@app.route("/chat/create")
def chat_create_page():
    return render_template("create.html")

@app.route("/join/", methods=['GET', 'POST'])
def chat_join():
    if request.method == 'GET':
        return render_template("join-get.html")
    if request.method == 'POST':
        return redirect(f"/chat/room/{request.form.get('room_key')}")

@app.route("/chat/room/<string:number>/")
def chat_room_get(number):
    if os.path.isfile(f"chats/room.{number}.txt"):
        content_mes = open(f"chats/room.{number}.txt", "r", encoding='utf-8').read()
        title = number
        msg_list = content_mes.split('\n') if content_mes else None
        return render_template("room.html", title=title, msg_list=msg_list, room_key=number, user=json.loads(json.loads(json.dumps(request.cookies)).get("user")).get("name"))
    else:
        return "This room does not exist."

@app.route("/chat/room/<id>/messages")
def chat_room_get_messages(id):
    return open(f"chats/room.{id}.txt", "r", encoding='utf-8').read().split("\n")
@app.route("/chat/room/<id>/send/<message>/<user>")
def chat_room_send_message(id, message, user):
    content_room = open(f"chats/room.{id}.txt", "a", encoding='utf-8')
    if message:
        time_msg = f"{time.localtime().tm_hour}:{time.localtime().tm_min}.{time.localtime().tm_sec}"
        content_room.write(f"<i>{time_msg}</i> <b>{json.loads(json.loads(json.dumps(request.cookies)).get('user')).get('name')}</b><br> <a>{message}</a>\n")
    return Response('{"success": true}', mimetype="text/json")

########## Forum ##########
@app.route("/api/get_feed")
def forum_get_feed():
    return Response(forum_con.get_feed(), mimetype="text/json")
@app.route("/api/add_post")
def forum_add_post():
    try:
        args = request.args
        forum_con.add_post(text=args.get("text"), name=args.get("name"), email=args.get("email"), password=args.get("password"))
        return Response('{"success": true}', mimetype="text/json")
    except:
        return Response('{"success": false}', mimetype="text/json")
@app.route("/api/get_users")
def forum_get_users():
    return Response(json.dumps(user_list), mimetype="text/json")

app.run(host="0.0.0.0", port=80)
