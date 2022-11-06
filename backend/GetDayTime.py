from flask import Flask, jsonify
from pytz import timezone
from datetime import datetime

app = Flask(__name__)

@app.route('/currentDayTime/')
def getCurrentDayTime():
    with app.app_context():
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%a %H:%M:%S')  
        ind_time_arr = ind_time.split(' ')
        current_day, current_time = ind_time_arr[0], ind_time_arr[1]
        day_time_arr = [current_day, current_time]
        return jsonify(day_time_arr)

print(getCurrentDayTime())



if __name__ == "__main__":
    app.run(debug = True, port=5000)