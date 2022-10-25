# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:05:49 2022

@author: 劉佳怡
"""

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
import conn



app = Flask(__name__,static_folder="static" ,static_url_path = "/static")
app.secret_key = "no"

@app.route("/")
def form():
    state = "未登入"
    session["state"] = state
    return render_template("home.html")

   
@app.route("/signin",methods=["POST"])
def signin():
    input_username = request.form["username"]
    input_password = request.form["password"]
    if input_username == "" or input_password== "":
        return redirect("/error?message=empty")
    else:
        result = conn.confirm(input_username,input_password)
        if result == "correct":
            state = "已登入"
            session["state"] = state
            who = conn.filt(input_username)
            session["name"] = who[1]
            session["id"] = who[0]
            return redirect("/member")
        elif result == "wrong":
            state = "未登入"
            session["state"] = state
            return redirect("/error")
        
    
    
@app.route("/signup",methods=["POST"])
def signup():
    input_name = request.form["name"]
    input_username = request.form["username"]
    input_password = request.form["password"]
    if input_name == "" or input_username == "  " or input_password == "":
        return redirect("/error?message=setempty")
    else:
        result = conn.filt(input_username)
        if (result == None ):
            conn.add(input_name,input_username,input_password)
            return redirect("/")
        else:
            return redirect("/error?message=usernameused")



    
@app.route("/member")
def success():
    if session["state"] == "已登入":
        name = session['name']
        messageall = conn.message_content()
        return render_template("success.html",name=name,messageall=messageall)
        
    
    else:
        return redirect("/")
    

@app.route("/message",methods=["POST"])
def message():
    if session["state"] == "已登入":
        id = session['id']
        id = str(id)
        content = request.form["content"]
        if content != "輸入想輸入的內容...." :
            conn.message_send(id,content)
            return redirect("/member")
        else:
            return redirect("/member")
    else:
        return redirect("/")
    
@app.route("/error")
def fail():
    message = request.args.get("message",None)
    if message == "empty":  
        return render_template("fail.html",message="請輸入帳號、密碼")
    elif message == "usernameused":
        return render_template("fail.html",message="帳號已經被註冊")
    elif message == "setempty":
        return render_template("fail.html",message="欄位不能空白")
    else:
        return render_template("fail.html",message="帳號、或密碼輸入錯誤")
    
@app.route("/signout")
def signout():
    state = session["state"]
    state.replace("已登入","未登入")
    session["state"] = state
    name = ""
    id =  ""
    session["name"] = name
    session["id"] = id
    return redirect("/")

app.run(port=3000)