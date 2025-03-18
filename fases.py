import random

def escolherPeca():
    peca = random.randint(0 , 3)
    return peca

def criarFase(tamanho):
    tabuleiro = []
    _tamanho = tamanho ** 2
    for i in range(0 , _tamanho):
        tabuleiro.append(escolherPeca())
    return tabuleiro

fasesFacil = []
for i in range(0 , 9):
    fasesFacil.append(criarFase(7))
    
fasesNormal = []
for i in range(0 , 9):
    fasesNormal.append(criarFase(9))

fasesDificil = []
for i in range(0 , 9):
    fasesDificil.append(criarFase(11))

'''
contador = 1
for i in fasesFacil[0]:
    print(f"{contador} : {i}")
    contador += 1
'''