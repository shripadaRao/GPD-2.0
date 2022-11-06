from flask import Flask, jsonify
import time
import json

app = Flask(__name__)

@app.route('/currentDayTime/')
def getCurrentDayTime():
    with app.app_context():
        current_time = time.ctime()
        parse_array = current_time.split(' ')
        global parsed_array
        current_day = parse_array[0]
        current_time = parse_array[4]
        parsed_array = [current_day, current_time]
        return jsonify(parsed_array)

print(getCurrentDayTime())



if __name__ == "__main__":
    app.run(debug = True, port=5000)