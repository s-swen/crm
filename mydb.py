#mydb.py
import MySQLdb

db = MySQLdb.connect(
    host='127.0.0.1', # localhost sometimes triggers socket mode, 127 always forces tcp
    user='root',
    passwd='password',
    port=3306,
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE elderco")

print('All Done!')