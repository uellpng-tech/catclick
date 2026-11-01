import time as tm
import pyautogui as py
import threading

rodando = False

def comecaclique(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao):
    global rodando
    rodando = True

    x = int(entradax.get())
    y = int(entraday.get())

    min = int(entradamin.get())
    seg = int(entradaseg.get())
    milis = int(entradamilis.get())

    tempo = min * 60 + seg + milis / 1000

    while rodando:

        if clicktipo.get() == "Dois cliques":
            py.doubleClick(x, y)
        else:
            if clickbotao.get() == "Direito":
                py.click(x, y, button="right")
            elif clickbotao.get() == "Rolagem":
                py.click(x, y, button="middle")
            else:
                py.click(x, y)

        tm.sleep(tempo)

def comecarautomacao(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao, rodandoe=False):
    if rodandoe == False:
        return
    else:
        threading.Thread(target=comecaclique, args=(entradax, entraday, entradamin, entradaseg, entradamilis, clicktipo, clickbotao), daemon=True).start()

def pararf():
    global rodando
    rodando = False

def alternar():
    global rodando

    if rodando == False:
        pararf()
    else:
        comecarautomacao()