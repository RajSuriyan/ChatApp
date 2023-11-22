from typing import *
from flask import Flask,render_template,request,session,redirect,flash,url_for
from flask_socketio import join_room,leave_room,SocketIO,send
import random

from string import ascii_uppercase

app:Flask=Flask(__name__,static_folder="./static")
app.config["SECRET_KEY"]="sfadfdsdsjfhavfjvfdhvf"

socketio=SocketIO(app)
rooms:dict={}



def generate_unique_code(num)->str:
    while True:
        code:str=""
        for _ in range(num):
            code+=random.choice(ascii_uppercase)
        if code not in rooms:
            return code

@app.route("/",methods=["GET","POST"])
def home()->render_template:
    session.clear()    
    if request.method=='POST':
        name:str=request.form.get("name","")
        code:str=request.form.get("code","")
        join:Optional[bool]=request.form.get("join",False)
        create:Optional[bool]=request.form.get("create",False)
        
        
        if not name:
            flash("Enter the name to continue", 'error')
            return render_template("home.html",name=name,code=code)
        if join!=False and not code:
            flash("Enter the room code to continue", 'error')
            return render_template("home.html",name=name,code=code)
        room=code
        if create!=False:
            room=generate_unique_code(4)
            rooms[room]={"members":0,"messages":[]}
        elif code not in rooms:
            flash("Room Doesn't Exist", 'error')
            return render_template("home.html",name=name,code=code)
        session["room"]=room
        session["name"]=name
        return redirect(url_for("room"))       
    return render_template("home.html")




@app.route("/room")
def room()->render_template:
    
    room:str=session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    
    return render_template("room.html",code=room,message=rooms[room]["messages"])

@app.route("/available_rooms")
def available_rooms()->render_template:
    return render_template("avail.html",rooms=rooms)

@socketio.on("connect")
def connect(auth)->None:
    room:str=session.get("room")
    name:str=session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name":name,"message":"Has entered the room\n"},to=room)
    rooms[room]["members"]+=1
    print(f"{name} has joined the room: {room}")


@socketio.on("message")
def message(data):
    name=session.get("name")
    room=session.get("room")
    _message=data['data']
    if room not in rooms:
        return
    
    content={
        "name":name,
        "message":_message
    }
    send(content,to=room)
    print(f"{name}: {_message}")
    rooms[room]["messages"].append(content)
    




@socketio.on("disconnect")
def disconnect()->None:
    room=session.get("room")
    name=session.get("name")
    leave_room(room)
    if room in rooms:
        rooms[room]["members"]-=1
        if rooms[room]["members"]<=0:
            del rooms[room]
    send({"name":name,"message":"Has left the room"},to=room)
    print(f"{name} has left the room: {room}")
        
        
    
    

if __name__=="__main__":
    socketio.run(app,debug=True)
    