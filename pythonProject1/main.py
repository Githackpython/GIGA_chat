from flask import Flask,request,render_template,redirect,url_for,session
from os import getrandom
app = Flask('GIGA_chat')
@app.route("/",methods=['GET','POST'])
def main():
    if request.method=='POST':
        a=request.form.get('enter')
        b=request.form.get('reg')
        if a=='1':
            return redirect(url_for('login'))
        if b=='1':
            return redirect(url_for('reg'))
    return render_template('main.html')
@app.route("/reg",methods=['POST','GET'])
def reg():
    if request.method=='POST':
        log=request.form.get('username')
        pas=request.form.get('password')
        with open('db.txt','r') as db:
            a=db.readlines()
            if not(str(log+':'+pas+';'+'\n') in a):
                with open('db.txt','a') as data:
                    data.write(log+':'+pas+';'+'\n')
                    session['name']=log
                    return redirect(url_for('chat'))
    return render_template('reg.html')
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        log=request.form.get('username')
        pas=request.form.get('password')
        with open('db.txt','r') as db:
            a=db.readlines()
            if str(log+':'+pas+';'+'\n') in a:
                session['name']=log
                return redirect(url_for('chat',name=log))
            else:
                redirect(url_for('login'))
    return render_template('reg.html')
@app.route("/chat",methods=['POST','GET'])
def chat():
    if str(session.get('name'))=='None':
        return redirect(url_for('login'))
    if request.method=='POST':
        msg=request.form.get('message-text')
        with open('msg.txt','a') as msgs:
            msgs.write(str(session.get('name'))+': '+msg+'\n')
    with open('msg.txt','r') as msgs:
        a=msgs.readlines()
        if len(a)>50:
            f=open('msg.txt', 'w+')
            f.seek(0)
            f.close()
    return render_template('gigachat.html',message=a)
app.secret_key=getrandom(10)
app.run(host='0.0.0.0')
