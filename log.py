import sys, os, datetime, time

czas=datetime.datetime.now()


def czas():
    return str(time.strftime("%H:%M"))

def data():
    return str(time.strftime("%d-%m-%Y"))

def zapis_dziennika_zdarzen(dane):
    plik = open('Desktop/Home/log.txt', 'a+')
    plik.write(czas() + ' ' + dane+'\n')
    plik.close()
    print (czas() + ' ' + dane)

def kasowanie_dziennika_zdarzen():
    plik = open('Desktop/Home/log.txt', 'w')
    plik.write(data() + "  " +czas()+'\nDziennik zdarzen:\n\n')
    plik.close()

def zapis_stuff(dane):
    plik = open('Desktop/Home/stuff.txt', 'a+')
    plik.write(czas() + ' ' + dane+'\n')
    plik.close()