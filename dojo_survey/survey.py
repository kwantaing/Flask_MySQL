from flask import Flask, render_template, request,redirect, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)  
app.secret_key = "yeet"
@app.route('/')
def home():
    return render_template('form.html')

@app.route('/result',methods = ['POST'])
def result():
    print("Got request Info")
    print(request.form)

    mysql = connectToMySQL("Dojo_Survey")

    data={
        "name": request.form["name"],
        "location" : request.form["location"],
        "fav_language" : request.form["fav_language"],
        "comment" : request.form["comment"]
    }
    isValid = True

    if (len(request.form['name'])<1):
        isValid = False
        flash("name field is required")
    if(len(request.form['comment'])>120):
        isValid = False
        flash("please keep your comment under 120 characters")
    if(isValid):
        query = "INSERT INTO information ( name, location, fav_language, comment, created_at, updated_at) VALUES( %(name)s, %(location)s, %(fav_language)s, %(comment)s, NOW(), NOW())"
        result = mysql.query_db(query,data)
        mysql2 = connectToMySQL("Dojo_Survey")
        name = data["name"]
        query2 = f"SELECT * FROM information where User_id = {result}"
        result2 = mysql2.query_db(query2)
        print(result2)
        return render_template("result.html",result = result2)
    else:
        return redirect('/')

if __name__=="__main__":  
    app.run(debug=True)    