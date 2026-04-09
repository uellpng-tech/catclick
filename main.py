import tkinter as tk
import time as tm
import pyautogui as py
import threading
import keyboard
from tkinter import PhotoImage, Label,ttk
from pynput.mouse import Listener, Button

janela = tk.Tk()
janela.title("CatClick")
janela.geometry("500x400")
janela.iconbitmap("imagens/icon.ico")
janela.resizable(width=False, height=False)
fundo = PhotoImage(file="imagens/fundo.png")
labelfundo = Label(janela, image=fundo)
labelfundo.place(x=0, y=0, relwidth=1, relheight=1)

def limite(texto):
    return texto.isdigit() and len(texto) <= 2 or texto == ""

def zero(event):
    if entradamin.get() == "":
        entradamin.insert(0, "0")
    if entradaseg.get() == "":
        entradaseg.insert(0, "0")
    if entradamilis.get() == "":
        entradamilis.insert(0, "0")

limitarn = (janela.register(limite), "%P")

tk.Label(janela, text="Intervalo entre cliques").place(x=5, y=10)
labelmin = tk.Label(janela, text="Minutos:").place(x=5, y=40)
labelseg = tk.Label(janela, text="Segundos:").place(x=5, y=65)
labelmilis = tk.Label(janela, text="Milissegundos:").place(x=5, y=90)

entradamin = tk.Entry(janela, width=5, validate="key", validatecommand=limitarn)
entradamin.place(x=60, y=42)
entradamin.insert(0,"0")
entradamin.bind("<FocusOut>", zero)

entradaseg = tk.Entry(janela, width=5, validate="key", validatecommand=limitarn)
entradaseg.place(x=70, y=67)
entradaseg.insert(0,"0")
entradaseg.bind("<FocusOut>", zero)

entradamilis = tk.Entry(janela, width=5, validate="key", validatecommand=limitarn )
entradamilis.place(x=93, y=92)
entradamilis.insert(0,"0")
entradamilis.bind("<FocusOut>", zero)

click = tk.Label(janela, text="Tipo de clique").place(x=150 , y=10)

clicktipo = tk.StringVar()
clicktipoopcao = ttk.Combobox(janela, textvariable=clicktipo, width=12)
clicktipoopcao['values'] = ["Um clique", "Dois cliques"]
clicktipoopcao.current(0)
clicktipoopcao.place(x=150 , y=40)

clickbotao =  tk.StringVar()
clickbotaoopcao = ttk.Combobox(janela, textvariable=clickbotao, width=12)
clickbotaoopcao['values'] = ["Esquerdo", "Direito", "Rolagem"]
clickbotaoopcao.current(0)
clickbotaoopcao.place(x=150 , y=65)

def limitarposicao(texto):
    return texto.isdigit() or texto == ""

limitarp = (janela.register(limitarposicao), "%P") 

def capturandoposicao():
    global captura
    captura = True
        
    while captura:
        x, y = py.position()

        entradax.delete(0, tk.END)
        entradax.insert(0, str(x))

        entraday.delete(0, tk.END)
        entraday.insert(0, str(y))

        tm.sleep(0.05)

def clique(x, y, botao, clique):
    global captura

    if clique and botao == Button.left:
        entradax.delete(0, tk.END)
        entradax.insert(0, str(x))

        entraday.delete(0, tk.END)
        entraday.insert(0, str(y))

        ativabotao()

        captura = False
        return False
            

def escolhaposicao():
    global captura
    captura = True

    threading.Thread(target=capturandoposicao, daemon=True).start()

    threading.Thread(target=lambda: Listener(on_click=clique).run(), daemon=True).start()

posicao = tk.Label(janela, text="posição").place(x=270, y=10)

posicaobotao = tk.Button(janela, text="Escolher local", height=1, command=escolhaposicao)
posicaobotao.place(x=270, y=40)

captura = False

textox = tk.Label(janela, text="X").place(x=360, y=43)

entradax = tk.Entry(janela, width=7, validate="key", validatecommand=limitarp)
entradax.place(x=375, y=43)

textoy = tk.Label(janela, text="Y").place(x=430, y=43)

entraday = tk.Entry(janela, width=7, validate="key", validatecommand=limitarp)
entraday.place(x=445, y=43)

def ativabotao():
    x = entradax.get()
    y = entraday.get()
    min = entradamin.get()
    seg = entradaseg.get()
    milis = entradamilis.get()

    if not x.isdigit() or not y.isdigit():
        comeca.config(state="disabled")
        parar.config(state="disabled")
        alternarb.config(state="disabled")
        return
    
    if int(min) == 0 and int(seg) == 0 and int(milis) == 0:
        comeca.config(state="disabled")
        parar.config(state="disabled")
        alternarb.config(state="disabled")
        return
    else:
        comeca.config(state="normal")
        parar.config(state="normal")
        alternarb.config(state="normal")

def comecaclique():
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

def comecarthread():
    global rodando
    if rodando:
        return
    threading.Thread(target=comecaclique, daemon=True).start()

def pararf():
    global rodando
    rodando = False

def alternar():
    global rodando

    if rodando:
        pararf()
    else:
        comecarthread()

def redefinirf():
    entradamin.delete(0, tk.END)
    entradamin.insert(0, "0")

    entradaseg.delete(0, tk.END)
    entradaseg.insert(0, "0")

    entradamilis.delete(0, tk.END)
    entradamilis.insert(0, "0")

    clicktipoopcao.current(0)
    clickbotaoopcao.current(0)

    comeca.config(state="disabled")
    parar.config(state="disabled")
    alternarb.config(state="disabled")

    entradax.delete(0, tk.END)
    entraday.delete(0, tk.END)

    janela.focus_force()

keyboard.add_hotkey("F6", comecarthread)
keyboard.add_hotkey("F7", pararf)
keyboard.add_hotkey("F8", alternar)

py.FAILSAFE = True

comeca = tk.Button(janela, text="Começar (F6)", width=20, height=2, state="disabled", command=comecarthread)
comeca.place(x=185, y=200)


parar = tk.Button(janela, text="Parar (F7)", width=20, height=2, state="disabled", command=pararf)
parar.place(x=340, y=200)

alternarb = tk.Button(janela, text="Alternar (F8)", width=20, height=2, state="disabled", command=alternar)
alternarb.place(x=340, y=250)

redefinir = tk.Button(janela, text="Redefinir", width=20, height=2, command=redefinirf)
redefinir.place(x=185, y=250)

entraday.bind("<KeyRelease>", lambda e: ativabotao()) 
entradax.bind("<KeyRelease>", lambda e: ativabotao()) 
entradamin.bind("<KeyRelease>", lambda e: ativabotao()) 
entradaseg.bind("<KeyRelease>", lambda e: ativabotao()) 
entradamilis.bind("<KeyRelease>", lambda e: ativabotao())

if __name__ == "__main__":
    janela.mainloop()