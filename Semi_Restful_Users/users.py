from flask import Flask, render_template, request, redirect, url_for
from mysqlconnection import connectToMySQL  
app = Flask(__name__)   

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/users/new')
def redirect_new():
    return render_template('new.html')

@app.route('/create', methods=["POST"])
def add_user():
    print(request.form)
    mysql = connectToMySQL("semi_users")

    data={
        "first_name" : request.form["first_name"],
        "last_name"  : request.form['last_name'],
        "email"      : request.form['email']
    }
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES( %(first_name)s, %(last_name)s, %(email)s,   NOW(), NOW())"
    friends = mysql.query_db(query,data)
    print(friends)
    return redirect(url_for('info',id=friends))

    # return redirect('/')
@app.route('/users')
def all():
    mysql = connectToMySQL("semi_users")
    query="SELECT * from friends"
    result = mysql.query_db(query)
    print(result)
    return render_template("all.html", friends=result)
    
@app.route('/users/<id>')
def info(id):
    mysql = connectToMySQL("semi_users")
    query = f"SELECT * FROM friends WHERE friend_id = {id} "
    result = mysql.query_db(query)
    return render_template('user_postreg.html', result = result)

@app.route('/users/<id>/edit')
def edit(id):
    mysql = connectToMySQL("semi_users")
    query = f"SELECT * FROM friends WHERE friend_id = {id} "
    result = mysql.query_db(query)
    return render_template("edit.html", result = result)

@app.route('/update', methods=['POST'])
def update():
    print(request.form)
    mysql = connectToMySQL("semi_users")
    data={
        "first_name" : request.form["first_name"],
        "last_name"  : request.form['last_name'],
        "email"      : request.form['email'],
        "friend_id"  : request.form["friend_id"]
    }
    query = "UPDATE friends SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE friend_id = %(friend_id)s;"
    friends = mysql.query_db(query,data)
    print(friends)
    return redirect(url_for('info',id=request.form["friend_id"]))

@app.route('/users/<id>/destroy')
def destroy(id):
    mysql = connectToMySQL("semi_users")
    query = f"DELETE FROM friends where friend_id = {id}"
    result = mysql.query_db(query)
    return redirect('/users')
if __name__=="__main__":  
    app.run(debug=True)   
