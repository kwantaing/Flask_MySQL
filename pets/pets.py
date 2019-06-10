from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('mydb')	        # call the function, passing in the name of our db
    pets = mysql.query_db('SELECT * FROM pets;')  # call the query_db function, pass in the query as a string
    print(pets)

    return render_template("index.html",pets= pets)
            
@app.route("/addpet", methods=["POST"])
def add():
    mysql = connectToMySQL('mydb')
    print(request.form)
    data={
        "name":request.form["name"],
        "type":request.form["type"]
    }
    query = "INSERT into pets (name,type,created_at,updated_at) VALUES (%(name)s, %(type)s,NOW(),NOW() );"
    mysql.query_db(query,data)
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
    