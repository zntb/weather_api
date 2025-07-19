import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


stations  = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 ", "CN" ]]

@app.route('/')
def home():
    return render_template("home.html", data=stations.to_html(classes='data', header="true", index=False))


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
 
    
@app.route('/api/v1/<station>')
def all_data(station):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(
        filename,
        skiprows=20,
        parse_dates=["    DATE"],
        header=0
    )
    result = df.to_dict(orient='records')
    return {
        "station": station,
        "data": result
    }
  
    
@app.route('/api/v1/yearly/<station>/<year>')
def yearly_data(station, year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(
        filename,
        skiprows=20,
        header=0
    )
    
    df['    DATE'] = df['    DATE'].astype(str)  # Ensure DATE is string for filtering
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient='records')
    return result

if __name__ == '__main__':
    app.run(debug=True)