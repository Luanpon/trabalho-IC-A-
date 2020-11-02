import pygame
import sys

# matrizGrade : matriz que representa a grade por onde a tartaruga anda.
# 0 indica quadrado em branco pelo qual a tartaruga pode andar
# 1 indica a posicao inicial da tartaruga
# 2 indica a posicao da minhoca
# 3 indica um obstaculo
matrizGrade = [
    [3,0,0,0,0,3],
    [0,0,3,3,0,0],
    [0,3,3,1,3,2],
    [0,0,0,0,3,0]
]

matrizPosicoes = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
]

pygame.init()

tamanhoTela = largura, altura = 700, 500

tela = pygame.display.set_mode(tamanhoTela)

tartaruga = pygame.image.load('tartaruga.png')
minhoca = pygame.image.load('minhoca.png')

tartaruga = pygame.transform.scale(tartaruga, (90, 90))
minhoca = pygame.transform.scale(minhoca, (90, 90))

def existe(i,j):

    try:
        if i<0 or j<0:
            return False

        else:
            matrizGrade[i][j] = matrizGrade[i][j]
            return True

    except:
        return False

def indice_lista(lista,valor):

    try:
        return lista.index(valor)
    except:
        return -1

def calcula_caminho():

    listaAberta = []
    listaFechada = []
    posicaoInicialTartaruga = []
    posicaoMinhoca = []
    matrizA = []
    celula = 0
    caminhoEncontrado = None
    celulaAtualX = -1
    celulaAtualY = -1

    for i in range(len(matrizGrade)):

        matrizA.append([])

        for j in range(len(matrizGrade[i])):

            x = matrizPosicoes[i][j][0]
            y = matrizPosicoes[i][j][1]

            if matrizGrade[i][j] == 1:
                posicaoInicialTartaruga = [i,j]
                matrizA[i].append({"celula": celula, "pai": None, "f": None, "g": None, "h": None,
                                   "tipo": "inicio", "i": i, "j": j, "x": x, "y": y})
            elif matrizGrade[i][j] == 2:
                posicaoMinhoca = [i,j]
                matrizA[i].append({"celula": celula, "pai": None, "f": None, "g": None, "h": None,
                                   "tipo": "fim", "i": i, "j": j, "x": x, "y": y})
            elif matrizGrade[i][j] == 3:
                matrizA[i].append({"celula": celula, "pai": None, "f": None, "g": None, "h": None,
                                   "tipo": "bloco", "i": i, "j": j, "x": x, "y": y})
            else:
                matrizA[i].append({"celula": celula, "pai": None, "f": None, "g": None, "h": None,
                                   "tipo": "normal", "i": i, "j": j, "x": x, "y": y})

            celula += 1

    while caminhoEncontrado == None:

        if celulaAtualX==-1 and celulaAtualY==-1:
            celulaAtualX = posicaoInicialTartaruga[0]
            celulaAtualY = posicaoInicialTartaruga[1]

        vizinhos = [
            [celulaAtualX - 1, celulaAtualY],
            [celulaAtualX + 1, celulaAtualY],
            [celulaAtualX, celulaAtualY - 1],
            [celulaAtualX, celulaAtualY + 1]
        ]

        for vizinho in vizinhos:

            vizinhoX = vizinho[0]
            vizinhoY = vizinho[1]

            if existe(vizinhoX,vizinhoY):
                if matrizGrade[vizinhoX][vizinhoY] != 3 and matrizGrade[vizinhoX][vizinhoY] != 1 and indice_lista(listaFechada,matrizA[vizinhoX][vizinhoY]) < 0 and indice_lista(listaAberta, matrizA[vizinhoX][vizinhoY]) < 0:

                    matrizA[vizinhoX][vizinhoY]["pai"] = matrizA[celulaAtualX][celulaAtualY]["celula"]
                    matrizA[vizinhoX][vizinhoY]["g"] = abs(vizinhoX-posicaoInicialTartaruga[0]) + abs(vizinhoY-posicaoInicialTartaruga[1])
                    matrizA[vizinhoX][vizinhoY]["h"] = abs(vizinhoX-posicaoMinhoca[0]) + abs(vizinhoY-posicaoMinhoca[1])
                    matrizA[vizinhoX][vizinhoY]["f"] = matrizA[vizinhoX][vizinhoY]["g"] + matrizA[vizinhoX][vizinhoY]["h"]
                    listaAberta.append(matrizA[vizinhoX][vizinhoY])

                    if matrizA[vizinhoX][vizinhoY]["tipo"] == "fim":
                        caminhoEncontrado = True

        if len(listaAberta) > 0:
            listaAberta = sorted(listaAberta, key=lambda k: k['f'])
            celulaAtualX = listaAberta[0]["i"]
            celulaAtualY = listaAberta[0]["j"]
            print(listaAberta)
            listaFechada.append(listaAberta[0])
            listaAberta.remove(listaAberta[0])
        else:
            caminhoEncontrado = False

    print('caminho econtrado?: ',caminhoEncontrado)
    caminho = [ matrizA[posicaoMinhoca[0]][posicaoMinhoca[1]] ]
    while 1:

        for i in range(len(matrizGrade)):
            for j in range(len(matrizGrade[i])):

                if matrizA[i][j]["celula"] == caminho[0]["pai"]:
                    caminho.insert(0,matrizA[i][j])
                    break

        if caminho[0]["pai"] == None:
            break

    for c in caminho:
        print(c)
    return [caminhoEncontrado,caminho]

def desenha_grade():

    # posicoes
    x = 0
    y = 0

    # iteradores
    i = 0
    j = 0

    while y < 400:

        while x < 600:

            if matrizGrade[i][j] == 3:
                pygame.draw.rect(tela, (0, 0, 255), (x, y, 100, 100))
            else:
                pygame.draw.rect(tela, (0, 0, 0), (x, y, 100, 100), 2)

            matrizPosicoes[i][j] = [x + 5, y + 5]

            if matrizGrade[i][j] == 2:
                tela.blit(minhoca,(x+5,y+5))

            x += 100
            j += 1

        y += 100
        i += 1

        x = 0
        j = 0

def animacao(caminho):


    tela.fill((255, 255, 255))
    desenha_grade()


def principal():

    k = 1
    Xatual = -1
    Yatual = -1
    Xdestino = -1
    Ydestino = -1

    desenha_grade()

    while 1:

        calculaCaminho = calcula_caminho()
        caminhoEncontrado = calculaCaminho[0]
        caminho = calculaCaminho[1]

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if caminhoEncontrado:
                if Xatual==-1 and Yatual==-1:
                    Xatual = caminho[0]["x"]
                    Yatual = caminho[0]["y"]

            if caminhoEncontrado:

                if k<len(caminho):
                    Xdestino = caminho[k]["x"]
                    Ydestino = caminho[k]["y"]
                else:
                    Xatual = -1
                    Yatual = -1
                    k = 1
                    break

            if caminhoEncontrado:

                if Xatual<Xdestino:
                    tela.fill((255, 255, 255))
                    desenha_grade()
                    tela.blit(tartaruga,(Xatual,Yatual))
                    Xatual += 5
                elif Xatual>Xdestino:
                    tela.fill((255, 255, 255))
                    desenha_grade()
                    tela.blit(tartaruga,(Xatual,Yatual))
                    Xatual -= 5
                elif Yatual<Ydestino:
                    tela.fill((255, 255, 255))
                    desenha_grade()
                    tela.blit(tartaruga, (Xatual, Yatual))
                    Yatual += 5
                elif Yatual>Ydestino:
                    tela.fill((255, 255, 255))
                    desenha_grade()
                    tela.blit(tartaruga, (Xatual, Yatual))
                    Yatual -= 5
                else:
                    k += 1

            if caminhoEncontrado == False:
                tela.fill((255, 255, 255))
                desenha_grade()
                for i in range(len(matrizGrade)):
                    for j in range(len(matrizGrade[i])):
                        if matrizGrade[i][j] == 1:
                            tela.blit(tartaruga,(matrizPosicoes[i][j][0],matrizPosicoes[i][j][1]))

            pygame.display.update()
            pygame.time.Clock().tick(30)


principal()
