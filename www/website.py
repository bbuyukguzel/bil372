from flask import Flask
from flask import render_template, request
from sqlalchemy import *
from sqlalchemy.engine.url import URL
import setting
app = Flask(__name__)

db = None

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def homepage():
    return render_template('/index.html')


@app.route('/profile/<id>')
def profile(id):
    return render_template('/profile.html', data= getName(id))


@app.route('/result', methods=['POST'])
def result():
    keyword = request.form["x"]
    # print("id: %s", id)
    l = list()


    for i in res:
        l.append(select(i[0], i[1], ""))


    return render_template('/result.html', key=id, data=l)

def db_connect():
    return create_engine(URL(**setting.DATABASE))

def getName(id):
    c = db.connect()
    query = "select fname, lname from bio where pid="+str(id)
    result = c.execute(query)

    liste  = list()
    for i in result:
        liste.append(i)

    return liste

def searchID():

    c = db.connect()
    query = "select pid from person where pid="+str(id)
    result = c.execute(query)

    liste  = list()
    for i in result:
        liste.append(i)

    return liste



"""
def select(table, cols, const):
    liste = list()
    c = db.connect()
    query = "select "

    if(type(cols) == str):
        query += cols + " from " + table
    elif(type(cols) == list):
        for i in cols:
            query += i + " "
        query += "from " + table


    if(type(const) == dict):
        query += " where "
        for i in const:
            query += i + "=" + const[i]

    a = c.execute(query)

    for i in a:
        liste.append(i)
    c.close()
    return liste
"""
"""
def findAllDB(keyword):
    liste = list()
    c = db.connect()
    print(keyword)
    records = c.execute(text("SELECT * from search_columns(\'"+keyword+"\')").execution_options(autocommit=True))
    # records = c.execute('select * from search_columns(\'%s\')', id)
    # print(records)
    for i in records:
        liste.append([i[1], i[2]])

    # print(liste)
    c.close()
    return liste
"""


if __name__ == '__main__':
    db = db_connect()
    app.debug=True
    app.run()
        
        
