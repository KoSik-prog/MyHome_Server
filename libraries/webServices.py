
#jakas zmiana


def transmisja(messag, adres):
    if(messag.find('salonOswietlenie.') != -1):   # SALON
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz:pocz+3])
        if(chJasnosc>=0 and chJasnosc<=100):
            sterowanieOswietleniem(lampaPok1Tradfri.Adres, str(chJasnosc))
        else:
            dziennik.zapis_dziennika_zdarzen("Blad danych! -> {}".format(chJasnosc))
    if(messag.find('tradfriLampaJasn.') != -1):   # LAMPA W SALONIE
        pocz=messag.find(".")+1
        chJasnosc=int(messag[pocz:pocz+3])
        if(chJasnosc>=0 and chJasnosc<=100):
            sterowanieOswietleniem(lampaDuzaTradfri.Adres, str(chJasnosc))
        else:
            dziennik.zapis_dziennika_zdarzen("Blad danych! -> {}".format(chJasnosc))
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
            dziennik.zapis_dziennika_zdarzen("Wyslano dane UDP")
        except:
            dziennik.zapis_dziennika_zdarzen("Blad danych dla UDP")
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
        terrarium.wilgDN=float(messag[(pocz+2):(pocz+5)])
        pocz=messag.find(",t:")+1
        terrarium.tempDN=float(messag[(pocz+2):(pocz+6)])
        pocz=messag.find("/w:")+1
        terrarium.wilg2=float(messag[(pocz+2):(pocz+5)])
        pocz=messag.find("/I:")+1
        terrarium.UVI=float(messag[(pocz+2):(pocz+11)])
        dziennik.zapis_dziennika_zdarzen("   Terrarium tempUP: {}*C, wilgDN: {}%  /  tempDN: {}*C, Wilg2: {}*C  /  UVI: {}".format(terrarium.tempUP,terrarium.wilgDN,terrarium.tempDN,terrarium.wilg2,terrarium.UVI))
        sql.addRecordTerrarium(terrarium.tempUP,terrarium.wilgDN,terrarium.tempDN,terrarium.wilg2,terrarium.UVI)
    if(messag.find('ko2') != -1):
        wiad="#05L" + messag[3:15]
        dziennik.zapis_dziennika_zdarzen(wiad)
        NRFwyslij(1,wiad).start()
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('gra') != -1):
        wiad="#05G" + messag[3:6]
        dziennik.zapis_dziennika_zdarzen(wiad)
        NRFwyslij(1,wiad).start()
        lampaTV.FlagaSterowanieManualne=True
    if(messag.find('lelw')): # LAMPA LED BIALY
        wiad="#06W" + messag[4:7]
        NRFwyslij(3,wiad).start()
    if(messag.find('pok1max') != -1):
        wiad="#05K255255255255"
        lampaTV.Ustawienie="255255255"
        lampaTV.Jasnosc=255
        dziennik.zapis_dziennika_zdarzen(wiad)
        dziennik.zapis_dziennika_zdarzen(wiad)
        NRFwyslij(1,wiad).start()
        ikea.ikea_dim_group(hubip, user_id, securityid, security_user, tradfriDev.salon, 100)
        lampaTV.FlagaSterowanieManualne=True
        dziennik.zapis_dziennika_zdarzen("Tryb swiatel: Pokoj 1 max")
    if(messag.find('budaTryb.') != -1):
        pocz=messag.find(".")+1
        wiad="#15T" + messag[pocz]
        NRFwyslij(12,wiad).start()
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
        ustawSwiatloZeZwloka(lampaPok1Tradfri.Adres, 0, 30).start()
        #ustawSwiatloZeZwloka(lampaPrzedpokojTradfri.Adres, 0, 31).start()
        #ustawSwiatloZeZwloka(dekoFlaming.Adres, 0, 30*60).start()
        dekoFlaming.FlagaSterowanieManualne=True
        dziennik.zapis_dziennika_zdarzen("Tryb swiatel: spij")
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
        dziennik.zapis_dziennika_zdarzen("Tryb swiatel: romantyczny  --> "+wiad)