try:
    import traceback, sqlite3, datetime, sys ,os
except ImportError:
    print "Blad importu"

#-------------------BAZA DANYCH--------- SQL ---------------------------------------
def addRecordSensorOutdoorTemp (temp,wilg,wiatr,kierunek):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO tempzewnetrzna values(datetime('now','localtime'),?,?,?,?)",[temp,wilg,wiatr,kierunek])
    conn.commit()
    conn.close()

def addRecordSensorOutdoorLight (lux1,ir1):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    try:
        curs.execute("INSERT INTO swiatlo values(datetime('now','localtime'),?,?)",[lux1,ir1])
        conn.commit()
    except sqlite3.IntegrityError:
        print("rekord istnieje")
    conn.close()

def dodajRekordTempPok (temp,wilg):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO temppokoju values(datetime('now','localtime'),?,?)",[temp,wilg])
    conn.commit()
    conn.close()

def dodajRekordTempSyp (temp,wilg):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO tempsypialni values(datetime('now','localtime'),?,?)",[temp,wilg])
    conn.commit()
    conn.close()

def dodajRekordKwiatek2(wilgotnosc,slonce,zasilanie,wilgotnosc_raw):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    try:
        curs.execute("INSERT INTO kwiatek2 values(datetime('now','localtime'),?,?,?,?)",[wilgotnosc,slonce,zasilanie,wilgotnosc_raw])
        conn.commit()
    except sqlite3.IntegrityError:
        print("rekord istnieje")
    conn.close()

def dodajRekordKwiatek3(wilgotnosc,slonce,zasilanie,wilgotnosc_raw):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    try:
        curs.execute("INSERT INTO kwiatek3 values(datetime('now','localtime'),?,?,?,?)",[wilgotnosc,slonce,zasilanie,wilgotnosc_raw])
        conn.commit()
    except sqlite3.IntegrityError:
        print("rekord istnieje")
    conn.close()

def dodajRekordKwiatek4(wilgotnosc,slonce,zasilanie,wilgotnosc_raw):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    try:
        curs.execute("INSERT INTO kwiatek4 values(datetime('now','localtime'),?,?,?,?)",[wilgotnosc,slonce,zasilanie,wilgotnosc_raw])
        conn.commit()
    except sqlite3.IntegrityError:
        print("rekord istnieje")
    conn.close()

def dodajRekordKwiatek5(wilgotnosc,slonce,zasilanie,wilgotnosc_raw):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    try:
        curs.execute("INSERT INTO kwiatek5 values(datetime('now','localtime'),?,?,?,?)",[wilgotnosc,slonce,zasilanie,wilgotnosc_raw])
        conn.commit()
    except sqlite3.IntegrityError:
        print("rekord istnieje")
    conn.close()

def dodajRekordKwiatek6(wilgotnosc,slonce,zasilanie,wilgotnosc_raw):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    try:
        curs.execute("INSERT INTO kwiatek6 values(datetime('now','localtime'),?,?,?,?)",[wilgotnosc,slonce,zasilanie,wilgotnosc_raw])
        conn.commit()
    except sqlite3.IntegrityError:
        print("rekord istnieje")
    conn.close()

def dodajRekordKwiatek(wilgotnosc,slonce,woda,zasilanie):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO kwiatek values(datetime('now','localtime'),?,?,?,?,0)",[wilgotnosc,slonce,woda,zasilanie])
    conn.commit()
    conn.close()

def dodajRekordKwiatekPodlanie():
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO kwiatekpodlewanie values(datetime('now','localtime'))")
    conn.commit()
    conn.close()

def dodajRekordTerrarium(temp1,wilg1,temp2,wilg2,uvi):
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO terrarium values(datetime('now','localtime'),?,?,?,?,?)",[temp1,wilg1,temp2,wilg2,uvi])
    conn.commit()
    conn.close()

def kasujstaredane():
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("DELETE FROM temppokoju WHERE timestamp<datetime('now','-3 month')")
    curs.execute("DELETE FROM tempsypialni WHERE timestamp<datetime('now','-3 month')")
    curs.execute("DELETE FROM tempzewnetrzna WHERE timestamp<datetime('now','-3 month')")
    curs.execute("DELETE FROM kwiatek WHERE timestamp<datetime('now','-3 month')")
    conn.close()


def dodajTabele():
    conn=sqlite3.connect('/var/www/html/home_database.db')
    curs=conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS kwiatek6 (timestamp DATETIME PRIMARY KEY, wilgotnosc INTEGER,slonce INTEGER,zasilanie INTEGER,wilgotnosc_raw INTEGER);")
    conn.commit()
    conn.close()