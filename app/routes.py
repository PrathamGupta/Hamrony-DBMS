from flask import Flask, render_template, flash, redirect, url_for, request, json
from app import app, mysql

#Global Variables
countMatch=-1
artistName=''
userData = []
userRow=[]
dic={}
userLogged=()



@app.route('/')
def main():
    global dic
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    user=cur.fetchall()
    for i in user:
        dic[i] = False
    return redirect("http://127.0.0.1:5000/"+"Login")




@app.route('/Login', methods  =['POST','GET'])
def login():
    global dic
    global userLogged
    # loggedIn= False
    print("HERE")
    if request.method == 'POST' and 'email' in request.form and 'passwd' in request.form:
        email=request.form['email']
        passwd=request.form['passwd']
        print("HERE2")
        cur=mysql.connection.cursor()
        print("HERE3")
        cur.execute('SELECT * FROM users where email=%s and passwd=%s', (email, passwd))
        user=cur.fetchone()
        userLogged=user
        print(user)
        # if(user):
        print("HERE4")
        dic[user]=True
        print(dic[user])
        if(dic[user]==True):
            return redirect("http://127.0.0.1:5000/"+"HomePage")
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')



@app.route('/Register', methods=['POST','GET'])
def register():
    msg=''
    email=""
    password=""
    name=""
    print("HERE2")
    if request.method == 'POST':
        print("HERE")
        if 'uname' in request.form and 'uname'.lower()!='admin' and 'passwd' in request.form and 'email' in request.form and 'gender' in request.form and 'dob' in request.form:
            name=request.form['uname']
            passwd=request.form['passwd']
            email=request.form['email']
            gender=request.form['gender']
            dob=request.form['dob']
            cur=mysql.connection.cursor()
            print(email)
            cur.execute('SELECT * FROM users WHERE email=%s',(email,))
            if cur.fetchone():
                return render_template('reg.html')
            print(email)
            cur.execute('SELECT COUNT(*) FROM users')
            cur.execute('INSERT INTO users(user_id, Name, email, passwd, gender, dob) VALUES (%s, %s, %s, %s, %s, %s)', (int(cur.fetchone()[0])+1,name, email, passwd, gender, dob))
            mysql.connection.commit()
            return redirect("http://127.0.0.1:5000/")
        else:
            return render_template('reg.html')
    else:
        return render_template('reg.html')



@app.route('/HomePage', methods=['POST','GET'])
def homePage():
    global dic
    global userLogged
    print("HOMEPAGE")
    if( userLogged not in dic or dic[userLogged] is False):
        return redirect("http://127.0.0.1:5000/"+"Login")
    else:
        return render_template('homePage.html', uname=userLogged[1])



@app.route('/Profile', methods=['POST','GET'])
def profile():
    global dic
    global userLogged
    if(request.method=='GET'):
        if( userLogged not in dic or dic[userLogged] is False):
            return redirect("http://127.0.0.1:5000/"+"Login")
        else:
            return render_template('profilePage.html', user=userLogged)
    if(request.method=='POST' and 'passwd' in request.form):
        userLogged[1]!='admin'
        cur=mysql.connection.cursor()
        userLogged[3]=request.form['passwd']
        cur.execute('UPDATE users SET passwd=%s WHERE user_id=%s',(request.form['passwd'], userLogged[0]))
        mysql.connection.commit()
        return render_template('profilePage.html', user=userLogged)



@app.route('/meet')
def artistPick():
    global dic
    global userLogged
    if(request.method=='GET'):
        if( userLogged not in dic or dic[userLogged] is False):
            return redirect("http://127.0.0.1:5000/"+"Login")
    curr=mysql.connection.cursor()
    curr.execute("select * from artists order by artists.artist_id")
    data = curr.fetchall()
    return render_template("artist.html", info=data)



@app.route('/match', methods=['GET', 'POST'])
def match():
    global countMatch
    global userData
    global userRow
    global artistName
    global dic
    global userLogged
    if(request.method=='GET'):
        if( userLogged not in dic or dic[userLogged] is False):
            return redirect("http://127.0.0.1:5000/"+"Login")
    if request.method == 'POST':
        artistName = request.form.get('comp_select')

        # Find Artist Details
        curr=mysql.connection.cursor()
        sql_select_query = """select * from artists a where a.name = %s"""
        curr.execute(sql_select_query, (artistName,))
        data = curr.fetchall()
    
        #Finding Users with the same interest
        sql_select_query = """select * from fav_artists f where f.artist_id = %s"""
        curr.execute(sql_select_query, (data[0][0],))
        data=curr.fetchall()
        list_of_user=[]
        for i in data:
            list_of_user.append(i[0])
        print(list_of_user)

        # Find Matching User Id's
        sql_select_query = """ select * from users u where u.user_id in %s"""
        curr.execute(sql_select_query, (list_of_user, ))
        data=curr.fetchall()
        userData=data
        countMatch=-1

    countMatch+=1
    if countMatch==len(userData):
        countMatch=0   
    userRow=userData[countMatch]
    print(countMatch)

    return render_template("meet.html", info=userRow)




@app.route('/connect', methods=['GET', 'POST'])
def connect():
    global artistName
    global dic
    global userLogged
    if(request.method=='GET'):
        if( userLogged not in dic or dic[userLogged] is False):
            return redirect("http://127.0.0.1:5000/"+"Login")

    userId = request.form.get('userid')
    userName = request.form.get('userName')

    # Find Artist Details
    curr=mysql.connection.cursor()
    sql_select_query = """select * from artists a where a.name = %s"""
    curr.execute(sql_select_query, (artistName,))
    data = curr.fetchall()

    #Adding to User connections
    tup=(userId, data[0])
    # sql_select_query = """ insert into  %s"""
    # curr.execute(sql_select_query, tup)
    # data = curr.fetchall()

    print(userId)
    return render_template('connected.html', info=userName)