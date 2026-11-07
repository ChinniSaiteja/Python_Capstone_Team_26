# Python_Capstone_Team_26
# AI-powered Waste Sorting &amp; Recycling Assistant
## Homework Assignment 3 – Waste Management Web App (Flask + MySQL)

#### Project Structure

<img width="662" height="396" alt="image" src="https://github.com/user-attachments/assets/24c4823d-1e15-4786-9e63-f36e16cb8540" />

#### How it works
#### 1)MySQL database: the waste_management database contains a waste_items table with the waste-item records.
#### 2)Flask application: database.py reads the connection settings from the .env file, connects to MySQL with mysql-connector-python, and retrieves all rows from waste_items. app.py calls this function in the / route.
#### 3)Webpage: the records are passed to templates/index.html, which displays them in an HTML table styled by static/style.css.

<img width="660" height="110" alt="image" src="https://github.com/user-attachments/assets/9e7473f9-bdca-430d-a4d7-b017295c7563" />

#### Requirements
#### 1.Python 3.12
#### 2.MySQL Server 8.x (and optionally MySQL Workbench)
#### 3.Python packages listed in requirement.txt:
##### Flask
##### mysql-connector-python
##### python-dotenv
   


