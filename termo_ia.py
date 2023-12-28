# -*- coding: utf-8 -*-

import random
import pygame
import unicodedata

def remover_acentos(palavra):
    palavra_sem_acentos = ''.join(c for c in unicodedata.normalize('NFD', palavra) if unicodedata.category(c) != 'Mn')
    return palavra_sem_acentos.upper()

def abrir_dic(nome_arquivo):
    arquivo = open(nome_arquivo, "r", encoding="utf-8")
    palavras = arquivo.readlines()
    arquivo.close()
    return [remover_acentos(palavra)[:5] for palavra in palavras]


dic_termo = abrir_dic("dicionario_termo.txt")
dic_tentativas = abrir_dic("tentativas.txt")

resposta = random.choice(dic_termo)
print(resposta)


primeira_tentativa = random.choice(dic_termo) # gera a 1 palavra para ser tentada pela I.A.

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
tentativas = [primeira_tentativa]

letras_verde = []
letras_amarela = []
letras_cinza = []

ultima_palavra = []

cont = 0

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
  letras_nao_usadas = ""
  for letra in alfabeto:
    if letra not in letras_usadas:
      letras_nao_usadas = letras_nao_usadas + letra

  return letras_nao_usadas

def determina_cor(tentativa, j):
    letra = tentativa[j]

    if letra == resposta[j]:
        return verde

    elif letra in resposta:
        n_letras_resp = resposta.count(letra)
        n_correto = 0
        n_ocorrencias = 0
        for i in range(5):
            if tentativa[i] == letra:
                if i <= j:
                    n_ocorrencias += 1
                if letra == resposta[i]:
                    n_correto += 1

        if (n_letras_resp - n_correto - n_ocorrencias) >= 0:
            return amarelo

    return cinza

def switchCorExtenso(cor, palavra_tentativa, posicao_letra):
    letra = palavra_tentativa[posicao_letra]
    letra_e_pos = {"letra": letra, "posicao": posicao_letra}

    if cor == cinza and letra not in letras_cinza:
        letras_cinza.append(letra)

    elif cor == amarelo:
        if all(
            (
                letra_e_pos["letra"] != dic["letra"] or letra_e_pos["posicao"] != dic["posicao"]
            )
            for dic in letras_amarela
        ) or not letras_amarela:
            letras_amarela.append({"letra": letra, "posicao": posicao_letra})

    elif cor == verde:
        if all(
            (
                letra_e_pos["letra"] != dic["letra"] or letra_e_pos["posicao"] != dic["posicao"]
            )
            for dic in letras_verde
        ) or not letras_verde:
            letras_verde.append({"letra": letra, "posicao": posicao_letra})


  # elif cor == verde and letra not in [dic["letra"] for dic in letras_amarela]:
  #   letras_verde.append({"letra": letra, "posicao": posicao_letra})
  
def mostra(cont):
    if cont == 0:
      print(f"letras cinzas {letras_cinza} \n")
      print(f"letras amarelas {letras_amarela} \n")
      print(f"letras verdes {letras_verde} \n")
    cont += 1 
    return cont


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
        cor = determina_cor(tentativas[i], j)
        switchCorExtenso(cor,tentativas[i], j)
        pygame.draw.rect(tela, cor, quadrado, border_radius=3)
        letra = fonte.render(tentativas[i][j], False, (255, 255, 255))
        superficie = letra.get_rect(center= (x + tm_quadrado//2, y + tm_quadrado//2))
        tela.blit(letra, superficie)

      if i == len(tentativas) and j < len(entrada):
        letra = fonte.render(entrada[j], False, cinza)
        superficie = letra.get_rect(center= (x + tm_quadrado//2, y + tm_quadrado//2))
        tela.blit(letra, superficie)

      x += tm_quadrado + margem

    y += tm_quadrado + margem

  if len(tentativas) == 6 and tentativas[5] != resposta:
    fim_de_jogo = True
    letras = fonte.render(resposta, False, cinza)
    superficie = letras.get_rect(center= (largura//2, altura-margem_inferior//2-margem))
    tela.blit(letras, superficie)
    cont = mostra(cont)

  pygame.display.flip()

  for evento in pygame.event.get():

    if evento.type == pygame.QUIT:
      animacao = False

    elif evento.type == pygame.KEYDOWN:

      if evento.key == pygame.K_ESCAPE:
        animacao = False

      if evento.key == pygame.K_BACKSPACE:
        if len(entrada) > 0:
          entrada = entrada[:len(entrada)-1]

      elif evento.key == pygame.K_RETURN:
        if len(entrada) == 5 and entrada in dic_tentativas:
          tentativas.append(entrada)
          letras_sobra = letras_ja_usadas(tentativas)
          fim_de_jogo = True if entrada == resposta else False
          entrada = ""
        
      elif evento.key == pygame.K_SPACE:
        fim_de_jogo = False
        resposta = random.choice(dic_termo)
        primeira_tentativa = random.choice(dic_termo) # gera a 1 palavra para ser tentada pela I.A.
        entrada = ""
        tentativas = [primeira_tentativa]
        letras_sobra = alfabeto


      elif len(entrada) < 5 and not fim_de_jogo:
        entrada = entrada + evento.unicode.upper()