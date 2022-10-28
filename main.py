from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import pyrebase
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

"""example output:  {'display_text': ['hello!'], 'clock': ['on'], 'TimeTable': ['Sat', '16:33:41']} """


# firebase_config = {"apiKey": "AIzaSyDMAxF4jqNKGy1zyV6GMgT2qxYbr1mG6bY",

#   "authDomain": "gpd-2-fab7c.firebaseapp.com",

#   "projectId": "gpd-2-fab7c",

#   "storageBucket": "gpd-2-fab7c.appspot.com",

#   "messagingSenderId": "1061276271847",

#   "appId": "1:1061276271847:web:69662a45954d944b78ce42",

#     "databaseURL" : "https://gpd-2-fab7c-default-rtdb.firebaseio.com/"
# }

firebase_config = {
   "apiKey" : os.getenv('API_KEY'),
   "authDomain" : os.getenv("authDomain"),
   "projectId" : os.getenv("projectId"),
   "storageBucket" : os.getenv("storageBucket"),
   "messagingSenderId" : os.getenv("messagingSenderId"),
   "appId" : os.getenv("appId"),
   "databaseURL" : os.getenv("databaseURL")
}
print(firebase_config)

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()

@app.route('/')
def home():
   return render_template('index.html')

def fetchTimeTableApi():
   response_data =  requests.get("http://127.0.0.1:8080/currentDayTime/")
   response_data = response_data.content
   response_data_parsed = str(response_data)[2:-1]
   resp_data_dict = {"TimeTable":json.loads(response_data_parsed)}
   return(resp_data_dict)


@app.route('/api',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      form_data = request.form.to_dict(flat=False)
      result = form_data  
      result.update(fetchTimeTableApi()) 
      #print(result)
      db.push(result)
      return render_template("result.html")


if __name__ == '__main__':
   app.run(debug = True)