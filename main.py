from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api/v1/<station>/<date>')
def api(station, date):
    temperature = 24
    return {station: station, "date": date, "temperature": temperature}

app.run(debug=True, port=5000)