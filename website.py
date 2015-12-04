from flask import Flask
from flask import render_template, request
from sqlalchemy import *
from sqlalchemy.engine.url import URL
import setting
import main
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


@app.route('/add_person', methods=['POST'])
def add_person():

    result=""
    try:
        keyword = request.form['x']
    except Exception as e:
        print(e)
        pass

    try:
        result = main.mainStart(keyword)
    except Exception as e:
        print(e)

    return render_template('/profile.html', data=result)


@app.route('/result', methods=['POST'])
def result():
    global KEYWORD
    keyword = ""
    filter=""

    try:
        keyword = request.form['x'].lower()
    except Exception as e:
        print(e)
        pass

    if(keyword):
        KEYWORD = keyword
    else:
        keyword = KEYWORD


    try:
        filter = request.form.getlist('filter')
    except Exception as e:
        print(e)
        pass

    l = list()

    if(filter):
        if("kisiler" in filter):
            res = searchInBio(keyword)
            for i in res:
                l.append(i[0])

        if("universite" in filter):
            res = searchInUni(keyword)
            for i in res:
                l.append(i[0])

        if("bolum" in filter):
            res = searchInDept(keyword)
            for i in res:
                l.append(i[0])

        if("ilgialani" in filter):
            res = searchInInterest(keyword)
            for i in res:
                l.append(i[0])
    else:
        res = searchInBio(keyword)
        for i in res:
            if(not i[0] in l):
                l.append(i[0])

        res = searchInUni(keyword)
        for i in res:
            if(not i[0] in l):
                l.append(i[0])

        res = searchInDept(keyword)
        for i in res:
            if(not i[0] in l):
                l.append(i[0])

        res = searchInInterest(keyword)
        for i in res:
            if(not i[0] in l):
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


def searchInBio(keyword):
    columns = ["fname", "lname", "title", "bplace", "education"]
    c = db.connect()
    liste = list()

    for col in columns:
        query = "select pid from bio where "+col+" ilike \'"+keyword+"\'"
        res = c.execute(query)
        f = res.fetchall()
        if(f):
            for i in f:
                liste.append(i)

    return liste

def searchInUni(keyword):
    c = db.connect()
    query = "select pid from work where university"+" ilike \'"+keyword+"\'"
    res = c.execute(query)
    f = res.fetchall()

    return [i for i in f if f]


def searchInDept(keyword):
    c = db.connect()
    query = "select pid from work where dept"+" ilike \'"+keyword+"\'"
    res = c.execute(query)
    f = res.fetchall()

    return [i for i in f if f]


def searchInInterest(keyword):
    c = db.connect()
    query = "select pid from interested_in where interest"+" ilike \'"+keyword+"\'"
    res = c.execute(query)
    f = res.fetchall()

    return [i for i in f if f]



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
