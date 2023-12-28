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
margem = 10
margem_topo = 100
margem_inferior = 100
margem_lados = 100

cinza = (70, 70, 80)
verde = (6, 214, 160)
amarelo = (255, 209, 102)

entrada = ""
tentativas = []
alfabeto = "ABCDEFGHIJKLNMOPQRSTUVWXYZÇ"
letras_sobra = alfabeto
fim_de_jogo = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Termo")

tm_quadrado = (largura - 4 * margem - 2 * margem_lados) // 5
fonte = pygame.font.SysFont("free sans bold", tm_quadrado)
fonte_pequena = pygame.font.SysFont("free sans bold", tm_quadrado//2)


def letras_ja_usadas(tentativas):
 letras_usadas = "".join(tentativas)

#config tela
tela = pygame.display.set_mode((largura, altura))

#loop de jogadas
animacao = True
while animacao:

  tela.fill("white")

  letras = fonte_pequena.render(letras_sobra, False, cinza)
  superficie = letras.get_rect(center= (largura//2, margem_topo//2))
  tela.blit(letras, superficie)

  y = margem_topo
  for i in range(6):
    x = margem_lados
    for j in range(5):
      quadrado = pygame.Rect(x, y, tm_quadrado, tm_quadrado)
      pygame.draw.rect(tela, cinza, quadrado, width=2, border_radius=3)

      if i < len(tentativas):
        cor = cinza
        pygame.draw.rect(tela, cor, quadrado, border_radius=3)
        letra = fonte.render(tentativas[i][j], False, (255, 255, 255))
        superficie = letra.get_rect(center= (x + tm_quadrado//2, y + tm_quadrado//2))
        tela.blit(letra, superficie)

      x += tm_quadrado + margem

    y += tm_quadrado + margem


  pygame.display.flip()

  for evento in pygame.event.get():

    if evento.type == pygame.QUIT:
      animacao = False

    elif evento.type == pygame.KEYDOWN:

      if evento.key == pygame.K_ESCAPE:
        animacao = False

      elif evento.key == pygame.K_RETURN:
        if len(entrada) == 5 and entrada not in tentativas:
          tentativas.append(entrada)
          fim_de_jogo = True if entrada == resposta else False
          entrada = ""


      elif len(entrada) < 5 and not fim_de_jogo:
        entrada = entrada + evento.unicode.upper()