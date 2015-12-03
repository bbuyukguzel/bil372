import random
from crawler import Crawler


# returns random n lines in URL list file
def test(n=5, sample=True):
    with open('URL.txt') as file:
        content = [line.rstrip('\n') for line in file]
    file.close()
    if sample:
        return random.sample(content, n)
    else:
        return content


if __name__ == '__main__':

    for url in test(5, sample=False):
        print(url)
        c = Crawler(url)
        print(c.run())
        

def add_database(url, fname, lname, uniname, rank, researchList, interestList, email, phone, fax, office_no, address,
                 projectList, pubList,
                 password='admin', host='localhost', dbname='bil372',
                 user='postgres'):
    conn_string = "host=" + host + " dbname=" + dbname + "user=" + user + " password=" + password
    conn = psycopg2.connect(conn_string)
    c = conn.cursor()
    c.execute(
        "TRUNCATE TABLE person, bio, contact, interested_in, project, published, research, work RESTART IDENTITY;")
    c.execute("SELECT * FROM person where website = \'" + url + "\'")
    result = c.fetchall()
    if len(result) == 0:
        print('Not found')
        c.execute("INSERT INTO person (website) VALUES (\'" + url + "\') RETURNING pid;")
        repid = c.fetchone()[0]
        query = "INSERT INTO bio (pid,fname,lname,title,bdate,bplace,education) VALUES (%s, %s, %s, 'tittle', '1.1.2015', 'bplace' ,'education');"
        data = (repid, fname, lname)
        c.execute(query, data)
        conn.commit()
        query = "INSERT INTO work (pid,university, dept) VALUES (%s, %s, %s);"
        data = (repid, uniname, rank)
        c.execute(query, data)
        conn.commit()
        counter = 1
        for research in researchList:
            query = "INSERT INTO research (researchid,pid,rname) VALUES (%s, %s, %s);"
            data = (counter, repid, research)
            c.execute(query, data)
            conn.commit()
            counter += 1
        counter = 1
        for interest in interestList:
            query = "INSERT INTO interested_in (interestid,pid,interest) VALUES (%s, %s, %s);"
            data = (counter, repid, interest)
            c.execute(query, data)
            conn.commit()
            counter += 1
        query = "INSERT INTO contact (pid,email,phone,fax,office_no,address) VALUES (%s, %s, %s, %s, %s,%s);"
        data = (repid, email, phone, fax, office_no, address)
        c.execute(query, data)
        conn.commit()
        counter = 1
        for project in projectList:
            query = "INSERT INTO project (projectid,pid,pname) VALUES (%s, %s, %s);"
            data = (counter, repid, project)
            c.execute(query, data)
            conn.commit()
            counter += 1
        query = "INSERT INTO contact (pid,email,phone,fax,office_no,address) VALUES (%s, %s, %s, %s, %s,%s);"
        data = (repid, email, phone, fax, office_no, address)
        c.execute(query, data)
        conn.commit()

            # parse substring pubList
            #
            # EDIT HERE
            #

        for pub in pubList:
            query = "INSERT INTO publication (pubid, pubname,url,ptype) VALUES (%s, %s, %s, %s);"
            data = (' ', ' ', ' ', ' ')
            c.execute(query, data)
            conn.commit()
            query = "INSERT INTO interested_in (pid,pubid,pdate) VALUES (%s, %s, %s);"
            data = (repid, counter, ' ')
            c.execute(query, data)
            conn.commit()
            #
            # EDIT HERE
            #
            
    else:
        print('USER FOUND !')
    conn.close()
