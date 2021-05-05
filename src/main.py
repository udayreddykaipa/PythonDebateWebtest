from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import datetime
import string
import random

# from datetime import datetime
# now = datetime.now()
# id = 1
# formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
app.secret_key = "V5WEM9QR2O6QN548V5WEM9QR2O6QN548"


def connect_mysql():
    cnx = mysql.connector.connect(user="root", password="",
                                  host="127.0.0.1", database="test"
                                  )

    # mycursor = cnx.cursor()
    return cnx


@app.route('/user')
def loggedin():
    if(session.get('uname')):
        cnx = mysql.connector.connect(user="root", password="",
                                    host="127.0.0.1", database="test"
                                    )
        mycursor = cnx.cursor()
        mycursor.execute("SELECT `comment`, `time`, `tid` FROM `topic` WHERE 1")
        fetched_topics = mycursor.fetchall()
        mycursor.execute("SELECT `comment`, `timestamp`, `cid`, `relatedID`, `claimType` FROM `claims` WHERE 1")
        fetched_claims = mycursor.fetchall()
        mycursor.execute("SELECT `comment`, `timestamp`, `rid`, `cat`, `relatedID`, `relatedIDType` FROM `reply` WHERE 1")
        fetched_replies = mycursor.fetchall()
        return render_template('login.html', topics=fetched_topics, claims=fetched_claims, replies=fetched_replies,uname=session.get('uname'))
    return redirect(url_for('home'))
    

@app.route('/')
def home():
    if(session.get('uname')):
        print("already loggedin as:"+session['uname'])
        return redirect(url_for('loggedin'))
    cnx = mysql.connector.connect(user="root", password="",
                                  host="127.0.0.1", database="test"
                                  )
    mycursor = cnx.cursor()
    mycursor.execute("SELECT `comment`, `time`, `tid` FROM `topic` WHERE 1")
    fetched_topics = mycursor.fetchall()
    mycursor.execute("SELECT `comment`, `timestamp`, `cid`, `relatedID`, `claimType` FROM `claims` WHERE 1")
    fetched_claims = mycursor.fetchall()
    mycursor.execute("SELECT `comment`, `timestamp`, `rid`, `cat`, `relatedID`, `relatedIDType` FROM `reply` WHERE 1")
    fetched_replies = mycursor.fetchall()
    return render_template('home.html', topics=fetched_topics, claims=fetched_claims, replies=fetched_replies, uname=session.get('uname'))


@app.route('/claims')
def claims():
    return render_template('login.html')

# called when login btn clicked
@app.route('/login', methods=['POST'])
def login():
    print("SELECT * FROM user where username='" +
          request.form["username"]+"' and pwd='"+request.form["lpwd"]+"'")
    cnx = mysql.connector.connect(user="root", password="",
                                  host="127.0.0.1", database="test"
                                  )

    # print(request.form.get('luname',"")) #list of tuples
    mycursor = cnx.cursor()
    mycursor.execute("SELECT * FROM user where username='" +
                     request.form["username"]+"' and pwd='"+request.form["lpwd"]+"'")
    myresult = mycursor.fetchall()
    print(myresult, len(myresult))
    if(len(myresult) == 1):
        cnx.close()
        session['uname'] = myresult[0][0]
        session['uid'] = myresult[0][2]
        return redirect(url_for('loggedin'))
    else:
        cnx.close()
        return redirect(url_for('home'))

# called when register btn clicked
@app.route('/register', methods=['POST'])
def register():
    # check if pwd matches in 2 fields
    if(request.form["rpwd1"] == request.form["rpwd2"]):
        try:
            print("INSERT INTO `user`(`username`, `pwd`, `uid`) VALUES ('" +
                  request.form["runame"]+"','"+request.form["rpwd1"]+"','"+uid_generator()+"')")
            cnx = mysql.connector.connect(user="root", password="",
                                          host="127.0.0.1", database="test"
                                          )

            # print(request.form.get('luname',"")) #list of tuples
            mycursor = cnx.cursor()
            uid_str = uid_generator()
            mycursor.execute("INSERT INTO `user`(`username`, `pwd`, `uid`) VALUES ('" +
                             request.form["runame"]+"','"+request.form["rpwd1"]+"','"+uid_str+"')")
            cnx.commit()
            if(mycursor.rowcount == 1):
                cnx.close()
                session['uname'] = request.form["runame"]
                session['uid'] = uid_str
                return redirect(url_for('loggedin'))
            else:
                cnx.close()
                return redirect(url_for('home'))
        except:
            con.rollback()
            msg = "error in insert operation"
    else:
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    print("ihio")
    session.pop('uname', None)
    session.pop('uid', None)
    # flash('logged out successfully')
    return redirect(url_for('home'))


@app.route('/addtopic',  methods=['POST'])
def addTopic():
    if(session.get('uname')):
        print("already loggedin as:"+session['uname'])
        cnx = mysql.connector.connect(user="root", password="",
                                          host="127.0.0.1", database="test"
                                          )
        # print(request.form.get('luname',"")) #list of tuples
        mycursor = cnx.cursor()
        uid_str = uid_generator()
        mycursor.execute("INSERT INTO `topic`(`comment`, `time`, `tid`) VALUES ('"+request.form['title']+"|"+request.form['content']+"','"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"','"+uid_generator()+"')")
        cnx.commit()
        if(mycursor.rowcount == 1):
            cnx.close()

            return redirect(url_for('loggedin'))

        # return redirect(url_for('loggedin'))
    # return render_template('home.html')


@app.route('/addclaim',  methods=['POST'])
def addClaim():
    if(session.get('uname')):
        print("already loggedin as:"+session['uname'])
        cnx = mysql.connector.connect(user="root", password="",
                                          host="127.0.0.1", database="test"
                                          )
        
        mycursor = cnx.cursor()
        uid_str = uid_generator()
        print("INSERT INTO `claims`(`comment`, `timestamp`, `cid`, `relatedID`, `claimType`) VALUES ('"+request.form['claim']+"','"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"','"+uid_generator()+"','"+request.form['id']+"','1')")
        mycursor.execute("INSERT INTO `claims`(`comment`, `timestamp`, `cid`, `relatedID`, `claimType`) VALUES ('"+request.form['claim']+"','"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"','"+uid_generator()+"','"+request.form['id']+"','1')")
        cnx.commit()
        if(mycursor.rowcount == 1):
            cnx.close()

            return redirect(url_for('loggedin'))
        
    return redirect(url_for('/'))


@app.route('/addreply',  methods=['POST'])
def addReply():
    if(session.get('uname')):
        print("already loggedin as:"+session['uname'])
        cnx = mysql.connector.connect(user="root", password="",
                                          host="127.0.0.1", database="test"
                                          )
        mycursor = cnx.cursor()
        uid_str = uid_generator()
        print("INSERT INTO `reply`(`comment`, `timestamp`,`rid`, `cat`, `relatedID`, `relatedIDType`) VALUES ('"+request.form['claim']+"','"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"','','"+uid_generator()+"','"+request.form['id']+"','1')")
        mycursor.execute("INSERT INTO `reply`(`comment`, `timestamp`, `rid`, `cat`, `relatedID`, `relatedIDType`) VALUES ('"+request.form['claim']+"','"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"','','"+uid_generator()+"','"+request.form['id']+"','1')")
        cnx.commit()
        if(mycursor.rowcount == 1):
            cnx.close()
            return redirect(url_for('loggedin'))
        
    return redirect(url_for('/'))

def uid_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
