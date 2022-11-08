from flask import Flask, render_template, request, jsonify
app = Flask(__name__, template_folder="")
import pyrebase
import requests
import os
from dotenv import load_dotenv
load_dotenv()

"""example output:  {'display_text': ['hello!'], 'clock': ['on'], 'TimeTable': "DSP"} """

firebase_config = {
   "apiKey" : os.getenv('API_KEY'),
   "authDomain" : os.getenv("authDomain"),
   "projectId" : os.getenv("projectId"),
   "storageBucket" : os.getenv("storageBucket"),
   "messagingSenderId" : os.getenv("messagingSenderId"),
   "appId" : os.getenv("appId"),
   "databaseURL" : os.getenv("databaseURL")
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()

@app.route('/')
def home():
   return render_template('templates/index.html')

def fetchTimeTableApi():
   response_data =  requests.get("https://timetableapi.pythonanywhere.com/")
   return(response_data.json())

@app.route('/api',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      form_data = request.form.to_dict(flat=False)
      if "time-table" in form_data:
         form_data['time-table'] = str(fetchTimeTableApi())

      del form_data['sems'] #this seems unnecessary to push to storage.
      db.push(form_data)
      return render_template("templates/result.html")


if __name__ == '__main__':
   app.run(debug = True)