 # -*- coding: utf-8 -*-
try:
    import select, time, socket, traceback, sqlite3, smbus, datetime, random, threading, sys ,os, linecache, re, glob
except ImportError:
    print "Blad importu"

from libraries.log import *
time.sleep(.01)
from libraries.gui import *
from devicesList import *
from libraries.infoStrip import *
from libraries.weatherForecast import *
from libraries.ikea import *
from libraries.sqlDatabase import *
from libraries.nrf_connect import *

from time import sleep
import rpi_backlight as bl
import RPi.GPIO as GPIO
import xml.etree.cElementTree as ET

from numpy.random import randint

AddrOut = 2222
kasowanieSQL_flaga=False

#+++++ZWLOKA CZASOWA +++++++++++++++++++
time.sleep(5)

swiatlo=0
flaga_odczyt_ustawien=False


def sprawdzCzujniki():
    minimalneNapiecieBaterii=2.55
    minimalnaWilgotnosc = 10
    if((datetime.datetime.now() - czujnikZew.czas)>(datetime.timedelta(minutes=18))):
        infoStrip.set_error(0,True)
    if((datetime.datetime.now() - czujnikPok1.czas)>(datetime.timedelta(minutes=23))):
        infoStrip.set_error(1,True)
    if((datetime.datetime.now() - czujnikPok2.czas)>(datetime.timedelta(minutes=23))):
        infoStrip.set_error(2,True)
    if((datetime.datetime.now() - czujnikKwiatek.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(3,True)
    if((datetime.datetime.now() - czujnikKwiatek2.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(4,True)
    if((datetime.datetime.now() - czujnikKwiatek3.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(5,True)
    if((datetime.datetime.now() - czujnikKwiatek4.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(6,True)
    if((datetime.datetime.now() - czujnikKwiatek5.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(16,True)
    if((datetime.datetime.now() - czujnikKwiatek6.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(19,True)
    #sprawdzenie budy
    if((datetime.datetime.now() - buda.czas)>(datetime.timedelta(minutes=2))):
        buda.temp1=0.0
        buda.temp2=0.0
        buda.temp3=0.0
        buda.czujnikZajetosciFlaga=0
        buda.czujnikZajetosciRaw=0
    #sprawdzenie stanu baterii
    if(czujnikKwiatek.zasilanie <= 5):
        infoStrip.set_error(7,True)
    else:
        infoStrip.set_error(7,False)
    if(czujnikKwiatek2.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(8,True)
    else:
        infoStrip.set_error(8,False)
    if(czujnikKwiatek3.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(9,True)
    else:
        infoStrip.set_error(9,False)
    if(czujnikKwiatek4.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(10,True)
    else:
        infoStrip.set_error(10,False)
    if(czujnikKwiatek2.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek2.slonce < 60):
        infoStrip.set_error(11,True)
    else:
        infoStrip.set_error(11,False)
    if(czujnikKwiatek3.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek3.slonce < 60):
        infoStrip.set_error(12,True)
    else:
        infoStrip.set_error(12,False)
    if(czujnikKwiatek4.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek4.slonce < 60):
        infoStrip.set_error(13,True)
    else:
        infoStrip.set_error(13,False)
    if(czujnikKwiatek5.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(14,True)
    else:
        infoStrip.set_error(14,False)
    if(czujnikKwiatek5.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek5.slonce < 60):
        infoStrip.set_error(15,True)
    else:
        infoStrip.set_error(15,False)
    if(czujnikKwiatek6.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(17,True)
    else:
        infoStrip.set_error(17,False)
    if(czujnikKwiatek6.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek6.slonce < 60):
        infoStrip.set_error(18,True)
    else:
        infoStrip.set_error(18,False)




def sprawdzTimer():  #SPRAWDZENIE CO WYKONAC O DANEJ PORZE
    #----------------------SPRAWDZENIE BAZY DANYCH SQL-----------------------kasowanie starych rekordow------------
    if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:00") and kasowanieSQL_flaga==False:
        sql.delete_records(30) #kasowanie starych rekordow z bazy danych
        kasowanieSQL_flaga=True
        log.add_log("Skasowano stare dane z SQL")
    if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:01") and kasowanieSQL_flaga==True:
        kasowanieSQL_flaga=False
    #------------------------------------------------------------------------------------------
    autoCzas(lampaTV)
    autoCzas(dekoPok1)
    autoCzas(deko2Pok1)
    #autoCzas(dekoFlaming)
    autoCzas(lampaPok2Tradfri)
    autoCzas(lampaPok2)#---- LED SYPIALNI
    #autoCzas(lampaKuch)#-----LED KUCHNI
    #autoCzas(dekoUsb)#----USB Stick
    autoCzas(hydroponika)#----Hydroponika


def autoCzas(klasa):
    format = '%H:%M:%S.%f'
    aktual=datetime.datetime.now().time()
    try:
        zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(klasa.AutoON, format) # obliczenie roznicy czasu
    except ValueError as e:
        print('Blad czasu wł:', e)
    try:
        zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(klasa.AutoOFF, format) # obliczenie roznicy czasu
    except ValueError as e:
        print('Blad czasu wył:', e)
    #-----skasowanie flag ----------
    if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  klasa.FlagaSterowanieManualne==True):
        klasa.FlagaSterowanieManualne=False
    if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and klasa.FlagaSterowanieManualne==True):
        klasa.FlagaSterowanieManualne=False
    #------SPRAWDZENIE------------------------
    if(klasa.Flaga==0 and automatykaOswietlenia.swiatloObliczone<klasa.AutoLux_min and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
        log.add_log("AUTO {} -> ON".format(klasa.Opis))
        sterowanieOswietleniem(klasa.Adres,klasa.AutoJasnosc)
        time.sleep(20)
    if(klasa.Flaga==1 and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
        log.add_log("AUTO {} -> OFF".format(klasa.Opis))
        sterowanieOswietleniem(klasa.Adres,0)
        time.sleep(20)
#------------------UDP-----------------------------------
def server():
    try:
        message, address = s.recvfrom(1024)
        log.add_log(log.actualDate() +" " + "Polaczenie %s: %s" % (address, message))
        transmisja(message, address)
        return message
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()


def transmisja(messag, adres):
    if(messag.find('salonOswietlenie.') != -1):   # SALON
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz:pocz+3])
        if(chJasnosc>=0 and chJasnosc<=100):
            sterowanieOswietleniem(lampaPok1Tradfri.Adres, str(chJasnosc))
        else:
            log.add_log("Blad danych! -> {}".format(chJasnosc))
    if(messag.find('tradfriLampaJasn.') != -1):   # LAMPA W SALONIE
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz:pocz+3])
        if(chJasnosc>=0 and chJasnosc<=100):
            sterowanieOswietleniem(lampaDuzaTradfri.Adres, str(chJasnosc))
        else:
            log.add_log("Blad danych! -> {}".format(chJasnosc))
    if(messag.find('tradfriLampaKol.') != -1):   # LAMPA W SALONIE
        pocz=messag.find(".")+1
        sterowanieOswietleniem(lampaDuzaTradfri.Adres, messag[pocz:pocz+9])
    if(messag.find('swiatloSypialni.') != -1):   # SYPIALNIA
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz:pocz+3])
        lampaPok2.Jasnosc=chJasnosc
        sterowanieOswietleniem(lampaPok2Tradfri.Adres,lampaPok2.Jasnosc)
        sterowanieOswietleniem(lampaPok2.Adres,lampaPok2.Jasnosc)
        lampaPok2.FlagaSterowanieManualne=True
        dekoFlaming.FlagaSterowanieManualne=True
        sterowanieOswietleniem(dekoFlaming.Adres,messag[pocz])
    if(messag.find('swiatloSypialniTradfri.') != -1):   # SYPIALNIA TRADFRI
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz])
        sterowanieOswietleniem(lampaPok2Tradfri.Adres,chJasnosc)
    if(messag.find('swiatloJadalniTradfri.') != -1):   # Jadalnia TRADFRI
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz])
        sterowanieOswietleniem(lampaJadalniaTradfri.Adres,chJasnosc)
    if(messag.find('swiatlokuchni.') != -1):  # KUCHNIA
        pocz=messag.find(".")+1
        sterowanieOswietleniem(AdresKuchnia,messag[pocz])
        lampaKuch.FlagaSterowanieManualne=True
    if(messag.find('swiatloPrzedpokoj.') != -1):  # PRZEDPOKOJ
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz:len(messag)])
        sterowanieOswietleniem(lampaPrzedpokojTradfri.Adres,chJasnosc)
    if(messag.find('reflektor1.') != -1): # REFLEKTOR LED COLOR
        lampa1Pok1.Ustawienie=messag[11:23]
        lampa1Pok1.Jasnosc=messag[23:26]
        sterowanieOswietleniem(AdresLampa1,lampa1Pok1.Jasnosc)
    if(messag.find('reflektor1kolor.') != -1): # REFLEKTOR LED COLOR KOLOR
        lampa1Pok1.Ustawienie=messag[16:28]
        sterowanieOswietleniem(lampa1Pok1.Adres,lampa1Pok1.Jasnosc)
    if(messag.find('reflektor1jasn.') != -1): # REFLEKTOR LED COLOR JASNOSC
        lampa1Pok1.Jasnosc=messag[15:18]
        sterowanieOswietleniem(lampa1Pok1.Adres,lampa1Pok1.Jasnosc)
    if(messag.find('dekoracjePok1.') != -1): # DEKORACJE POKOJ 1
        pocz=messag.find(".")+1
        sterowanieOswietleniem(dekoPok1.Adres,messag[pocz])
        dekoPok1.FlagaSterowanieManualne=True
        sterowanieOswietleniem(deko2Pok1.Adres,messag[pocz])
    if(messag.find('dekoracjePok2.') != -1): # DEKORACJE POKOJ 2
        pocz=messag.find(".")+1
        dekoFlaming.FlagaSterowanieManualne=True
        sterowanieOswietleniem(dekoFlaming.Adres,messag[pocz])
    if(messag.find('dekoracjeUSB.') != -1): # uniwersalny modul USB
        pocz=messag.find(".")+1
        dekoUsb.FlagaSterowanieManualne=True
        sterowanieOswietleniem(dekoUsb.Adres,messag[pocz])
    if(messag.find('hydroponika.') != -1): # Hydroponika
        pocz=messag.find(".")+1
        dekoUsb.FlagaSterowanieManualne=True
        sterowanieOswietleniem(AdresHydroponika,messag[pocz])
    if(messag=='?m'):
        try:
            s.sendto('temz{:04.1f}wilz{:04.1f}tem1{:04.1f}wil1{:04.1f}tem2{:04.1f}wil2{:04.1f}'.format(czujnikZew.temp,czujnikZew.humi,czujnikPok1.temp,czujnikPok1.humi,czujnikPok2.temp,czujnikPok2.humi)+'wilk{:03d}slok{:03d}wodk{:03d}zask{:03d}'.format(int(czujnikKwiatek.wilgotnosc),int(czujnikKwiatek.slonce),int(czujnikKwiatek.woda),int(czujnikKwiatek.zasilanie))+'letv{}{}{}'.format(int(lampaTV.Flaga),lampaTV.Ustawienie,lampaTV.Jasnosc)+'lesy{}{:03d}'.format(int(lampaPok2.Flaga),lampaPok2.Jasnosc)+'lela{}{:03d}'.format(int(lampa1Pok1.Flaga),lampa1Pok1.Jasnosc), adres)
            log.add_log("Wyslano dane UDP")
        except:
            log.add_log("Blad danych dla UDP")
    if(messag.find('sterTV.') != -1):
        pocz=messag.find(".")+1
        if int(messag[(pocz+9):(pocz+12)])>=0:
            lampaTV.Ustawienie=messag[(pocz):(pocz+9)]
            lampaTV.Jasnosc=int(messag[(pocz+9):(pocz+12)])
        sterowanieOswietleniem(AdresLedTV,lampaTV.Jasnosc)
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('sterTVjasnosc.') != -1):
        zmien=messag[14:17]
        if int(zmien)>0:
            lampaTV.Jasnosc=int(zmien)
        sterowanieOswietleniem(AdresLedTV,zmien)
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('terrarium.') != -1):
        pocz=messag.find(".T:")+1
        terrarium.tempUP=float(messag[(pocz+2):(pocz+6)])
        pocz=messag.find("/W:")+1
        terrarium.wilgUP=float(messag[(pocz+2):(pocz+5)])
        pocz=messag.find(",t:")+1
        terrarium.tempDN=float(messag[(pocz+2):(pocz+6)])
        pocz=messag.find("/w:")+1
        terrarium.wilgDN=float(messag[(pocz+2):(pocz+5)])
        pocz=messag.find("/I:")+1
        terrarium.UVI=float(messag[(pocz+2):(pocz+11)])
        log.add_log("   Terrarium TempUP: {}*C, WilgUP: {}%  /  TempDN: {}*C, WilgDN: {}*C  /  UVI: {}".format(terrarium.tempUP,terrarium.wilgUP,terrarium.tempDN,terrarium.wilgDN,terrarium.UVI))
        sql.addRecordTerrarium(terrarium.tempUP,terrarium.wilgUP,terrarium.tempDN,terrarium.wilgDN,terrarium.UVI)
    if(messag.find('ko2') != -1):
        wiad="#05L" + messag[3:15]
        log.add_log(wiad)
        nrf.NRFwyslij(1,wiad)
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('gra') != -1):
        wiad="#05G" + messag[3:6]
        log.add_log(wiad)
        nrf.NRFwyslij(1,wiad)
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('lelw')): # LAMPA LED BIALY
        wiad="#06W" + messag[4:7]
        nrf.NRFwyslij(3,wiad)
    if(messag.find('pok1max') != -1):
        wiad="#05K255255255255"
        lampaTV.Ustawienie="255255255"
        lampaTV.Jasnosc=255
        log.add_log(wiad)
        log.add_log(wiad)
        nrf.NRFwyslij(1,wiad)
        ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, tradfriDev.salon, 100)
        lampaTV.FlagaSterowanieManualne=True
        log.add_log("Tryb swiatel: Pokoj 1 max")
    if(messag.find('budaTryb.') != -1):
        pocz=messag.find(".")+1
        wiad="#15T" + messag[pocz]
        nrf.NRFwyslij(12,wiad)
        sterowanieOswietleniem(AdresLedTV,lampaTV.Jasnosc)
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('spij') != -1):
        sterowanieOswietleniem(AdresLedTV,"000")
        lampaTV.FlagaSterowanieManualne=True
        sterowanieOswietleniem(lampaPok1Tradfri.Adres,0)
        sterowanieOswietleniem(lampaPok1Tradfri.Zarowka,15)
        #sterowanieOswietleniem(lampaJadalniaTradfri.Adres,0)
        #sterowanieOswietleniem(lampaPrzedpokojTradfri.Adres,100)
        sterowanieOswietleniem(lampaDuzaTradfri.Adres,0)
        sterowanieOswietleniem(dekoPok1.Adres,0)
        sterowanieOswietleniem(deko2Pok1.Adres,0)
        #sterowanieOswietleniem(lampa1Pok1.Adres,0)
        dekoPok1.FlagaSterowanieManualne=True
        deko2Pok1.FlagaSterowanieManualne=True
        deko2Pok1.FlagaSterowanieManualne=True
        ustawSwiatloZeZwloka(lampaPok1Tradfri.Adres, 0, 30)
        #ustawSwiatloZeZwloka(lampaPrzedpokojTradfri.Adres, 0, 31).start()
        #ustawSwiatloZeZwloka(dekoFlaming.Adres, 0, 30*60).start()
        dekoFlaming.FlagaSterowanieManualne=True
        log.add_log("Tryb swiatel: spij")
    if(messag.find('romantyczny') != -1):
        if(random.randint(0, 1)==1):
            lampaTV.Ustawienie="255000{:03d}".format(random.randint(20, 120))
        else:
            lampaTV.Ustawienie="255{:03d}000".format(random.randint(20, 120))
        sterowanieOswietleniem(lampaTV.Adres,lampaTV.Ustawienie)
        if(random.randint(0, 1)==1):
            kolor="255000{:03d}".format(random.randint(20, 150))
        else:
            kolor="255{:03d}000".format(random.randint(20, 150))
        sterowanieOswietleniem(lampaDuzaTradfri.Adres,kolor)
        sterowanieOswietleniem(lampaDuzaTradfri.Adres, 100)
        if(random.randint(0, 1)==1):
            lampa1Pok1.Ustawienie="255000{:03d}000".format(random.randint(20, 120))
        else:
            lampa1Pok1.Ustawienie="255{:03d}000000".format(random.randint(20, 120))
        sterowanieOswietleniem(lampa1Pok1.Adres, 255)
        sterowanieOswietleniem(lampaPok1Tradfri.Adres, 0)
        lampaTV.FlagaSterowanieManualne=True
        sterowanieOswietleniem(dekoPok1.Adres,0)
        dekoPok1.FlagaSterowanieManualne=True
        sterowanieOswietleniem(deko2Pok1.Adres,1)
        deko2Pok1.FlagaSterowanieManualne=True
        log.add_log("Tryb swiatel: romantyczny  --> "+wiad)


class ustawSwiatloZeZwloka(threading.Thread): #------WATEK NADAWANIA NRF
    def __init__(self, adres, jasnosc, czas):
        threading.Thread.__init__(self)
        self.adres = adres
        self.jasnosc = jasnosc
        self.czas = czas
    def run(self):
        time.sleep(self.czas)
        if self.jasnosc==0:
            sterowanieOswietleniem(self.adres,100)
        sterowanieOswietleniem(self.adres,self.jasnosc)
        log.add_log("Funkacja spij wlaczona")

def sterowanieOswietleniem(adres, ustawienie):
    if adres==lampaTV.Adres:   #TV
        wiad="#05K{}{:03d}".format(lampaTV.Ustawienie,int(ustawienie))
        if len(wiad)>=15:
            log.add_log("Ustawiono Led TV: {}".format(wiad))
            infoStrip.add_info("światło TV: {}".format(ustawienie))
            nrf.NRFwyslij(AdresLedTV,wiad)
            lampaTV.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaPok2.Adres:  #SYPIALNIA
        wiad="#S{:03d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Led Sypialni: {}".format(wiad))
            infoStrip.add_info("światło w sypialni: {}".format(ustawienie))
            nrf.NRFwyslij(AdresSypialnia,wiad)
            lampaPok2.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaKuch.Adres:  #KUCHNIA
        wiad="#07T{:01d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Led Kuchni: {}".format(wiad))
            infoStrip.add_info("światło w kuchni: {}".format(ustawienie))
            nrf.NRFwyslij(AdresKuchnia,wiad)
            lampaKuch.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampa1Pok1.Adres:  # LAMPA 1 w salonie
        wiad="#05K{}{:03d}".format(lampa1Pok1.Ustawienie, int(ustawienie))
        if len(wiad)>=5:
            lampa1Pok1.Jasnosc=int(ustawienie)
            log.add_log("Ustawiono Reflektor 1: {}".format(wiad))
            infoStrip.add_info("reflektor 1 w salonie: {}/{}".format(lampa1Pok1.Ustawienie,int(ustawienie)))
            nrf.NRFwyslij(AdresLampa1,wiad)
            lampa1Pok1.blad+=1
            if(int(ustawienie) == 0):
                lampa1Pok1.Flaga = 0
            else:
                lampa1Pok1.Flaga = 1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoPok1.Adres:  # dekoracje pok 1 / Reka
        wiad="#08T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Lampa 1: {}".format(wiad))
            infoStrip.add_info("dekoracje 1 w salonie: {}".format(ustawienie))
            nrf.NRFwyslij(dekoPok1.Adres,wiad).start()
            lampa1Pok1.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==deko2Pok1.Adres:  # dekoracje pok 1 / Eifla i inne
        wiad="#09T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Lampa 2: {}".format(wiad))
            infoStrip.add_info("dekoracje 2 w salonie: {}".format(ustawienie))
            nrf.NRFwyslij(deko2Pok1.Adres,wiad)
            dekoPok1.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoFlaming.Adres:  # FLAMING
        wiad="#10T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Lampa Flaming: {}".format(wiad))
            infoStrip.add_info("flaming: {}".format(ustawienie))
            nrf.NRFwyslij(AdresFlaming,wiad)
            dekoFlaming.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoUsb.Adres:  # Dekoracje - uniwersalny modul USB
        wiad="#11T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Uniwersalny USB: {}".format(wiad))
            infoStrip.add_info("uniwersalny USB: {}".format(ustawienie))
            nrf.NRFwyslij(AdresUsb,wiad)
            dekoUsb.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaPok1Tradfri.Adres:  # Tradfri Salon
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, adres, ustawienie)
        log.add_log("Tradfri Salon ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w salonie: {}".format(ustawienie))
    if adres==lampaPok1Tradfri.Zarowka:  # Tradfri Salon Zarowka
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        log.add_log("Tradfri Salon-Zarowka ->: {}".format(ustawienie))
    if adres==lampaJadalniaTradfri.Adres:  # Tradfri Jadalnia
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        log.add_log("Tradfri Jadalnia ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w jadalni: {}".format(ustawienie))
    if adres==lampaPrzedpokojTradfri.Adres:  # Tradfri przedpokoj
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        if(ustawienie>0):
            lampaPrzedpokojTradfri.Status=1
        else:
            lampaPrzedpokojTradfri.Status=0
        log.add_log("Tradfri Przedpokoj ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w przedpokoju: {}".format(ustawienie))
    if adres==lampaDuzaTradfri.Adres:  # Tradfri Lampa Duza
        if len(str(ustawienie))==1:
            if int(ustawienie)==0 or int(ustawienie)==1:
                ikea.ikea_power_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, int(ustawienie))
                log.add_log("Tradfri Lampa ON/OFF ->: {}".format(ustawienie))
        elif len(str(ustawienie))==9:
            chKolor1=int(ustawienie[0:3])
            chKolor2=int(ustawienie[3:6])
            chKolor3=int(ustawienie[6:9])
            ikea.ikea_RGB_lamp(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaDuzaTradfri.Adres, chKolor1, chKolor2, chKolor3)
            log.add_log("Tradfri Lampa kolor ->: {}".format(ustawienie))
            infoStrip.add_info("lampa w salonie -> kolor: {}".format(ustawienie))
        elif len(str(ustawienie))==2 or len(str(ustawienie))==3:
            if int(ustawienie)>1 and int(ustawienie)<=100:
                ikea.ikea_dim_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, int(ustawienie))
                log.add_log("Tradfri Lampa Jasnosc ->: {}".format(ustawienie))
                infoStrip.add_info("lampa w salonie: {}".format(ustawienie))
        else:
            log.add_log("Tradfri blad skladni")
    if adres==lampaPok2Tradfri.Adres:  # Tradfri Sypialnia
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.Adres, ustawienie)
            lampaPok2Tradfri.Flaga = False
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.Adres, ustawienie)
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.Adres, 1)
            lampaPok2Tradfri.Flaga = True
        log.add_log("Tradfri Sypialnia ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w sypialni: {}".format(ustawienie))
    if adres==hydroponika.Adres:   #Hydroponika
        if int(ustawienie) > 1:
            wiad="#17P1" #wlacz pompe
        else:
            wiad="#17A{:01d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Hydroponike: {}".format(wiad))
            infoStrip.add_info("Hydroponika: {}".format(ustawienie))
            nrf.NRFwyslij(hydroponika.Adres,wiad).start()
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))



def zapis_danych_xml():
    root = ET.Element("data")

    ET.SubElement(root, "czujnikZewtemp").text = str(czujnikZew.temp)
    ET.SubElement(root, "czujnikZewhumi").text = str(czujnikZew.humi)
    ET.SubElement(root, "czujnikZewlux").text = str(czujnikZew.lux)
    ET.SubElement(root, "czujnikZewbatt").text = str(czujnikZew.batt)
    ET.SubElement(root, "czujnikPok1temp").text = str(czujnikPok1.temp)
    ET.SubElement(root, "czujnikPok1humi").text = str(czujnikPok1.humi)
    ET.SubElement(root, "czujnikPok1batt").text = str(czujnikPok1.batt)
    ET.SubElement(root, "czujnikPok2temp").text = str(czujnikPok2.temp)
    ET.SubElement(root, "czujnikPok2humi").text = str(czujnikPok2.humi)

    ET.SubElement(root, "czujnikKwiatekSlonce").text = str(czujnikKwiatek.slonce)
    ET.SubElement(root, "czujnikKwiatekWilgotnosc").text = str(czujnikKwiatek.wilgotnosc)
    ET.SubElement(root, "czujnikKwiatekWoda").text = str(czujnikKwiatek.woda)
    ET.SubElement(root, "czujnikKwiatekZasilanie").text = str(czujnikKwiatek.zasilanie)

    ET.SubElement(root, "lampaTVFlaga").text = str(lampaTV.Flaga)
    ET.SubElement(root, "lampaTVUstawienie").text = str(lampaTV.Ustawienie)
    ET.SubElement(root, "lampaTVJasnosc").text = str(lampaTV.Jasnosc)

    ET.SubElement(root, "dekoracje1Flaga").text = str(dekoPok1.Flaga)
    ET.SubElement(root, "dekoracje2Flaga").text = str(deko2Pok1.Flaga)

    ET.SubElement(root, "dekoracjeUSB").text = str(dekoUsb.Flaga)

    ET.SubElement(root, "dekoracjeFlaming").text = str(dekoFlaming.Flaga)

    ET.SubElement(root, "lampaPrzedpokoj").text = str(lampaPrzedpokojTradfri.Status)

    ET.SubElement(root, "lampaKuchFlaga").text = str(lampaKuch.Flaga)

    ET.SubElement(root, "lampaPok2Flaga").text = str(lampaPok2.Flaga)
    ET.SubElement(root, "lampaPok2Jasnosc").text = str(lampaPok2.Jasnosc)

    ET.SubElement(root, "budaTemp1").text = str(buda.temp1)
    ET.SubElement(root, "budaTemp2").text = str(buda.temp2)
    ET.SubElement(root, "budaTemp3").text = str(buda.temp3)
    ET.SubElement(root, "budaCzujnikFlaga").text = str(buda.czujnikZajetosciFlaga)
    ET.SubElement(root, "budaCzujnikRaw").text = str(buda.czujnikZajetosciRaw)

    tree = ET.ElementTree(root)
    tree.write('/var/www/html/homevariables.xml')
    #log.add_log("Zapisano dane")

def zapis_ustawien_xml():
    setings = ET.Element("settings")

    ET.SubElement(setings, "lampaTVAutoLux_min").text = str(lampaTV.AutoLux_min)
    ET.SubElement(setings, "lampaTVAutoOff").text = str(lampaTV.AutoOFF)
    ET.SubElement(setings, "lampaTVAutoOn").text = str(lampaTV.AutoON)
    ET.SubElement(setings, "lampaTVJasnosc").text = str(lampaTV.Jasnosc)
    ET.SubElement(setings, "lampaTVUstawienie").text = str(lampaTV.Ustawienie)

    ET.SubElement(setings, "lampaKuchAutoLux_min").text = str(lampaKuch.AutoLux_min)
    ET.SubElement(setings, "lampaKuchAutoOFF").text = str(lampaKuch.AutoOFF)
    ET.SubElement(setings, "lampaKuchAutoON").text = str(lampaKuch.AutoON)

    ET.SubElement(setings, "lampa1Pok1Jasnosc").text = str(lampa1Pok1.Jasnosc)

    ET.SubElement(setings, "lampaPok2AutoJasnosc").text = str(lampaPok2.AutoJasnosc)
    ET.SubElement(setings, "lampaPok2AutoLux_min").text = str(lampaPok2.AutoLux_min)
    ET.SubElement(setings, "lampaPok2AutoOFF").text = str(lampaPok2.AutoOFF)
    ET.SubElement(setings, "lampaPok2AutoON").text = str(lampaPok2.AutoON)

    tree2 = ET.ElementTree(setings)
    tree2.write('/var/www/html/ustawienia.xml')
    log.add_log("Zapisano ustawienia")

def odczyt_ustawien_xml():
    tree = ET.ElementTree(file='/var/www/html/ustawienia.xml')
    root = tree.getroot()

    lampaTV.AutoLux_min = int(root.find('lampaTVAutoLux_min').text)
    lampaTV.AutoOff = root.find('lampaTVAutoOff').text
    lampaTV.AutoOn = root.find('lampaTVAutoOn').text
    lampaTV.Jasnosc = int(root.find('lampaTVJasnosc').text)
    lampaTV.Ustawienie = root.find('lampaTVUstawienie').text

    lampaKuch.AutoLux_min = int(root.find('lampaKuchAutoLux_min').text)
    lampaKuch.AutoOFF = root.find('lampaKuchAutoOFF').text
    lampaKuch.AutoON = root.find('lampaKuchAutoON').text

    lampa1Pok1.Jasnosc = int(root.find('lampa1Pok1Jasnosc').text)

    lampaPok2.AutoJasnosc = int(root.find('lampaPok2AutoJasnosc').text)
    lampaPok2.AutoLux_min = int(root.find('lampaPok2AutoLux_min').text)
    lampaPok2.AutoOFF = root.find('lampaPok2AutoOFF').text
    lampaPok2.AutoON = root.find('lampaPok2AutoON').text

def watchdog_reset():
    setings = ET.Element("settings")
    ET.SubElement(setings, "watchdogFlag").text = str(1)
    tree2 = ET.ElementTree(setings)
    tree2.write('Desktop/Home/watchdog.xml')

def czujnik_swiatla():
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
    bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
    ch0 = data[1] * 256 + data[0]
    return int(ch0)

def jasnosc_wyswietlacza(): #----STEROWANIE WYSWIETLACZEM - WATEK!!!!!!!!!! ----------------------------------------------------
    global swiatlo
    swiatlo_old=0
    while(1):
        swiatlo=czujnik_swiatla() #poprawic
        gui.swiatlo = swiatlo
        if swiatlo>(swiatlo_old+15) or swiatlo<(swiatlo_old-15): 
            if swiatlo<7:
                jasnoscwysw=11
            elif swiatlo>=7 and swiatlo<100:
                jasnoscwysw=int(((0.645*swiatlo)+5.4838)+11)
            elif swiatlo>=100 and swiatlo<1000:
                jasnoscwysw=int(((0.193*swiatlo) + 50.67)+11)
            elif swiatlo>=1000:
                jasnoscwysw=255
            bl.set_brightness(jasnoscwysw, smooth=True, duration=2)  # ustawienie jasnosci LCD
            #log.add_log("Jasnosc wyswietlacza:{}   / old:{}, new:{}".format(jasnoscwysw,swiatlo_old,swiatlo))
            swiatlo_old=swiatlo
        time.sleep(5)

#=====================================================
#Adresy  ==>>
AdresLedTV = 1
AdresSypialnia = 2
AdresLampa1 = 3
AdresKuchnia = 4
AdresLampa2 = 5 #Dekoracje 1 REKA
AdresLampa3 = 6 #Dekoracje 2 Eifla
AdresFlaming = 7 #Dekoracje Flaming
AdresUsb = 8 #Modul uniwersalny USB
AdresCzujnikKwiatka1 = 9
AdresCzujnikKwiatka2 = 10
AdresCzujnikKwiatka3 = 11
AdresBuda = 12
AdresCzujnikKwiatka4 = 13
AdresHydroponika = 15
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def ODCZYT_USTAWIEN_WATEK():  #------WATEK ODCZYTUJACY USTAWIENIA Z XML
    q=0
    while(1):
        if q>5:
            q=0
        if q==0:
            weather.get_forecast('Rodgau')
        odczyt_ustawien_xml()
        watchdog_reset()
        time.sleep(60)
        q=q+1

def SPRAWDZENIE_TIMERA_WATEK():  #------WATEK SPRAWDZAJACY TIMER
    while(1):
        sprawdzTimer()
        sprawdzCzujniki()
        time.sleep(10)

#++++++++++++++++++++++++++++++ funkcje dla watkow +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def LCD_thread_init():
    lcdTh = threading.Thread(target=gui.lcd)
    lcdTh.start()

def NRF_thread_init():
    nrfTh = threading.Thread(target=nrf.server)
    nrfTh.start()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
log.add_log("Uruchamiam serwer MyHome...")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)

#--------------UDP--------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', AddrOut))
s.setblocking(0)
ready=select.select([s],[],[],1)
#-------------WATKI--------------------------
LCD_thread_init()
NRF_thread_init()
l=threading.Thread(target=jasnosc_wyswietlacza)
l.start()
o=threading.Thread(target=ODCZYT_USTAWIEN_WATEK)
o.start()
ti=threading.Thread(target=SPRAWDZENIE_TIMERA_WATEK)
ti.start()
#--------------------------------------------
while(1):
    if ready[0]:
        server()
    ready=select.select([s],[],[],0.5)
    time.sleep(.01)
