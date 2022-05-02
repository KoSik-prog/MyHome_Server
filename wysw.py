# -*- coding: utf-8 -*-
try:
    import select, time, datetime, pogoda
except ImportError:
    print "Blad importu"

import sys ,os
import pygame, pygame.mixer, pygame.gfxdraw, glob
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
from time import sleep

licznik=0
czaspogody=0

bgcolor=(255,255,255,255)
aktualny_obraz=0
tryb_nocny=False
glowny=1

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'ikony')

def dzien(dzientyg):
    if(dzientyg==0):
        return "poniedziałek"
    if(dzientyg==1):
        return "wtorek"
    if(dzientyg==2):
        return "środa"
    if(dzientyg==3):
        return "czwartek"
    if(dzientyg==4):
        return "piątek"
    if(dzientyg==5):
        return "sobota"
    if(dzientyg==6):
        return "niedziela"

def miesiac(mies):
    if(mies=="January"):
        return "stycznia"
    elif(mies=="February"):
        return "lutego"
    elif(mies=="March"):
        return "marca"
    elif(mies=="April"):
        return "kwietnia"
    elif(mies=="May"):
        return "maja"
    elif(mies=="June"):
        return "czerwca"
    elif(mies=="July"):
        return "lipca"
    elif(mies=="August"):
        return "sierpnia"
    elif(mies=="September"):
        return "września"
    elif(mies=="October"):
        return "października"
    elif(mies=="November"):
        return "listopada"
    elif(mies=="December"):
        return "grudnia"
    else:
        return "error"
#======GRAFIKA========================================
def load_image(name):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image

class Obrazki(object):
    def __init__(self):
        self.tempin = load_image("temp_in.gif")
        self.tempout = load_image("temp_out.gif")
        self.wind = load_image("wind.gif")

global obrazek
obrazek = Obrazki()

def obraz(screen, osx ,osy, alpha, nazwa):
    if(nazwa == "temp_out"):
        foto=obrazek.tempout.convert()
    elif(nazwa == "temp_in"):
        foto=obrazek.tempin.convert()
    elif(nazwa == "wind"):
        foto=obrazek.wind.convert()
    else:
        #zapis_bledu(nazwa)
        foto=ikona.NA.convert()
    foto.set_alpha(alpha)
    screen.blit(foto, (osx, osy))

def box(screen, x,y,w,h,color):
    pygame.gfxdraw.box(screen, Rect((x,y),(w,h)), color)

def napis_centralny(screen, tekst, font, rozmiar, x, y, color, alpha):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    ren = a_sys_font.render(unicode(tekst,'utf-8'), True, color)
    ren.set_alpha(alpha)
    screen.blit(ren, (x - ren.get_width() // 2, y - ren.get_height() // 2))

def napis_centralny_tlo(screen, tekst, font, rozmiar, x, y, color, alpha, bgcolor):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    ren = a_sys_font.render(unicode(tekst,'utf-8'), True, color)
    ren.set_alpha(alpha)
    box(screen, x - ren.get_width() // 2,y - ren.get_height() // 2,ren.get_width()+30,ren.get_height(),bgcolor)
    screen.blit(ren, (x - ren.get_width() // 2, y - ren.get_height() // 2))

def napis_tlo(screen, tekst, font, rozmiar, x, y, color, alpha,bgcolor):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    text = a_sys_font.render(unicode(tekst,'utf-8'),True, color)
    text.set_alpha(alpha)
    box(screen, x,y,text.get_width()+30,text.get_height(),bgcolor)
    screen.blit(text, (x, y))

def napis2(screen, tekst, font, rozmiar, x, y, color, alpha):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    text = a_sys_font.render(unicode(tekst,'utf-8'),True, color)
    text.set_alpha(alpha)
    screen.blit(text, (x, y))
    return text.get_width()

def stan_ikona(x,y,stan):
    zielony=(0,150,0,255)
    czerwony=(150,0,0,255)

    if(stan==1):
        pygame.draw.circle(screen, zielony, (x,y), 12)
    elif(stan==0):
        pygame.draw.circle(screen, czerwony, (x,y), 12)
    else:
        pygame.draw.circle(screen, (0,0,150,255), (x,y), 12)

def wykres(x,y,procent,kolor):
    box(x,(y-4),150,-22,(255,255,255,255))
    pygame.draw.rect(screen, (100,100,100,255), [x-4,y,158,-30], 3)
    box(x,(y-4),int(procent*1.5),-22,kolor)

def obraz_stan(swiatlo,kwiatwilg,kwiatslonce,kwiatwoda,kwiatzas, ledLampFlag, ledLampPWM, ledLampWhite, ledtvFlag, ledtvjasnosc, ledSypFlag, ledSypialniPWM, ledKuchFlag):
    global screen, licznik, glowny
    global czasodswpogody,czaspogody
    kolor=(0,0,0,250)
    kolor_cien=(200,200,200,255)
    czcionka1=(100,80,0,255)
    menu_ustawien=True
    menu=0

    while(menu_ustawien==True):
        box(13,413,140,60,kolor_cien)
        box(163,413,140,60,kolor_cien)
        box(313,413,140,60,kolor_cien)
        box(463,413,140,60,kolor_cien)
        box(653,413,140,60,kolor_cien)
        box(10,410,140,60,(20,200,0,255))
        box(160,410,140,60,(20,200,0,255))
        box(310,410,140,60,(20,200,0,255))
        box(460,410,140,60,(20,200,0,255))
        box(650,410,140,60,(0,100,100,255))
        napis_centralny("STAN","Nimbus Sans L",42,80,440,(100,80,0,255),255)
        napis_centralny("KWIATEK","Nimbus Sans L",42,230,440,(100,80,0,255),255)
        napis_centralny("LCD","Nimbus Sans L",42,380,440,(100,80,0,255),255)
        napis_centralny("TIMER","Nimbus Sans L",42,530,440,(100,80,0,255),255)

        napis_centralny("WROC","Nimbus Sans L",42,720,440,(100,80,0,255),255)

        if menu==0:
            stan_ikona(40,35,ledtvFlag)
            napis2("LED TV","Nimbus Sans L",42,65,20,czcionka1,255)
            #napis2("Jasnosc:"+str(ledtvjasnosc),"Nimbus Sans L",42,300,20,czcionka1,255)
            wykres(220,50,(ledtvjasnosc/2.55),(157,119,147,255))
            stan_ikona(40,75,ledLampFlag)
            napis2("lampa","Nimbus Sans L",42,65,60,czcionka1,255)
            napis2(" / "+str(ledLampPWM),"Nimbus Sans L",42,390,60,czcionka1,255)
            wykres(220,90,(ledLampWhite/2.55),(157,119,147,255))
            stan_ikona(40,115,ledKuchFlag)
            napis2("kuchnia","Nimbus Sans L",42,65,100,czcionka1,255)
            stan_ikona(40,155,ledSypFlag)
            napis2("sypialnia","Nimbus Sans L",42,65,140,czcionka1,255)
            #napis2("Jasnosc:"+str(ledSypialniPWM),"Nimbus Sans L",42,300,140,czcionka1,255)
            wykres(220,170,(ledSypialniPWM/2.55),(157,119,147,255))
            menu_ustawien=False

        pygame.display.update()
        time.sleep(0.5)

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px=event.pos[0]
                py=event.pos[1]
                if(px>650 and px<790 and py>410 and py<470):
                    #menu_ustawien=False
                    glowny=1
                    screen.fill(bgcolor)
    return False


def obraz_kwiatek(kwiatwilg,kwiatslonce,kwiatwoda,kwiatzas):
    global screen, licznik
    global czasodswpogody,ledtvjasnosc, czaspogody
    kolor=(0,0,0,250)
    kolorczcionki1=(30,30,30,255)
    kolorczcionki2=(60,60,60,255)

    napis2(str(kwiatwilg)+"%","Nimbus Sans L",68,20,10,kolorczcionki2,255)
    napis2(str(kwiatslonce)+"%","Nimbus Sans L",68,20,80,kolorczcionki2,255)
    napis2(str(kwiatwoda)+"%","Nimbus Sans L",68,20,150,kolorczcionki2,255)
    napis2(str(kwiatzas)+"%","Nimbus Sans L",68,20,230,kolorczcionki2,255)
