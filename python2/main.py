from flask import Flask,request,render_template,redirect,url_for,session,make_response
from os import getrandom
import json
app = Flask('GIGA_chat')
@app.route("/",methods=['GET','POST'])
def main():
    a=request.cookies.get('name')
    if a!=None:
        session['name']=a
    if request.method=='POST':
        b=request.form.get('reg')
        if request.form.get('enter')=='1':
            return redirect(url_for('login'))
        if request.form.get('reg')=='1':
            return redirect(url_for('reg'))
        if request.form.get('chats')=='1':
            return redirect(url_for('chats'))
        if request.form.get('cchat')=='1':
            return redirect(url_for('cchat'))
    return render_template('main.html',login=session.get('name'))
@app.route("/chats",methods=['POST','GET'])
def chats():
    if request.method=='POST':
        with open('chats.json','r') as db:
            data=json.load(db)
            chats=list(data.keys())
            session['chat']=request.form.get('chat')
            return redirect(url_for('chat'))
    if str(session.get('name'))!='None':
        with open('chats.json','r') as db:
            data=json.load(db)
            chats=list(data.keys())
            return render_template('chats.html',chats=chats)
    return redirect(url_for('main'))
@app.route("/reg",methods=['POST','GET'])
def reg():
    if request.method=='POST':
        log=request.form.get('username')
        pas=request.form.get('password')
        with open('db.json','r') as db:
            users=json.load(db)
            if len(log)!=0 and len(pas)>5 and users.get(log)==None:
                with open('db.json','w') as data:
                    if request.form.get('cookies')=='1':
                        res=make_response('reg.html')
                        res.set_cookie('name',log)
                    users[log]={'password':pas,'chats':[],'email':''}
                    json.dump(users,data)
                    session['name']=log
                    return redirect(url_for('main'))
    return render_template('reg.html')
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        log=request.form.get('username')
        pas=request.form.get('password')
        cookie=request.form.get('cookies')
        with open('db.json','r') as db:
            users=json.load(db)
            user=users.get(log)
            if user!=None and user.get('password')==pas:
                session['name']=log
                if cookie=='1':
                    res=make_response('reg.html')
                    res.set_cookie('name',log)
                return redirect(url_for('main'))
            else:
                redirect(url_for('main'))
    return render_template('reg.html')
@app.route("/chat",methods=['POST','GET'])
def chat():
    if str(session.get('name'))=='None':
        return redirect(url_for('login'))
    if request.method=='POST':
        msg=request.form.get('message-text')
        with open('chats.json','r') as chats:
            db=json.load(chats)
            sms=db.get(session.get('chat'))
            sms.append(session.get('name')+': '+msg)
            db[session.get('chat')]=sms
            with open('chats.json','w') as chats:
                json.dump(db,chats)
    with open('chats.json','r') as chats:
        db=json.load(chats)
        sms=db.get(session.get('chat'))
    return render_template('gigachat.html',message=sms)
@app.route("/cchat",methods=['POST','GET'])
def cchat():
    if str(session.get('name'))=='None':
        return redirect(url_for('login'))
    if request.method=='POST':
        namechat=request.form.get('name')
        with open('chats.json','r') as db:
            data=json.load(db)
            if data.get(namechat)==None:
                data[namechat]=[]
                with open('chats.json','w') as db:
                    json.dump(data,db)
                    return redirect(url_for('chats'))
    return render_template('cchat.html')
app.secret_key=getrandom(10)
app.run(host='0.0.0.0')
