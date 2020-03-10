import os
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Secret Key value
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
bcrypt = Bcrypt()



@app.route('/')
def index():
    if 'username' in session:
           return 'You are logged in as ' + session['username']

    return render_template('pages/index.html', films=mongo.db.films.find())



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form.get['username']})
    
        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')):
                session['username'] = request.form['username']
            return redirect(url_for('index'))

            return 'Invalid username/password combination'
            
    return render_template('pages/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash(f'Thank you for using FilmDB. Yippeekyay!!')
    return redirect(url_for('index'))

    


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('pages/register.html', title='Register')




@app.route("/createmovie", methods=['POST', 'GET'])  
def createmovie():
    """Allows a user to log in and create Movie information"""
    if request.method == "POST":
        film_data = mongo.db.films
        print(film_data)
        film_data.insert_one(request.form.to_dict())
        return render_template("pages/createmovie.html")

    return render_template("pages/createmovie.html")


@app.route("/createtv", methods=['POST', 'GET'])  
def createtv():
    """Allows a user to log in and create TV information"""
    if request.method == "POST":
        film_data = mongo.db.TVData
        print(mongo.db.TVData)
        film_data.insert_one(request.form.to_dict())
        return render_template("pages/createtv.html")

    return render_template("pages/createtv.html")

    


@app.route("/films")
def films():
    return render_template("pages/films.html")


@app.route("/contact")
def contact():
    return render_template("pages/contact.html")


# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000)),
    debug=True)
