from flask import Flask, jsonify
import time
import json

app = Flask(__name__)

@app.route('/currentDayTime/')
def getCurrentDayTime():
    current_time = time.ctime()
    parse_array = current_time.split(' ')
    current_day = parse_array[0]
    current_time = parse_array[3]
    parsed_array = [current_day, current_time]
    current_day_time_json = json.dumps(parsed_array)
    return (current_day_time_json)

print(getCurrentDayTime())



if __name__ == "__main__":
    app.run(debug = True,port= 8080)