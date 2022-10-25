# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 19:00:13 2022

@author: 劉佳怡
"""

import mysql.connector




mydb = mysql.connector.connect(
     host="",
     user="",
     password="",
     port  = "",
     database=""
   )
    
mycursor = mydb.cursor()

def filt (input_username):     
    mycursor.execute("SELECT * FROM member WHERE username= %s ",(input_username,)) 
    myresult = mycursor.fetchone() 
    return myresult
        
def add(input_name,input_username,input_password):
    mycursor.execute("INSERT INTO member (name,username,password) VALUES(%s,%s,%s)",(input_name,input_username,input_password))
    mydb.commit()
    
    
def confirm(input_username,input_password):
    mycursor.execute("SELECT * FROM member WHERE username=%s ",(input_username,))
    myresult = mycursor.fetchone()
    
    if myresult != None:
        if myresult[2] == input_username and myresult[3] == input_password:
            return "correct"
        else:
            return "wrong"
    else: 
        return "wrong"
   
    
    
def message_content():
    messageall = [] 
    mycursor.execute("SELECT member_id,content FROM message ")
    myresult = mycursor.fetchall()
    
    
    for x in myresult:
        message = {}
        member_id = str(x[0])
        mycursor.execute("SELECT name FROM member WHERE id=%s ",(member_id,))
        name = mycursor.fetchone()
        author=name[0]
        content = x[1]
        message["author"] = author
        message["content"] = content
        
        messageall.append(message)
    
    return messageall

def message_send(id,content):
    mycursor.execute("INSERT INTO message(member_id,content) VALUES(%s,%s)",(id,content))
    mydb.commit()