#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        info strip
# Purpose:
#
# Author:      KoSik
#
# Created:     26.03.2021
# Copyright:   (c) kosik 2021
# -------------------------------------------------------------------------------
try:
    from devicesList import *
except ImportError:
    print("Import error - info strip")


class InfoStrip:
    actualInformation = ""
    displayedInformation = ""
    informations = ["", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    errorsArray = [[False, "blad czujnika zewnetrznego"],
                   [False, "blad czujnika salonu"],
                   [False, "blad czujnika sypialni"],
                   [False, "blad czujnika kwiatka (Konewka)"],
                   [False, "blad czujnika kwiatka 12 (Palma)"],
                   [False, "blad czujnika kwiatka 13 (Pachira)"],
                   [False, "blad czujnika kwiatka 14 (Pokrzywa)"],
                   [False, "minimalny poziom baterii kwiatka (konewka)"],
                   [False, "minimalny poziom baterii kwiatka 12 (Palma)"],
                   [False, "minimalny poziom baterii kwiatka 13 (Pachira)"],
                   [False, "minimalny poziom baterii kwiatka 14 (Pokrzywa)"],
                   [False, "wilgotnosc kwiatka 12 (Palma) ponizej 5%"],
                   [False, "wilgotnosc kwiatka 13 (Pachira) ponizej 5%"],
                   [False, "wilgotnosc kwiatka 14 (Pokrzywa) ponizej 5%"],
                   [False, "minimalny poziom baterii kwiatka 16 (Benjamin)"],
                   [False, "wilgotnosc kwiatka 16 (Benjamin) ponizej 5%"],
                   [False, "blad czujnika kwiatka 16 (Benjamin)"],
                   [False, "minimalny poziom baterii kwiatka 17 (Szeflera)"],
                   [False, "wilgotnosc kwiatka 17 ponizej 5% (Szeflera)"],
                   [False, "blad czujnika kwiatka 17 (Szeflera)"],
                   [False, "mała ilosc wody dla kwiatka - konewka"]]
    errorPosition = 0
    time = 0
    position = 0

    def set_error(self, errorNumber, isActiveFlag):
        self.errorsArray[errorNumber][0] = isActiveFlag

    def read_error(self):
        error = ""
        for x in range(len(self.errorsArray)):
            self.errorPosition += 1
            if self.errorPosition > len(self.errorsArray)-1:
                self.errorPosition = 0
            if (self.errorsArray[self.errorPosition][0] == True):
                error = self.errorsArray[self.errorPosition][1]
                break
        return error

    def add_info(self, info):
        for i in range(len(self.informations)):
            if self.informations[i] == "":
                self.informations[i] = info
                break

    def read_info(self):
        info = ""
        info = self.informations[0]
        for i in range(len(self.informations) - 1):
            self.informations[i] = self.informations[i+1]
        return info
    
    def get_errors_array(self):
        activeErrors = []
        for element in self.errorsArray:
            if element[0] == True:
                activeErrors.append(element[1])
        return {"errors":activeErrors}


infoStrip = InfoStrip()
