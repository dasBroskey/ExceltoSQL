# Overview

This is a program to transfer data from a excel (xls) file to a SQL database. The program only works for the activities xls file but with future updates hopefully will work with 
more files. The SQL database needs to be created first and the program will write the data into SQL. To run this program there is base knowledge of SQL needed as the program currently does
not provide an interface to work with the data.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of the cloud database.}

[Software Demo Video](https://www.youtube.com/watch?v=VJbHzxzYCYo)

# Cloud Database

SQL is the used database with data transfered from Excel to SQL with a Python prgram.

The structure is two tables, the first table is a state table with state_id, name, and abreviated columns. The second table includes all the data about the activity
such as the city, street, address number, venue, activity name, start_date, end_date, distance from Rexburg, ID, price, website, activity type, and a foreign
key state_id.

# Development Environment

MySQL Database was used to write and create the database. Excel was used to collect the data. Python was used as a path between Excel and SQL.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [From Excel to Databse tutorial][(http://url.link.goes.here)](https://medium.com/financeexplained/from-excel-to-databases-with-python-c6f70bdc509b)
* [xlrd Python Documentation][(http://url.link.goes.here)](https://xlrd.readthedocs.io/en/latest/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* UI for easier search of the database
* Implement functions for multiple databases
* Function to read what the database needs for tables
