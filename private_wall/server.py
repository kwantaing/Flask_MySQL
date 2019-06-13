from flask import Flask, render_template, request, redirect, flash, url_for, session
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re 

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

app = Flask(__name__)
app.secret_key="secret_key"
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    print(session)
    # session.clear()
    return render_template("index.html")

@app.route("/register", methods = ["POST"])
def register():
    mysql = connectToMySQL("private_wall")
    isValid = True
    if(len(request.form["password"])<5 or len(request.form["pwconfirm"])<5):
        flash("please make a valid password over 5 characters", 'register')
        isValid = False
    if (len(request.form["first_name"])<2):
        flash("First Name must be at least 2 characters", 'register')
        isValid = False
    if (len(request.form["last_name"])<2):
        flash("Last Name must be at least 2 characters", 'register')
        isValid = False
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!", 'register')
        isValid = False
    if isValid ==False:
        return redirect('/')
    hashedpw = (bcrypt.generate_password_hash(request.form["password"]))
    if not (bcrypt.check_password_hash(hashedpw, request.form["pwconfirm"])):
        flash("Passwords do not match!", 'register')
        isValid = False

    data = {
        'first_name' : request.form["first_name"],
        'last_name'  : request.form["last_name"],
        'email'      : request.form["email"],
        'pw'         : hashedpw
    }

    mysql2 = connectToMySQL("private_wall")
    checkemail = "SELECT email from USERS"
    all_emails = mysql2.query_db(checkemail)
    print(all_emails)
    for user in all_emails:
        if(user["email"]==request.form["email"]):
            isValid = False
            flash("email is already registered",'register')
            return redirect('/')

    if(isValid):
        query= "INSERT INTO USERS (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s, NOW(),NOW())"
        registered = mysql.query_db(query,data)
        session["current_id"]=registered
        return redirect('/success')
    else: 
        return redirect('/')

@app.route('/login', methods = ["POST"])
def login():
    mysql = connectToMySQL("private_wall")
    isValid = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!",'login')
        isValid = False
    if(len(request.form["password"])<1):
        flash("wrong password, try again",'login')
        isValid = False
    if isValid ==False:
        return redirect('/')
    data = {
        'email':request.form["email"],
        'pw': request.form["password"]
    }
    query = "SELECT * from USERS where email = %(email)s"
    info = mysql.query_db(query,data)
    print(info)
    print(bcrypt.check_password_hash(info[0]['password'],request.form["password"]))
    if not(bcrypt.check_password_hash(info[0]['password'],request.form["password"])):
        flash("wrong password, try again",'login')
        return redirect('/')
    else:
        session["current_id"]=info[0]["user_id"]
        print("success")
        print(session)

        return redirect (url_for("login_success"))

@app.route('/success')
def login_success():
    if bool(session)==False:
        print(session)
        return redirect('/')
    else:
        print(session)
        id = session["current_id"]
        response = "Welcome User id"
        mysql = connectToMySQL("private_wall")
        query = f"SELECT * FROM USERS WHERE user_id = {id}"
        result = mysql.query_db(query)
        print(result)
        recipients = load_send()
        messages = load_message()
        return render_template("wall.html",user = result, recipients= recipients, messages = messages)
#load all send message fields for other users
def load_send():
    mysql = connectToMySQL("private_wall")
    id = session["current_id"]
    query = f"SELECT user_id, first_name from USERS WHERE user_id !={id}"
    recipients = mysql.query_db(query)
    print(recipients)
    return (recipients)

@app.route('/send' ,methods=["POST"])
def send_message():
    data = {
        'sender_id': session["current_id"],
        'recipient_id': request.form["recipient_id"],
        'message': request.form["message"]
    }
    mysql = connectToMySQL("private_wall")
    query = "INSERT INTO MESSAGES (sender_id, recipient_id, content, created_at) VALUES (%(sender_id)s, %(recipient_id)s, %(message)s, NOW())"
    mysql.query_db(query,data)
    return redirect('/success')

def load_message():
    mysql = connectToMySQL("private_wall")
    session["msg_count"] = 0
    data = {
        'recipient_id' : session["current_id"]
    }
    query = "SELECT USERS.first_name, MESSAGES.message_id, MESSAGES.content, MESSAGES.created_at FROM MESSAGES LEFT JOIN USERS ON USERS.user_id = MESSAGES.sender_id WHERE MESSAGES.recipient_id = %(recipient_id)s"
    message = mysql.query_db(query,data)
    for messages in message:
        session["msg_count"]+=1
    print(message)
    return message

@app.route('/delete_msg', methods=["POST"])
def delete_msg():
    mysql = connectToMySQL("private_wall")
    data ={
        'message_id' : request.form["message_id"]
    }
    query="DELETE FROM MESSAGES WHERE message_id = %(message_id)s"
    mysql.query_db(query,data)
    return redirect('/success')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
    