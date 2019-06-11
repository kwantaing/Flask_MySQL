from flask import Flask, render_template, redirect, flash, url_for, request
from mysqlconnection import connectToMySQL
import re


app = Flask(__name__)
app.secret_key="email validation"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/submit', methods=["POST"])
def submit():
    mysql = connectToMySQL('email_valid')
    data = {
        'email':request.form['email']
    }
    isValid = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
        isValid = False
        return render_template("error.html")
    else:
        query="INSERT INTO email (email, created_at) VALUES (%(email)s, NOW())"
        inserted = mysql.query_db(query,data)
        id = int(inserted)
        mysql1 = connectToMySQL('email_valid')
        query1 = f"SELECT * FROM email WHERE id = {id}"
        result = mysql1.query_db(query1)

        mysql2 = connectToMySQL("email_valid")
        query2 = "SELECT * FROM email"
        emails = mysql2.query_db(query2)
        return render_template('success.html', result = result, emails = emails) 

# @app.route('/print')
# def print():
@app.route("/delete/<id>")
def delete(id):
    mysql = connectToMySQL("email_valid")
    query= f"DELETE FROM email WHERE id = {id}"
    deleted = mysql.query_db(query)
    mysql1 = connectToMySQL("email_valid")
    query1 = "SELECT * FROM email"
    result = mysql1.query_db(query1)
    print(result)
    return render_template('all.html', emails = result)



if __name__=="__main__":
    app.run(debug=True)
