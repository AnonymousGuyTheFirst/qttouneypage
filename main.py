from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    countfile = open("playercount.txt", "r")                # Open file with playercount
    data = countfile.read()                                 # Save into memory
    countfile.close()                                       # Close that shit
    return render_template("index.html", playercount=data)  # Parse playercount to template
