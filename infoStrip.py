# -*- coding: utf-8 -*-

from devicesList import *

class INFO_STRIP_CL:
    aktualnaInformacja=""
    wyswietlanaInformacja=""
    informacje=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    bledy=[[False,"blad czujnika zewnetrznego"],
    [False,"blad czujnika salonu"],
    [False,"blad czujnika sypialni"],
    [False,"blad czujnika kwiatka (Konewka)"],
    [False,"blad czujnika kwiatka 12 (" + czujnikKwiatek2.nazwa + ")"],
    [False,"blad czujnika kwiatka 13 (Pachira)"],
    [False,"blad czujnika kwiatka 14 (Pokrzywa)"],
    [False,"minimalny poziom baterii kwiatka (konewka)"],
    [False,"minimalny poziom baterii kwiatka 12 (Palma)"],
    [False,"minimalny poziom baterii kwiatka 13 (Pachira)"],
    [False,"minimalny poziom baterii kwiatka 14 (Pokrzywa)"],
    [False,"wilgotnosc kwiatka 12 (Palma) ponizej 5%"],
    [False,"wilgotnosc kwiatka 13 (Pachira) ponizej 5%"],
    [False,"wilgotnosc kwiatka 14 (Pokrzywa) ponizej 5%"],
    [False,"minimalny poziom baterii kwiatka 16 (Benjamin)"],
    [False,"wilgotnosc kwiatka 16 (Benjamin) ponizej 5%"],
    [False,"blad czujnika kwiatka 16 (Benjamin)"],
    [False,"minimalny poziom baterii kwiatka 17 (Szeflera)"],
    [False,"wilgotnosc kwiatka 17 ponizej 5% (Szeflera)"],
    [False,"blad czujnika kwiatka 17 (Szeflera)"],
    [False,"mała ilosc wody dla kwiatka - konewka"]]
    pozycjaOdczytuBledu=0
    czas=0
    pozycja=0


    def dodajUsunBlad(self, numerBledu, aktywny):
        self.bledy[numerBledu][0]=aktywny

    def odczytajBlad(self):
        blad=""
        for x in range(len(self.bledy)):
            self.pozycjaOdczytuBledu+=1
            if self.pozycjaOdczytuBledu > len(self.bledy)-1:
                self.pozycjaOdczytuBledu=0
            if(self.bledy[self.pozycjaOdczytuBledu][0] == True):
                blad=self.bledy[self.pozycjaOdczytuBledu][1]
                break
        return blad

    def dodajInfo(self, informacja):
        for i in range(len(self.informacje)):
            if self.informacje[i]=="":
                self.informacje[i]=informacja
                break

    def odczytajInfo(self):
        informacja=""
        informacja=self.informacje[0]
        for i in range(len(self.informacje)-1):
            self.informacje[i]=self.informacje[i+1]
        return informacja

infoStrip=INFO_STRIP_CL()