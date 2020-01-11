from flask import Flask, render_template

app = Flask (__name__)

@app.route("/index")
def index ():
    return render_template("index.html")

@app.route("/films")
def index ():
    return render_template("films.html")    

@app.route("/tv")
def tv():
    return render_template("tv.html")

@app.route("/casting")
def Casting():
    return render_template("casting")
   
if __name__ == "__main__":
    app.run(debug=True)
