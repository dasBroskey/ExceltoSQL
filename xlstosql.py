import xlrd
import mysql.connector
import maskpass

def ActivitiesInfo(List):
    #Returns dictionary for insert statements
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
    #Reads filename and returns list of rows
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    spread = []
    #Create list or rows read from .xls file
    for r in range(1,sheet.nrows):
        row = []
        for c in range(sheet.ncols):
            if len(str(sheet.cell_value(r,c)))>0:
                row.append(sheet.cell_value(r,c))
            else:
                row.append(None)
        spread.append(row)   
    return spread

def sqlConnect():
    #connects to SQL server with username and password
    username = input("What is the username?: ")
    #hides password input
    passwrd = maskpass.askpass(mask='*')
    mydb = mysql.connector.connect(
        host = "localhost",
        user = username,
        password =  passwrd
    )  
    #returns database
    return mydb

#global variables used to hold data
actlist = []
sqlstate = []
stateDict = {}

#Create list of lists(rows) from database
spreadsheet = xlsRead("Activities.xls")
#Creates dictionary for each row
for i in spreadsheet:
    actlist.append(ActivitiesInfo(i))

#Connect to database and initialize cursor
db = sqlConnect()
cursor = db.cursor()

#Retrieve states already in database
cursor.execute("USE upact;")
cursor.execute("SELECT * FROM state;")
#Returns list of states already in database
result = cursor.fetchall()
for sqlrow in result:
    #Create list of states already in database
    sqlstate.append(sqlrow[1])

for xlrow in actlist:
    #For each row of data that state is not in database insert state data into database
    if xlrow['state'] not in sqlstate:
        cursor.execute(f"""
            INSERT INTO state(name,abrv)
            VALUES('{xlrow['state']}','{xlrow['state_abrv']}')
            """)
        sqlstate.append(xlrow['state'])

cursor.execute("SELECT * FROM state;")
#Retrieve and store all states in database
staterow = cursor.fetchall()
#Create dictionary for states and state_id for SQL Insert statement
for tuple in staterow:
    stateDict[tuple[1]] = tuple[0]

#Insert activities data into database using dictionary
for xlrow in actlist:
    cursor.execute(f"""INSERT INTO identifier(city,street,number,venue,name,start_date,end_date,distance,price,website,type,state_id) VALUES ('{xlrow['city']}','{xlrow['street']}',{xlrow['number']},'{xlrow['venue']}',"{xlrow['name']}",'{xlrow['start']}','{xlrow['end']}',{xlrow['distance']},{xlrow['price']},'{xlrow['website']}','{xlrow['type']}',{stateDict[xlrow['state']]});""")
#Base query to return all data in database
query = "SELECT i.name,i.venue,i.start_date,i.number, i.street, i.city, s.abrv FROM state s JOIN identifier i ON i.state_id = s.state_id ORDER BY i.start_date;"

#Loop for user input
while query != "x": 
    cursor.execute(query)
    tuplist = cursor.fetchall()
    for tup in tuplist:
        print(f'{tup}\n')
    query = input("What is your query? Type 'x' to exit. ")

db.commit()