from flask import Flask
from flask import render_template, request
from sqlalchemy import *
from sqlalchemy.engine.url import URL
import setting
app = Flask(__name__)

db = None
KEYWORD = ""

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
    KEYWORD = keyword

    # print("id: %s", id)
    l = list()

    res = searchInBio(keyword)
    for i in res:
        l.append(i[0])

    namelist = list()
    for i in l:
        namelist.append(searchByID(i))

    return render_template('/result.html', key=keyword, data=namelist)


@app.route('/result2', methods=['POST'])
def result2():

    keyword = KEYWORD
    filter = request.form.getlist('filter')
    print(filter)


    # print("id: %s", id)
    l = list()

    res = searchInBio(keyword)
    for i in res:
        l.append(i[0])

    namelist = list()
    for i in l:
        namelist.append(searchByID(i))


    return render_template('/result.html', key=keyword, data=namelist)

def searchByID(id):
    c = db.connect()
    liste = list()

    query = "select fname, lname from bio where pid=\'"+str(id)+"\'"
    res = c.execute(query)

    if(res):
        for i in res:
             return i


    return list("None", "None")


def db_connect():
    return create_engine(URL(**setting.DATABASE))

def findAll(keyword):

    tables = ["bio", "contact", "contribute", "interested_in",
                "person", "project", "publication",
                "published", "research", "work"]

    searchInBio(keyword)

    c = db.connect()

def searchInBio(keyword):
    columns = ["fname", "lname", "title", "bplace", "education"]
    c = db.connect()
    liste = list()

    for col in columns:
        query = "select pid from bio where "+col+"=\'"+keyword+"\'"
        res = c.execute(query)
        f = res.fetchall()
        if(f):
            for i in f:
                liste.append(i)

    return liste


if __name__ == '__main__':
    db = db_connect()
    app.debug=True
    app.run()



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

