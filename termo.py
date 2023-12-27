# -*- coding: utf-8 -*-

import random
import pygame

def abrir_dic(nome_arquivo):
  arquivo = open(nome_arquivo, "r", encoding="utf-8")
  palavras = arquivo.readlines()
  arquivo.close()
  return [palavra[:5].upper() for palavra in palavras] 

dic_termo = abrir_dic("dicionario_termo.txt")
dic_tentativas = abrir_dic("tentativas.txt")

resposta = random.choice(dic_termo)
print(resposta)

largura = 600
altura = 700

pygame.init()
pygame.font.init()
pygame.display.set_caption("Termo")

#config tela
tela = pygame.display.set_mode((largura, altura))

#loop de jogadas
animacao = True
while animacao:

  tela.fill("white")
  pygame.display.flip()

  for evento in pygame.event.get():

    if evento.type == pygame.QUIT:
      animacao = False

    elif evento.type == pygame.KEYDOWN:

      if evento.type == pygame.K_ESCAPE:
        animacao = False