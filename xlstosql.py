from typing import List
from venv import create
import xlrd
import pandas.io.sql as sql
from configparser import ConfigParser
import mysql.connector

def ActivitiesInfo(List):

    activity = {}

    activity['state'] = List[0]
    activity['state_abrv'] = List[1]
    activity['city'] = List[2]
    activity['street'] = List[3]
    activity['number'] = int(List[4])
    activity['venue'] = List[5]
    activity['name'] = List[6]
    activity['start'] = List[7]
    activity['end'] = List[8]
    activity['distance'] = int(List[9])
    activity['price'] = float(List[10])
    activity['website'] = List[11]
    activity['type'] = List[12]

    return activity
def xlsRead (filename):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    
    spread = []
    
    for r in range(1,sheet.nrows):
        row = []
        for c in range(sheet.ncols):
            if len(str(sheet.cell_value(r,c)))>0:
                row.append(sheet.cell_value(r,c))
            else:
                row.append(None)
        #print(row)
        spread.append(row)   
    return spread

def sqlConnect():
    username = input("What is the username?: ")
    passwrd = input("Please type your password: ")
    mydb = mysql.connector.connect(
        host = "localhost",
        user = username,
        password = passwrd
    )  
    return mydb

actlist = []
spreadsheet = xlsRead("Activities.xls")
for i in spreadsheet:
    print(f'{i}\n')
    actlist.append(ActivitiesInfo(i))
db = sqlConnect()
cursor = db.cursor()
sqlstate = []
cursor.execute("USE upact;")
cursor.execute("SELECT * FROM state;")
#Returns list
result = cursor.fetchall()
for sqlrow in result:
        sqlstate.append(sqlrow[1])
# print(sqlstate)
#print(type(result))

for xlrow in actlist:
    
    if xlrow['state'] not in sqlstate:
        cursor.execute(f"""
            INSERT INTO state(name,abrv)
            VALUES('{xlrow['state']}','{xlrow['state_abrv']}')
            """)
        sqlstate.append(xlrow['state'])
cursor.execute("SELECT * FROM state;")
staterow = cursor.fetchall()
# print(staterow)
stateDict = {}
for tuple in staterow:
    stateDict[tuple[1]] = tuple[0]
# print(stateDict)

for xlrow in actlist:
    cursor.execute(f"""INSERT INTO identifier(city,street,number,venue,name,start_date,end_date,distance,price,website,type,state_id) VALUES ('{xlrow['city']}','{xlrow['street']}',{xlrow['number']},'{xlrow['venue']}',"{xlrow['name']}",'{xlrow['start']}','{xlrow['end']}',{xlrow['distance']},{xlrow['price']},'{xlrow['website']}','{xlrow['type']}',{stateDict[xlrow['state']]});""")
query = "SELECT i.name,i.venue,i.start_date,i.number, i.street, i.city, s.abrv FROM state s JOIN identifier i ON i.state_id = s.state_id ORDER BY i.start_date;"
while query != "x":
    
    cursor.execute(query)
    tuplist = cursor.fetchall()
    for tup in tuplist:
        print(f'{tup}\n')
    query = input("What is your query? Type 'x' to exit. ")