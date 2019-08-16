import sqlite3

con = sqlite3.connect("ppomList.db")
cursor = con.cursor()

#ppomList 테이블이 존재하면 DROP 에서 오류
cursor.execute("DROP TABLE ppomList")
cursor.execute("CREATE TABLE ppomList(number text UNIQUE, title text, url text, sendYn text, date text)")
#cursor.execute("INSERT INTO ppomList VALUES('1', '해피머니 25%할인!!!으아아달려으아아', 'urlurlurlurl', 'N', '2019815')")
# cursor.execute("INSERT INTO ppomList VALUES(2, 'RuRi', 'Toronto')")
# cursor.execute("INSERT INTO ppomList VALUES(3, 'Ruo', 'alberta')")

con.commit()

cursor.execute("SELECT * FROM ppomList")

# for row in cursor:
#      print( "%s 의 주소는 %s 입니다." % (row[1], row[2]) )

con.close()