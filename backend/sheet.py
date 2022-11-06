""" integration with google sheets, also includes queries.
    Uses api/currentDayTime for necessary queries."""

"""1st column, rows are Days. 1st row, columns are time slots in 24 hour format(imp)."""


import gspread
import requests
CURRENT_TIME_API = "http://127.0.0.1:5000/currentDayTime"


gc = gspread.service_account(filename="config/mcs-miniproject-7fdfa4473ccc.json")
sh = gc.open_by_key("1pn8RGkd6cFOjd67yUU-cKNrJkBU9Ml4FlU7DPU573Sc")

# # def pickFile(sem):
# #     print(sem)
# #     return(sh.sem)

# SemToSheet = {
#     "sheet1": "5th",
#     "sheet2" : "7th",
#     "sheet3" : "3rd"
# }

sheet = sh.sheet1

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
def getDayTimeFromApi():
    res = requests.get(CURRENT_TIME_API)
    return(res.json())


parsedIndexValues = [] #returns [row,column]


# search for the day
def searchDayTimeValues():
    all_days = getDays()
    for index,day in enumerate(all_days):
        if day == getDayTimeFromApi()[0]:
            parsedIndexValues.append(index+1) # appends row
    
    current_time = getDayTimeFromApi()[1]
    current_time = current_time[:5] #perform string operations to remove seconds
    current_time = int(current_time.replace(':','')) #parse current_time 

    for index,class_time in enumerate(all_class_timings):
        if class_time > current_time:
            parsedIndexValues.append(index+1) #appends column
            return
searchDayTimeValues()


def fetchCellFromSheet(row,column):
    return(sheet.cell(row,column).value)



from flask import Flask, jsonify
app = Flask(__name__)
row = parsedIndexValues[0]
column = parsedIndexValues[1]
current_class = fetchCellFromSheet(row,column)
print(current_class)


@app.route('/currentClass')
def main():
    return jsonify(current_class)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    
