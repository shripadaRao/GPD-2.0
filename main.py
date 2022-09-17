from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import pyrebase
import requests
import json

"""example output:  {'display_text': ['hello!'], 'clock': ['on'], 'TimeTable': ['Sat', '16:33:41']} """


firebase_config = {"apiKey": "AIzaSyDMAxF4jqNKGy1zyV6GMgT2qxYbr1mG6bY",

  "authDomain": "gpd-2-fab7c.firebaseapp.com",

  "projectId": "gpd-2-fab7c",

  "storageBucket": "gpd-2-fab7c.appspot.com",

  "messagingSenderId": "1061276271847",

  "appId": "1:1061276271847:web:69662a45954d944b78ce42",

    "databaseURL" : "https://gpd-2-fab7c-default-rtdb.firebaseio.com/"
}

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

# def parseImmutableDict(form_data):
#    print("response: ", form_data)
#    form_data_str= str(form_data)
#    form_data_str= form_data_str[20:-2]
#    form_data_str.replace("(","[")
#    form_data_str.replace(")","]")
#    print("form_data_str: ", form_data_str)
#    form_data_parsed = list(form_data_str)
#   # print("form_data_parsed: ", form_data_parsed)
#    #print(form_data_parsed)
   # return(str(form_data))

#print(fetchTimeTableApi())

@app.route('/api',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      form_data = request.form.to_dict(flat=False)
      result = form_data  
      result.update(fetchTimeTableApi()) 
      print(result)
      #print(jsonify(result))
      #db.push(result)
      #return("Response Submitted!" + "Output: " +str(result))
      return render_template("result.html")


if __name__ == '__main__':
   app.run(debug = True)