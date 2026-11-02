import time as tm
import pyautogui as py
import threading

rodando = False

def comecaclique(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao):
    global rodando
    rodando = True

    x = int(entradax)
    y = int(entraday)

    min = int(entradamin)
    seg = int(entradaseg)
    milis = int(entradamilis)

    tempo = min * 60 + seg + milis / 1000

    while rodando:

        if clicktipo == "Dois cliques":
            py.doubleClick(x, y)
        else:
            if clickbotao == "Direito":
                py.click(x, y, button="right")
            elif clickbotao == "Rolagem":
                py.click(x, y, button="middle")
            else:
                py.click(x, y)

        tm.sleep(tempo)

def comecarautomacao(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao, rodandoe=False):
    if rodandoe == False:
        return
    else:
        threading.Thread(target=comecaclique, args=(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao)).start()

def pararf():
    global rodando
    rodando = False

def alternar(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao):
    global rodando

    if rodando == True:
        pararf()
    else:
        comecarautomacao(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao, rodandoe=True)