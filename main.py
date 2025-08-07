import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pygame
import os
from mutagen.mp3 import MP3  
from tkinter import Canvas


pygame.mixer.init()

playlist = [
    {
        "titulo": "Headlock",
        "artista": "Imogen Heap",
        "arquivo": "headlock.mp3",
        "capa": "headlock.jpg"
    },
    {
        "titulo": "Bout It",
        "artista": "JMSN",
        "arquivo": "bout_it.mp3",
        "capa": "bout_it.jpg"

    },
        {
            "titulo": "Lover Girl",
            "artista": "Laufey",
            "arquivo": "lover_girl.mp3",
            "capa": "lover_girl.jpg"
        },
        {
            "titulo": "Ruthlessness",
            "artista": "Epic, The Musical",
            "arquivo": "ruthlessness.mp3",
            "capa": "ruthlessness.jpg"
        }
    ]

musica_atual = 0  
em_execucao = False




cor_barra = "#8B6024"  

def atualizar_barra():
    canvas_barra.delete("all")
    y1, y2 = 4, 7
    largura_total = 250

    if pygame.mixer.music.get_busy():
        try:
            pos = pygame.mixer.music.get_pos() / 1000  
            audio = MP3(playlist[musica_atual]["arquivo"])
            duracao = audio.info.length
            progresso = (pos / duracao) * largura_total if duracao > 0 else 0

            canvas_barra.create_rectangle(0, y1, progresso, y2, fill=cor_barra, outline=cor_barra)

            raio = 4
            x = progresso
            canvas_barra.create_oval(x - raio, y1 - raio, x + raio, y2 + raio, fill="white", outline=cor_barra, width=1.5)

        except Exception:
            pass

    janela.after(500, atualizar_barra)




def tocar_musica():
    global em_execucao
    pygame.mixer.music.load(playlist[musica_atual]["arquivo"])
    pygame.mixer.music.play()
    atualizar_interface()
    em_execucao = True
    botao_play.config(image=icone_pause)

def pausar_ou_retomar():

    global em_execucao
    if em_execucao:
        pygame.mixer.music.pause()
        em_execucao = False
        botao_play.config(image=icone_play)
    else:
        pygame.mixer.music.unpause()
        em_execucao = True
        botao_play.config(image=icone_pause)



def proxima():
    global musica_atual
    musica_atual = (musica_atual + 1) % len(playlist)
    tocar_musica()



def anterior():
    global musica_atual
    musica_atual = (musica_atual - 1) % len(playlist)
    tocar_musica()


def atualizar_interface():
    dados = playlist[musica_atual]
    titulo.set(dados["titulo"])
    artista.set(dados["artista"])

    img = Image.open(dados["capa"])
    img = img.resize((193, 193))
    img = ImageTk.PhotoImage(img)
    capa_label.config(image=img)
    capa_label.image = img



janela = tk.Tk()
janela.title("Meu Player")
janela.geometry("320x400")
janela.resizable(False, False)
janela.configure(bg="#E8C698")

titulo = tk.StringVar()
artista = tk.StringVar()


canvas_barra = Canvas(janela, width=250, height=8, bg="#E8C698", highlightthickness=0)
canvas_barra.place(x=35, y=305)

capa_label = tk.Label(janela, bg="#E8C698")
capa_label.pack(pady=10)

janela.after(500, atualizar_barra)

bg_img = Image.open("fundo1.png").resize((265, 60))
bg_img_tk = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(janela, image=bg_img_tk, bg="#E8C698", bd=0)
bg_label.place(x=28, y=230)


tk.Label(janela, textvariable=titulo, font=("lexend", 12, "bold"), bg="#D8AD70", fg="#FFFFFF", bd=0, highlightthickness=0).place(x=40, y=238, anchor="nw")
tk.Label(janela, textvariable=artista, font=("lexend", 10, "bold"), bg="#D8AD70", fg="#8A6024", bd=0, highlightthickness=0).place(x=40, y=258, anchor="nw")


frame_botoes = tk.Frame(janela, bg="#E8C698")
frame_botoes.pack(pady=10)

icone_play = ImageTk.PhotoImage(Image.open("play.png").resize((25, 25)))
icone_pause = ImageTk.PhotoImage(Image.open("pause.png").resize((25, 25)))
icone_avancar = ImageTk.PhotoImage(Image.open("avancar.png").resize((18, 18)))
icone_voltar = ImageTk.PhotoImage(Image.open("voltar.png").resize((18, 18)))

frame_botoes.place(x=95, y=340) 

botao_voltar = tk.Button(frame_botoes, image=icone_voltar, command=anterior, bd=0, bg="#E8C698", activebackground="#E8C698")
botao_voltar.grid(row=0, column=0, padx=10)

botao_play = tk.Button(frame_botoes, image=icone_play, command=pausar_ou_retomar, bd=0, bg="#E8C698", activebackground="#E8C698")
botao_play.grid(row=0, column=1, padx=10)

botao_avancar = tk.Button(frame_botoes, image=icone_avancar, command=proxima, bd=0, bg="#E8C698", activebackground="#E8C698")
botao_avancar.grid(row=0, column=2, padx=10)



janela.after(100, tocar_musica)

janela.mainloop()



