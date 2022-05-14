import datetime

class czujnikZewCl:   #CZUJNIK TEMPERATURY ZEWNETRZNEJ
    temp=1.1
    humi=1.1
    batt=1.1
    lux=0
    ir=0
    predkoscWiatru=0
    kierunekWiatru=0
    czas=datetime.datetime.now()
    blad=False
    noc_flaga=False
    noc_ustawienie=60  #ustawienie kiedy noc
    flaga_peirwszaPaczka=False
czujnikZew=czujnikZewCl

class czujnikPok1Cl:  #SALON
    temp=2.2
    humi=2.2
    batt=2.2
    czas=datetime.datetime.now()
    blad=False
    sqlRoom = 'pok1Temp'
czujnikPok1=czujnikPok1Cl

class czujnikPok2Cl:   #SYPIALNIA
    temp=3.3
    humi=3.3
    batt=3.3
    czas=datetime.datetime.now()
    blad=False
    sqlRoom = 'pok2Temp'
czujnikPok2=czujnikPok2Cl

class czujnikKwiatekCl:   #KWIATEK
    woda=0
    slonce=0
    wilgotnosc=100
    zasilanie=100
    czas=datetime.datetime.now()
    error = "blebleble"
czujnikKwiatek=czujnikKwiatekCl

class czujnikKwiatek2Cl:   #adres 12  KWIATEK _maly czujnik PALMA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=120.0
    wartoscMax=500.0
    czas=datetime.datetime.now()
    nazwa = "Palma"
czujnikKwiatek2=czujnikKwiatek2Cl

class czujnikKwiatek3Cl:   #adres 13  KWIATEK _maly czujnik PACHIRA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=380.0
    wartoscMax=500.0
    czas=datetime.datetime.now()
czujnikKwiatek3=czujnikKwiatek3Cl

class czujnikKwiatek4Cl:   #adres 14  KWIATEK _maly czujnik POKRZYWA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=280.0#250.0
    wartoscMax=580.0
    czas=datetime.datetime.now()
czujnikKwiatek4=czujnikKwiatek4Cl

class czujnikKwiatek5Cl:   #adres 16  KWIATEK _maly czujnik BENJAMIN
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=400.0
    wartoscMax=550.0
    czas=datetime.datetime.now()
czujnikKwiatek5=czujnikKwiatek5Cl

class czujnikKwiatek6Cl:   #adres 17  KWIATEK _maly czujnik  SZEFLERA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=260.0
    wartoscMax=500.0
    czas=datetime.datetime.now()
czujnikKwiatek6=czujnikKwiatek6Cl

class terrariumCl:   #TERRARIUM
    temp1=0.0
    wilg1=0.0
    temp2=0.0
    wilg2=0.0
    UVI=0.0
terrarium=terrariumCl

class budaCl:   #BUDA
    Adres=12
    temp1=0.0
    temp2=0.0
    temp3=0.0
    czujnikZajetosciFlaga=False
    czujnikZajetosciRaw=0
    tryb=0
    czas=datetime.datetime.now()
buda=budaCl

class dekoPok1Cl:     #Dekoracje w salonie Reka
    Adres=5
    Flaga=0
    AutoON='15:50:00.0000'
    AutoOFF='23:05:00.0000'
    AutoLux_min=700 #ustawienie minimum oswietlenia przy ktorym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    blad=0
    Opis="Lampa-reka"
dekoPok1=dekoPok1Cl

class deko2Pok1Cl:     #Dekoracje 2 w salonie  Eifla i inne
    Adres=6
    Flaga=0
    AutoON='15:50:00.0000'
    AutoOFF='23:04:00.0000'
    AutoLux_min=800 #ustawienie minimum oswietlenia przy ktorym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    blad=0
    Opis="Dekoracje szafka"
deko2Pok1=deko2Pok1Cl

class dekoFlamingCl:     #Dekoracje w sypialni
    Flaga=0
    AutoON='20:00:00.0000'
    AutoOFF='23:59:00.0000'
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    AutoLux_min=400 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    blad=0
    Adres=7
    Opis='Flaming'
dekoFlaming=dekoFlamingCl

class dekoUsbCl:     #USB Stick
    AutoON='17:00:00.0000'
    AutoOFF='23:00:00.0000'
    AutoLux_min=1100
    AutoJasnosc=1
    Flaga=0
    blad=0
    FlagaSterowanieManualne=False
    Adres=8
    Opis='USB-Stick'
dekoUsb=dekoUsbCl

class hydroponikaCl:     #Hydroponika
    AutoON='08:00:00.0000'
    AutoOFF='19:00:00.0000'
    AutoLux_min=65000
    Flaga=0
    blad=0
    AutoJasnosc=1
    FlagaSterowanieManualne=False
    Adres=15
    Opis='Hyroponika'
hydroponika=hydroponikaCl

class lampaTVCl:     #LED TV
    Ustawienie="255255255"
    Bialy=000
    Jasnosc=70
    Flaga=0
    AutoON='16:00:00.0000'
    AutoOFF='23:00:00.0000'
    AutoLux_min=1000 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=70
    blad=0
    Adres=1
    Opis="LED TV"
lampaTV=lampaTVCl

class lampaPok2Cl:  # OSWIETLENIE SYPIALNI
    Jasnosc=0
    Flaga=0
    AutoON='21:00:00.0000'
    AutoOFF='23:50:00.0000'
    AutoLux_min=400 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=5
    blad=0
    Adres=2
    Opis='Sypialnia'
lampaPok2=lampaPok2Cl

class lampa1Pok1Cl:  # REFLEKTOR W SALONIE
    Ustawienie="000000000100"
    Jasnosc=0
    Flaga=0
    blad=0
    Adres=3
    Opis='Reflektor 1'
lampa1Pok1=lampa1Pok1Cl

class lampaKuchCl:  # OSWIETLENIE KUCHNI
    Flaga=0
    AutoON='15:00:00.0000'
    AutoOFF='23:58:00.0000'
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    AutoLux_min=1300 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    blad=0
    Adres=4
    Opis='Kuchnia'
lampaKuch=lampaKuchCl

class lampaDuzaTradfriCl:
    Adres="65537" #Adres="131079"  -> grupa
    Status=False
lampaDuzaTradfri=lampaDuzaTradfriCl

class lampaPok1TradfriCl:
    Zarowka="65559"
    Adres="131074"
    Status=False
lampaPok1Tradfri=lampaPok1TradfriCl

class lampaJadalniaTradfriCl:
    Adres="131075"
    Status=False
lampaJadalniaTradfri=lampaJadalniaTradfriCl

class lampaPok2TradfriCl:  #SYPIALNIA
    Adres="131082"
    Flaga=0
    AutoON='21:10:00.0000'
    AutoOFF='23:50:00.0000'
    AutoLux_min=600 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=5
    blad=0
    Opis="Lampy sypialnia"
lampaPok2Tradfri=lampaPok2TradfriCl

class lampaPrzedpokojTradfriCl:
    Adres="131077"
    Status=False
    Opis="Oswietlenie przedpokoj"
lampaPrzedpokojTradfri=lampaPrzedpokojTradfriCl

class automatykaOswietleniaCl:
    wartosciLux=[2000,2000,2000,2000,2000]
    swiatloObliczone=2000
    flagaSwiatloWlaczone=False
automatykaOswietlenia=automatykaOswietleniaCl()