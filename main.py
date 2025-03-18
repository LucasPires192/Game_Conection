import pygame as py
import random
import math

py.init()

# Definindo parâmetros do jogo
j_largura = 1300
j_altura = 720
janela = py.display.set_mode((j_largura , j_altura))
py.display.set_caption('Conection')
background = (192,192,192)
azul = (30,144,255)
verde = (0,255,127)
vermelho = (255 , 0 , 0)
corPeca = verde
preto = (0 , 0 , 0)
azulClaro = (91 , 140 , 238)
movimentos = 0
tamanhoPeca = 20
fonte = py.font.SysFont("Monospace", 30, True, True)
tamanhoFase = 11

x = 150
y = 20
loop = True
listaFormas = ["T", "X", "L", "I"]  # Formas das peças

pecaConectada = []
for i in range(0 , tamanhoFase ** 2):
    pecaConectada.append(i)
    pecaConectada[i] = 0

#lista das formas das pecas
formas = {
    "T": [[0 , 0 , 0], [1 , 1 , 1], [0 , 1 , 0]],
    "X": [[0 , 1 , 0], [1 , 1 , 1], [0 , 1 , 0]],
    "L": [[0 , 1 , 0], [0 , 1 , 1], [0 , 0 , 0]],
    "I": [[0 , 1 , 0], [0 , 1 , 0], [0 , 1 , 0]]
}

#escolhe uma forma aleatoria
def escolherPeca():
    peca = random.choice(listaFormas)
    return peca

# Função para criar o tabuleiro
def criarFase(tamanho):
    tabuleiro = []
    _tamanho = tamanho ** 2
    for i in range(0 , _tamanho):
        tabuleiro.append(rotacionarAleatorio(formas[escolherPeca()]))
    return tabuleiro

#desenha o painel da quantidade de movimentos
def desenharMovimentos():
    _x = 950
    _y = 50
    py.draw.rect(janela , azulClaro , (_x - 5 , _y - 7 , 300 , 50))
    py.draw.rect(janela , preto , (_x - 5 , _y - 7 , 300 , 50) , 3)
    textMovimento = f"Movimentos: {movimentos}"
    formatacao_texto = fonte.render(textMovimento , False , preto)
    janela.blit(formatacao_texto , (_x , _y))

#desenha o inicio da fase
def desenharInicio():
    _x = x - 130 
    _y = y
    py.draw.rect(janela , azul , (x - (tamanhoPeca * 2) , y + tamanhoPeca, tamanhoPeca * 2 , tamanhoPeca))
    imgEnergia = py.image.load('img/energia.png' , 'energia').convert_alpha()
    imgEnergia = py.transform.scale(imgEnergia , (int((imgEnergia.get_width() * 0.1)) , int((imgEnergia.get_height() * 0.1))))
    janela.blit(imgEnergia , (_x  , _y))
    _largura = imgEnergia.get_width()
    _altura = imgEnergia.get_height()
    py.draw.rect(janela , preto , (_x , _y , _largura , _altura) , 3)

#desenha o objetivo final
def desenharFim():
    _x = x + ((tamanhoFase * (tamanhoPeca * 3) + tamanhoPeca * 2))
    _y = y + ((tamanhoFase * (tamanhoPeca * 3) - tamanhoPeca * 8))
    py.draw.rect(janela , vermelho , (x + (tamanhoFase * (tamanhoPeca * 3)) , y + (tamanhoFase * (tamanhoPeca * 3)) - (2 * tamanhoPeca), tamanhoPeca * 2 , tamanhoPeca))
    imgAltair = py.image.load('img/altair8800.png' , 'altair').convert_alpha()
    imgAltair = py.transform.scale(imgAltair , (int((imgAltair.get_width() * 0.4)) , int((imgAltair.get_height() * 0.4))))
    _largura = imgAltair.get_width()
    _altura =  imgAltair.get_height()
    janela.blit(imgAltair , (_x  , _y))
    py.draw.rect(janela , preto , (_x , _y , _largura , _altura) , 3)

# Função para desenhar as peças
def desenharPecas(formas , cor , x , y , tamanhoPeca):
    _cor = cor
    for linhaIndex, linha in enumerate(formas):
        for colunaIndex, coluna in enumerate(linha):
            if coluna:
                py.draw.rect(janela, _cor, (x + colunaIndex * tamanhoPeca, y + linhaIndex * tamanhoPeca, tamanhoPeca, tamanhoPeca))

#desenha o background
def desenharBackground():
        janela.fill(background)
        py.draw.rect(janela , preto , (x - 3, y - 3 , (((tamanhoFase * tamanhoPeca) * 3) + 6), (((tamanhoFase * tamanhoPeca) * 3)) + 6) , 3)

# Função para rotacionar a forma da peça
def rotacionarForma(forma):
    """Rotaciona uma peça 90 graus"""
    _forma = [list(row) for row in zip(*forma[::-1])]
    return _forma

#rotaciona a peca aleatorimente
def rotacionarAleatorio(forma):
    _forma = forma
    for i in range(0 , random.randint(0 , 2)):
        _forma = rotacionarForma(_forma)
    return _forma

# Função para rotacionar a peça selecionada no tabuleiro
def rotacionarPecaSelecionada():
    tabuleiro[selected_piece_index] = rotacionarForma(tabuleiro[selected_piece_index])  # Atualiza a peça no tabuleiro

#funcao para definir as arestas das pecas
def definirArestas(peca1, peca2):
    pass

def estaConectado(peca1, peca2, lado1, lado2):
    """Verifica se as extremidades entre duas peças estão conectadas"""
    return peca1[lado1[0]][lado1[1]] and peca2[lado2[0]][lado2[1]]

def verificarConeccoes(tabuleiro):
    global pecaConectada
    pecaConectada = [0] * (tamanhoFase ** 2)  # Reinicia as conexões

    # A primeira peça (início) está sempre conectada
    pecaConectada[0] = 1

    # Loop para verificar conexões
    for _contador in range(len(tabuleiro)):
        pecaAtual = tabuleiro[_contador]

        # Verifica conexões com peças vizinhas
        if (_contador % tamanhoFase) != 0:  # Não está na borda esquerda
            pecaEsquerda = tabuleiro[_contador - 1]
            if pecaAtual[1][0] and pecaEsquerda[1][2] and pecaConectada[_contador - 1]:
                pecaConectada[_contador] = 1

        if (_contador % tamanhoFase) != (tamanhoFase - 1):  # Não está na borda direita
            pecaDireita = tabuleiro[_contador + 1]
            if pecaAtual[1][2] and pecaDireita[1][0] and pecaConectada[_contador]:
                pecaConectada[_contador + 1] = 1

        if _contador >= tamanhoFase:  # Não está na primeira linha
            pecaAcima = tabuleiro[_contador - tamanhoFase]
            if pecaAtual[0][1] and pecaAcima[2][1] and pecaConectada[_contador - tamanhoFase]:
                pecaConectada[_contador] = 1

        if _contador < len(tabuleiro) - tamanhoFase:  # Não está na última linha
            pecaAbaixo = tabuleiro[_contador + tamanhoFase]
            if pecaAtual[2][1] and pecaAbaixo[0][1] and pecaConectada[_contador]:
                pecaConectada[_contador + tamanhoFase] = 1

    # Verifica se a peça final está conectada
    if pecaConectada[-1]:  # Última peça conectada
        return True
    return False

# Inicialização de variáveis
selected_piece_index = 0  # Índice da peça selecionada
contador = 0
x_inicial = x
y_inicial = y
tabuleiro = criarFase(tamanhoFase)  # Garante que tabuleiro seja inicializado no início do jogo
pecaConectada = [0] * (tamanhoFase ** 2)  # Inicializa as conexões das peças
movimentos = 0
jogo_terminado = False
mostrar_tabuleiro_fim = False
tempo_fim_jogo = 0  # Marca o tempo do fim do jogo

def verificarFimDeJogo():
    """Verifica se a última peça está conectada ao objetivo."""
    global jogo_terminado, mostrar_tabuleiro_fim, tempo_fim_jogo
    if pecaConectada[-1]:  # Última peça conectada
        if not jogo_terminado:
            mostrar_tabuleiro_fim = True
            tempo_fim_jogo = py.time.get_ticks()  # Marca o tempo atual
        jogo_terminado = True



def desenharTelaFinal():
    """Desenha a tela final com a contagem de movimentos e opção de reinício."""
    janela.fill((0, 0, 0))  # Fundo preto
    
    # Mensagem de vitória
    texto_vitoria = "Parabéns! Você completou o jogo!"
    formatacao_texto = fonte.render(texto_vitoria, True, (255, 255, 255))
    janela.blit(formatacao_texto, (j_largura // 2 - formatacao_texto.get_width() // 2, j_altura // 2 - 100))
    
    # Total de movimentos
    texto_movimentos = f"Movimentos totais: {movimentos}"
    formatacao_movimentos = fonte.render(texto_movimentos, True, (255, 255, 255))
    janela.blit(formatacao_movimentos, (j_largura // 2 - formatacao_movimentos.get_width() // 2, j_altura // 2))
    
    # Botão de reinício
    botao_reinicio = py.Rect(j_largura // 2 - 100, j_altura // 2 + 100, 200, 50)
    py.draw.rect(janela, (30, 144, 255), botao_reinicio)
    texto_reinicio = "Reiniciar"
    formatacao_reinicio = fonte.render(texto_reinicio, True, (0, 0, 0))
    janela.blit(formatacao_reinicio, (botao_reinicio.x + botao_reinicio.width // 2 - formatacao_reinicio.get_width() // 2, botao_reinicio.y + 10))
    
    py.display.update()
    return botao_reinicio

# Loop principal
while loop:
    if jogo_terminado:
        # Exibe o tabuleiro por 2 segundos antes de mostrar a tela final
        if mostrar_tabuleiro_fim:
            if py.time.get_ticks() - tempo_fim_jogo > 1000:  # 2000ms = 2 segundos
                mostrar_tabuleiro_fim = False  # Desativa a exibição do tabuleiro
            else:
                # Desenha o estado final do tabuleiro antes de mostrar a tela final
                desenharBackground()
                desenharInicio()
                desenharFim()
                desenharMovimentos()

                x_inicial = x
                y_inicial = y
                contador = 0
                for i in tabuleiro:
                    if contador != 0 and (contador % tamanhoFase) == 0:
                        y_inicial += tamanhoPeca * 3
                        x_inicial = x
                    cor_atual = azulClaro if pecaConectada[contador] else corPeca
                    desenharPecas(i, cor_atual, x_inicial, y_inicial, tamanhoPeca)

                    x_inicial += tamanhoPeca * 3
                    contador += 1
                
                py.display.update()
                continue  # Continua o loop até terminar o delay

        # Exibe a tela final
        botao_reinicio = desenharTelaFinal()
        for event in py.event.get():
            if event.type == py.QUIT:
                loop = False
            
            if event.type == py.MOUSEBUTTONDOWN:
                if botao_reinicio.collidepoint(event.pos):  # Clique no botão de reinício
                    # Reiniciar o jogo
                    movimentos = 0
                    pecaConectada = [0] * (tamanhoFase ** 2)
                    tabuleiro = criarFase(tamanhoFase)  # Reinicia o tabuleiro corretamente
                    jogo_terminado = False
        continue

    # Eventos do jogo
    for event in py.event.get():
        if event.type == py.QUIT:
            loop = False

        if event.type == py.KEYDOWN:
            # Movimentos e interações
            if event.key == py.K_RIGHT:
                movimentos += 1
                selected_piece_index = (selected_piece_index + 1) % len(tabuleiro)
            elif event.key == py.K_LEFT:
                movimentos += 1
                selected_piece_index = (selected_piece_index - 1) % len(tabuleiro)
            elif event.key == py.K_UP:
                movimentos += 1
                selected_piece_index = (selected_piece_index - tamanhoFase) % len(tabuleiro)
            elif event.key == py.K_DOWN:
                movimentos += 1
                selected_piece_index = (selected_piece_index + tamanhoFase) % len(tabuleiro)

            if event.key == py.K_SPACE:
                movimentos += 1
                rotacionarPecaSelecionada()
    
    # Atualizações do jogo
    desenharBackground()
    desenharInicio()
    desenharFim()
    desenharMovimentos()
    verificarConeccoes(tabuleiro)
    verificarFimDeJogo()  # Verificar se o jogo terminou

    # Desenhar peças
    x_inicial = x
    y_inicial = y
    contador = 0
    for i in tabuleiro:
        if contador != 0 and (contador % tamanhoFase) == 0:
            y_inicial += tamanhoPeca * 3
            x_inicial = x
        cor_atual = azulClaro if pecaConectada[contador] else corPeca
        desenharPecas(i, cor_atual, x_inicial, y_inicial, tamanhoPeca)

        # Destacar peça selecionada
        if contador == selected_piece_index:
            py.draw.rect(janela, (255, 0, 0), (x_inicial, y_inicial, tamanhoPeca * 3, tamanhoPeca * 3), 3)

        x_inicial += tamanhoPeca * 3
        contador += 1

    py.display.update()

py.quit()