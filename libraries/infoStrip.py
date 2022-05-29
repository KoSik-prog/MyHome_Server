# -*- coding: utf-8 -*-

from devicesList import *

class INFO_STRIP_CL:
    actualInformation=""
    displayedInformation=""
    informations=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    errorsArray=[[False,"blad czujnika zewnetrznego"],
    [False,"blad czujnika salonu"],
    [False,"blad czujnika sypialni"],
    [False,"blad czujnika kwiatka (Konewka)"],
    [False,"blad czujnika kwiatka 12 (" + czujnikKwiatek2.name + ")"],
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
    errorPosition=0
    time=0
    position=0


    def set_error(self, numerBledu, aktywny):
        self.errorsArray[numerBledu][0]=aktywny

    def read_error(self):
        blad=""
        for x in range(len(self.errorsArray)):
            self.errorPosition+=1
            if self.errorPosition > len(self.errorsArray)-1:
                self.errorPosition=0
            if(self.errorsArray[self.errorPosition][0] == True):
                blad=self.errorsArray[self.errorPosition][1]
                break
        return blad

    def add_info(self, info):
        for i in range(len(self.informations)):
            if self.informations[i]=="":
                self.informations[i]=info
                break

    def read_info(self):
        info=""
        info=self.informations[0]
        for i in range(len(self.informations)-1):
            self.informations[i]=self.informations[i+1]
        return info

infoStrip=INFO_STRIP_CL()