import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api/v1/<station>/<date>')
def api(station, date):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    print('filename', filename)
    
    # Read the CSV with correct column names
    df = pd.read_csv(
        filename, 
        skiprows=20, 
        parse_dates=["    DATE"],  # 4 spaces before DATE
        header=0  # Use the first row after skiprows as header
    )
    
    # Convert date to match the format in your CSV (YYYYMMDD)
    date_str = date.replace("-", "")  # Convert "YYYY-MM-DD" to "YYYYMMDD"
    
    # Filter the data (note the 4 spaces before DATE and TG)
    temperature = df.loc[df['    DATE'] == date_str]['   TG'].squeeze() / 10
    
    return {
        "station": station, 
        "date": date, 
        "temperature": temperature
    }

app.run(debug=True, port=5000)