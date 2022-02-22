import logging
import sys
import pymysql

host = ""
database ="test"
username =""
password =""
port = 1234

def main():

    conn = pymysql.connect(host=host, user=username,password=password,db=database,port= port, charset='utf8')
    cursor = conn.cursor()

    query ="INSERT INTO tt (name, number) value ('james', '45678')"
    cursor.execute(query)
    conn.commit()

    conn.close()

if __name__ == '__main__':
    main()