""" integration with google sheets. url - https://docs.google.com/spreadsheets/d/1pn8RGkd6cFOjd67yUU-cKNrJkBU9Ml4FlU7DPU573Sc/edit#gid=0
    Uses IST timezone ."""

"""1st column, rows are Days. 1st row, columns are time slots in 24 hour format(imp)."""


import gspread
from pytz import timezone
from datetime import datetime


#get current day time indian standard time
def getCurrentDayTime():
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%a %H:%M:%S')  
    ind_time_arr = ind_time.split(' ')
    current_day, current_time = ind_time_arr[0], ind_time_arr[1]
    day_time_arr = [current_day, current_time]
    return (day_time_arr)

gc = gspread.service_account(filename="config/mcs-miniproject-7fdfa4473ccc.json")
sh = gc.open_by_key("1pn8RGkd6cFOjd67yUU-cKNrJkBU9Ml4FlU7DPU573Sc")

# write code to select with semester (sheet)

sheet = sh.sheet1  #sheet1 

def getDays():
    return(sheet.col_values(1))
all_days = getDays()


def getClassTimings():
    return(sheet.row_values(1))

all_class_timings = getClassTimings()
#remove ":" from all_class_timings and convert to int
all_class_timings = [s.replace(':', '') for s in all_class_timings]
all_class_timings = [int(x) for x in all_class_timings[1:]]


# call the current day time api
# def getDayTimeFromApi():
#     res = requests.get(CURRENT_TIME_API)
#     return(res.json())

parsedIndexValues = [] #returns [row,column]

# search for the day
def searchDayTimeValues():
    all_days = getDays()
    for index,day in enumerate(all_days):
        if day == getCurrentDayTime()[0]:
            parsedIndexValues.append(index+1) # appends row
    
    current_time = getCurrentDayTime()[1]
    current_time = current_time[:5] #perform string operations to remove seconds
    current_time = int(current_time.replace(':','')) #parse current_time 

    for index,class_time in enumerate(all_class_timings):
        
        if class_time > current_time :
            print()
            parsedIndexValues.append(index+1) #appends column
            return
    if current_time >= all_class_timings[-1]:
        parsedIndexValues.append(index+2)        
        

def fetchCellFromSheet(row,column):
    if type(column) != int:
        return "no class going on"
    return(sheet.cell(row,column).value)

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    searchDayTimeValues()
    row, column = parsedIndexValues[0], parsedIndexValues[1]
    current_class = fetchCellFromSheet(row,column)
    if current_class is None:
        return jsonify("no class")
    return jsonify(current_class)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    