# used modules
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
from numpy.core.numeric import full
from EasyROI import EasyROI  
import json
from src.logger import writeLog
from src.utils import printScreen
from src.utils import get_project_root,sendMsgTelegram
from src.mouse import moveTo,mouseClick,ctrlF5,scrollTo,ctrlShiftR,mouseMoveClick
from time import sleep



# Definição de variáveis
roi_helper = EasyROI(verbose=False)  
i = 0 
heroisEncontrados=[{"raridade":"comum","qnt":"0"},
           {"raridade":"raro","qnt":"0"},
           {"raridade":"super_raro","qnt":"0"},
           ]

stageLogin = "Login"
stagePrincipal = "Principal"
stageMapa = "Mapa"
stageNewMap = "Novo Mapa"
stageError = "Tela de Erro"
stageHeroSelect = "Tela de Heróis"
stageLoading = "Tela de Carregamento"
sumChest_BrownSealed = 0
sumChest_PurpleSealed = 0
scaleResize = 50
mapStatus = "Inicio"


def imageSearch(jpg,source="cropped",extraImg='',threshold=0.7,ignoreRescale=False):
    root = get_project_root()
    targetJpg = str(root) + "/imgs/" + jpg
    target = cv2.imread(targetJpg)
    global scaleResize
    if (scaleResize != 100 and ignoreRescale==False):
        targetWidth = int(target.shape[1] * scaleResize / 100)
        targetHeight = int(target.shape[0] * scaleResize / 100)
        dim = (targetWidth, targetHeight)
        target = cv2.resize(target,dim, interpolation = cv2.INTER_AREA)
        
    if (source == "cropped"):
        source = imgCropped
    elif(source=="extra"):
        source=extraImg
    else:
        source = printScreen()
        
    

    result = cv2.matchTemplate(target,source,cv2.TM_CCOEFF_NORMED)
    y,x = np.unravel_index(result.argmax(), result.shape)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def returnImageData(jpg):
    root = get_project_root()
    targetJpg = str(root) + "/imgs/" + jpg
    target = cv2.imread(targetJpg)
    height, width, channels = target.shape 
    return height, width, channels 

def searchAndUniqueClick(cropX,cropY,img,extraImg=[],threshold=0.7,ignoreRescale=False):
    if (len(extraImg) >0):
        result = imageSearch(img,"extra",extraImg,threshold,ignoreRescale=ignoreRescale)
    else:
        result = imageSearch(img,ignoreRescale=ignoreRescale)
    
    if (len(result)>0):
        x,y,w,h = result[len(result)-1]
        mouseMoveClick(x,y,w,h,cropX,cropY)
        return True
    else:
        return False

def searchAndMultipleClick(cropX,cropY,img,ignoreRescale=False):
    result = imageSearch(img,ignoreRescale=ignoreRescale)
    if (len(result)>0):
        for x,y,w,h in result:
            mouseMoveClick(x,y,w,h,cropX,cropY)
            
            sleep(1)
        return True
    else:
        return False


def countFoundImages(cropX,cropY,img):
    result = imageSearch(img)
    return len(result)

def loginApp(cropX,cropY):
    result = searchAndUniqueClick(cropX,cropY,"btn_connect_wallet.jpg")
    if (result):
        sleep(5)
        attempts = 0
        while attempts < 20:
            result = imageSearch("btn_assinar.png","full",ignoreRescale=True)
            if (len(result) > 0):
                for x,y,w,h in result:
                    center_x = x + int(w/2) 
                    center_y = y + int(h/2) 
                    moveTo(center_x,center_y)
                    mouseClick()
                break
            sleep(0.5)
            attempts+=1
        
def countChests(cropX,cropY):
    sealedBlueChests= countFoundImages(cropX,cropY,"bau_azul_lacrado.jpg")
    sealedGoldChests = countFoundImages(cropX,cropY,"bau_dourado_lacrado.jpg")
    sealedBrownChests = countFoundImages(cropX,cropY,"bau_marrom_lacrado.png")
    sealedPurpleChests = countFoundImages(cropX,cropY,"bau_roxo_lacrado.jpg")
    return sealedBlueChests,sealedGoldChests,sealedBrownChests,sealedPurpleChests

def countBreakableRocks(cropX,cropY):
    breakableBrownRocks = countFoundImages(cropX,cropY,"pedra_marrom.png")
    breakableGoldRocks = countFoundImages(cropX,cropY,"pedra_amarela.png")
    breakableBricks = countFoundImages(cropX,cropY,"tijolo.jpg")
    return breakableBrownRocks,breakableGoldRocks, breakableBricks

def countUnbreakableRocks(cropX,cropY):
    obstacle1 = countFoundImages(cropX,cropY,"obstacle1.png")
    obstacle2 = countFoundImages(cropX,cropY,"obstacle2.png")
    obstacle3 = countFoundImages(cropX,cropY,"obstacle3.png")
    obstacle4 = countFoundImages(cropX,cropY,"obstacle4.png")
    
    return obstacle1,obstacle2, obstacle3, obstacle4

def countJails(cropX,cropY):
    jaulas = countFoundImages(cropX,cropY,"jaula_lacrada.jpg")
    return jaulas

def analyseBcoinsExpectation(cropX,cropY):
    sealedBlueChests,sealedGoldChests,sealedBrownChests,sealedPurpleChests = countChests(cropX,cropY)
    global sumChest_BrownSealed
    global sumChest_PurpleSealed
    sumChest_BrownSealed = sealedBrownChests
    sumChest_PurpleSealed = sealedPurpleChests
    breakableBrownRocks,breakableGoldRocks,breakableBricks = countBreakableRocks(cropX,cropY)
    jaulas = countJails(cropX,cropY)
    print ("Azuis: " + str(sealedBlueChests))
    print ("Dourados: " + str(sealedGoldChests))
    print ("Marrons: " + str(sealedBrownChests))
    print ("Roxos: " + str(sealedPurpleChests))
    print ("Pedras Marrons: " + str(breakableBrownRocks))
    print ("Pedras Douradas: " + str(breakableGoldRocks))
    print ("breakableBricks: " + str(breakableBricks))
    print ("Jaulas: " + str(jaulas))

def situacaoMapa(cropX,cropY):
    smallLifeBrownChests = countFoundImages(cropX,cropY,"bau_marrom_pouca_vida.png")
    halfLifeBrownChests = countFoundImages(cropX,cropY,"bau_marrom_pouca_vida.png")
    global mapStatus
    if (smallLifeBrownChests > halfLifeBrownChests):
        mapStatus='Início'
    else:
        mapStatus='Fim'
    
def refreshPrint(cropX,cropY):
    imgPrintScreen = printScreen()
    y = cropY
    x = cropX
    global imgCropped
    global brX
    global brY
    imgCropped = imgPrintScreen[y:brY,x: brX]
    
def refreshHerois(cropX,cropY):
    try:
        result = searchAndUniqueClick(cropX,cropY,str(scaleResize) + "/btn_voltar.jpg",ignoreRescale=True)
        if (result):
            i=0
            while i<10:
                refreshPrint(cropX,cropY)
                result = searchAndUniqueClick(cropX,cropY,"img_central_tesouro.jpg")
                if (result):
                    break
                else:
                    sleep(2)
                    i+=1
    except:
        pass

def enableHeroesWithGreenBar(cropX,cropY,imgParam):
    writeLog("Buscando heróis que estejam com a barra de vida na cor verde")
    attempts = 0 
    result = []
    while (len(result) == 0 and attempts < 5):
            refreshPrint(cropX,cropY)
            result = imageSearch(imgParam,threshold=0.75,ignoreRescale=True)
            if (len(result) == 0):
                sleep(5)
                attempts+=1
    for x,y,w,h in result:
        try:
            #recortar quadrado herói
            height, width, channels = returnImageData(imgParam)
            #heighIconHeroBarResized = int((height * scaleResize) / 100)
            wResized = int((580*scaleResize) / 100)
            #qbrY = y+heighIconHeroBarResized
            qbrY = y + height
            boxHero = imgCropped[y:qbrY, x:wResized]
            result2 = imageSearch(str(scaleResize) + "/barra_verde.png","extra",boxHero,0.75,ignoreRescale=True)
            #cv2.imshow("box",boxHero)
            #cv2.waitKey()
            if(len(result2)>0):
                print("Identificado. Colocando funcionário para trabalhar.")
                searchAndUniqueClick(cropX+x, cropY+y,str(scaleResize) + "/btn_work.png",boxHero,0.90,ignoreRescale=True)
                sleep(1)
        except cv2.error as e:
            for k in dir(e):
                #if k[0:2] != "__":
                 #   print("e.%s = %s" % (k, getattr(e, k)))

                # handle error: empty frame
                if e.err == "_img.size().height <= _templ.size().height && _img.size().width <= _templ.size().width":
                    pass
            
        

def heroesTeam(cropX,cropY):
    sleepAllHeroes(cropX,cropY)
    sleep(1)
    searchAndUniqueClick(cropX,cropY,str(scaleResize) + "/btn_fechar.png",ignoreRescale=True)
    sleep(1)
    refreshPrint(cropX,cropY)
    searchAndUniqueClick(cropX,cropY,"heroi_icone.png")
    sleep(1)
    #refreshPrint(cropX,cropY)
    i=0
    #refreshPrint(cropX,cropY)
    writeLog("Formando times")
    while (i<4):
        enableHeroesWithGreenBar(cropX,cropY,str(scaleResize) + "/barra_inicio_heroi_selecionado.png")
        enableHeroesWithGreenBar(cropX,cropY,str(scaleResize) + "/barra_inicio_heroi.png")

        #for key in jsonObject:
        #    raridade = key['raridade']
        #    qnt = int(key['qnt'])
        #    result2 = imageSearch(raridade+"_verde.png",boxHero,0.85)
        #    soma = 0
        #    for x,y,w,h in result2:
        #            soma +=1
        #    key['qnt'] = int(qnt) + int(soma)
        #    print(key['raridade'] + " " + str(key['qnt']))
        writeLog("Procurando mais heróis")
        resultScroll = imageSearch(str(scaleResize) + "/entre_herois.png",threshold=0.75)
        if (len(resultScroll) > 0):
            xScroll,yScroll,wScroll,hScroll = resultScroll[len(resultScroll)-1]
            heighScroll = int((280 * scaleResize) / 100)
            scrollTo((xScroll+cropX),(yScroll+cropY),(cropY+yScroll)-heighScroll)
            sleep(3)
        i+=1
    #print(heroisEncontrados)
    


def sleepAllHeroes(cropX,cropY):
    refreshPrint(cropX,cropY)
    result = imageSearch(str(scaleResize) + "/btn_all_descansar.png", ignoreRescale=True, threshold=0.70)
    if (len(result)>0):
        writeLog("Colocando todos os heróis pra dormirem")
        x,y,w,h = result[len(result)-1]
        mouseMoveClick(x,y,w,h,cropX,cropY)
        sleep(3)

def workAllHeroes(cropX,cropY):
    while True:
        refreshPrint(cropX,cropY)
        result = searchAndUniqueClick(cropX,cropY,str(scaleResize) + "/btn_all_trabalhar.png")
        if (result):
            return False
        else:
            sleep(2)
    
    

def findStage(cropX,cropY):
    refreshPrint(cropX,cropY)
    result = imageSearch("btn_connect_wallet.jpg")
    if (len(result)>0):
        return stageLogin
    result = imageSearch("img_central_tesouro.jpg")
    if (len(result)>0):
        return stagePrincipal
    result = imageSearch("btn_new_map.jpg")
    if (len(result)>0):
        return stageNewMap
    result = imageSearch("btn_ok.jpg")
    if (len(result)>0):
        return stageError
    result = imageSearch("tela_herois.png")
    if (len(result)>0):
        return stageHeroSelect
    obstacle1,obstacle2,obstacle3,obstacle4 = countUnbreakableRocks(cropX,cropY)
    if ((obstacle1>0) or (obstacle2>0) or (obstacle3>0) or (obstacle4>0)):
        return stageMapa
    result = imageSearch("bombcrypto_logo.png")
    if (len(result)>0):
        return stageLoading
    
  
def workFlow(cropX,cropY):
    count=0
    concluido = False
    temporizador = 3
    countStuckStage = 0
    while concluido == False:
        try: 
            writeLog("Identificando posição no workFlow")
            stage = findStage(cropX,cropY)
            
            writeLog("Estamos na tela: " + str(stage))
            imgPrintScreen = printScreen()

            if (stage==stageLogin):
                writeLog("Fazendo login no sistema...")
                loginApp(cropX,cropY)
                temporizador = 20   
            elif (stage==stagePrincipal):
                writeLog("Clicando no ícone de heróis")
                searchAndUniqueClick(cropX,cropY,"heroi_icone.png")
            elif(stage==stageMapa):
                #writeLog("Verificando situação do mapa e voltando para a tela inicial")
                #refreshHerois(cropX,cropY)
                #situacaoMapa(cropX,cropY)
                searchAndUniqueClick(cropX,cropY,str(scaleResize) + "/btn_voltar.jpg",ignoreRescale=True)
            elif(stage==stageNewMap):
                writeLog("Clicando no botão de novo mapa")
                searchAndUniqueClick(cropX,cropY,"btn_new_map.jpg")
                temporizador = 5
            elif(stage==stageHeroSelect):
                heroesTeam(cropX,cropY)
                searchAndUniqueClick(cropX,cropY,str(scaleResize) + "/btn_fechar.png",ignoreRescale=True)
                sleep(2)
                refreshPrint(cropX,cropY)
                resultMapa = imageSearch("img_central_tesouro.jpg")
                if (len(resultMapa)>0):
                    writeLog("Iniciando o mapa")
                    x,y,w,h = resultMapa[len(resultMapa)-1]
                    mouseMoveClick(x,y,w,h,cropX,cropY)
                    concluido = True
                    countStuckStage =0 
                    break
                else:
                    writeLog("Não foi possível iniciar o mapa.")
                    countStuckStage +=1
                    temporizador = 5

    
                if (countStuckStage > 3):
                    print("Provavelmente estamos em um looping. Vou atualizar a página.")
                    mouseMoveClick(0,0,0,0,cropX,cropY)
                    ctrlShiftR()
                    countStuckStage = 0
                    
                    
            elif(stage==stageError):
                writeLog("Erro detectado. Atualizando a página.",tipo="error")
                mouseMoveClick(0,0,0,0,cropX,cropY)
                ctrlF5()
                temporizador=30
            elif(stage==stageLoading):
                writeLog("Aguardando carregamento...")
                temporizador=20
            elif(stage==None):
                count +=1
                if(count==5):
                    writeLog("Nenhuma tela encontrada. Atualizando a página.",tipo="error")
                    mouseMoveClick(0,0,0,0,cropX,cropY)
                    ctrlF5()
                    temporizador=30
                    count=0
            else:
                count=0
            
            sleep(temporizador)
            #writeLog("Atualizando o print da tela.")
            y = cropY
            x = cropX
            global imgCropped
            imgCropped = imgPrintScreen[y:brY,x: brX]
        except Exception as e:
            writeLog("Erro detectado." + str(e) + " Atualizando a página.",tipo="error")
            ctrlF5()
            
def createAccountUntilFindJailMode():
    #cria nova carteira
    global imgPrintScreen
    jaulas = 0
    while jaulas == 0:
        #atualiza ignorando o cache
        imgPrintScreen = printScreen()
        writeLog("Limpa o cache")
        result = imageSearch("btn_clear_site_data.png","full")
        if (len(result)>0):
            x,y,w,h = result[len(result)-1]
            mouseMoveClick(x,y,w,h,0,0)
        
        writeLog("Atualiza página")
        result = imageSearch("bombcrypto_logo.png","full")
        if (len(result)>0):
            x,y,w,h = result[len(result)-1]
            mouseMoveClick(x,y,w,h,0,0)
            ctrlShiftR()
        else:
            result = imageSearch("btn_voltar.jpg","full")
            if (len(result)>0):
                x,y,w,h = result[len(result)-1]
                mouseMoveClick(x,y,w,h,0,0)
                ctrlShiftR()
        
       
        #clica no ícone da metamask
        imgPrintScreen = printScreen()
        writeLog("Abrir metamask")
        result = imageSearch("metamask.png","full")
        if (len(result)>0):
            x,y,w,h = result[len(result)-1]
            mouseMoveClick(x,y,w,h,0,0)
            sleep(2)
            imgPrintScreen = printScreen()
            #clica no ícone pra abrir as opções
            writeLog("Clica no ícone")
            result = imageSearch("metamask_binancesmartchain.png","full")
            if (len(result) > 0):
                x,y,w,h = result[len(result)-1]
                mouseMoveClick(x+100,y,w,h,0,0)
                sleep(2)
                imgPrintScreen = printScreen()
                #clica pra abrir a conta
                writeLog("Criar conta")
                result = imageSearch("metamask_criar_conta.png","full")
                if (len(result) > 0):
                    x,y,w,h = result[len(result)-1]
                    mouseMoveClick(x+100,y,w,h,0,0)
                    sleep(2)
                    imgPrintScreen = printScreen()
                    writeLog("Confirmar criação de conta")
                    result = imageSearch("btn_criar.png","full")
                    if (len(result) > 0):
                        x,y,w,h = result[len(result)-1]
                        mouseMoveClick(x,y,w,h,0,0)
                        result = [] 
                        while (len(result) == 0):
                            imgPrintScreen = printScreen()
                            #clica pra criar a conta
                            writeLog("Botão não conectado")
                            result = imageSearch("btn_nao_conectado.png","full")
                            sleep(5)
                        if (len(result) > 0):
                            x,y,w,h = result[len(result)-1]
                            mouseMoveClick(x,y,w,h,0,0)
                            sleep(3)
                            imgPrintScreen = printScreen()
                            #clica pra criar a conta
                            writeLog("Conectar")
                            result = imageSearch("btn_conectar.png","full")
                            if (len(result) > 0):
                                x,y,w,h = result[len(result)-1]
                                mouseMoveClick(x,y,w,h,0,0)
                                sleep(5)                        
                                achados = foundAccounts()
                                if (len(achados)>0):
                                    for x,y,w,h in achados:
                                        global scaleResize
                                        spaceGreenLineUntilButton = int((942 * scaleResize) / 100)
                                        spaceBetweenButtonAndLine = int((20 * scaleResize) / 100)
                                        
                                        w = w+spaceBetweenButtonAndLine+spaceGreenLineUntilButton
                                        x = x - spaceGreenLineUntilButton
                                        # 632 é a altura fixa - o botão
                                        fixedHeightMinusButton = int((620 * scaleResize) / 100)
                                        h = int(h)+fixedHeightMinusButton
                                        y = y-fixedHeightMinusButton
                                        #print(x,y,w,h)
                                        global brX
                                        global brY
                                        brX = x+w
                                        brY = y+h
                                        imgPrintScreen = printScreen()
                                        global imgCropped
                                        imgCropped = imgPrintScreen[y:brY, x:brX]
                                        writeLog("Conectar carteira")
                                        loginApp(x,y,False)
                                        sleep(10)
                                        refreshPrint(x,y)
                                        result = searchAndUniqueClick(x,y,"img_central_tesouro.jpg")
                                        sleep(2)
                                        refreshPrint(x,y)
                                        jaulas = countJails(x,y)
                                        print("Jaulas encontradas: " + str(jaulas))
    writeLog("Jaula Encontrada!")
    sendMsgTelegram("Jaula encontrada")


def foundAccounts():
    foundFooter = imageSearch("btn_expandir.png","full")
    return foundFooter
    

def main():
    manualCutScreen = False
    # Printscreen da tela
    global imgPrintScreen
    imgPrintScreen = printScreen()
    global imgCropped
    global brX,brY
    # Manual ou Automático?
    #createAccountUntilFindJailMode()
    if (manualCutScreen):
        # Permite ao usuário desenhar os limites das telas
        # Especifica quantas telas
        numberOfAccounts = int(input("Quantas telas serão captadas?"))
        print("Agora você precisa desenhar na tela o espaço de cada uma da(s) " + str(numberOfAccounts) + " tela(s).") 
        roi = roi_helper.draw_rectangle(imgPrintScreen, quantity=numberOfAccounts)  
        i=0 
        jsonObjectDump = json.dumps(roi)
        jsonObject = json.loads(jsonObjectDump)
        while i < numberOfAccounts:
            params = jsonObject['roi']['' + str(i) + '']
            brX = int(params['br_x'])
            brY = int(params['br_y'])
            y = int(params['tl_y'])
            x = int(params['tl_x'])
            h = int(params['h'])
            w = int(params['w'])
            imgCropped = imgPrintScreen[y:brY, x:brX]
            #cv2.imshow("Image",crop)
            #cv2.waitKey(0)
            workFlow(x,y)
            i+=1
    else:
        while True:
            achados = foundAccounts()
            print("Iniciando varredura. Quantidade de contas achadas: " + str(len(achados)))
            if (len(achados)>0):
                for x,y,w,h in achados:
                    # 20 = espaço entre o botão e a linha verde lateral
                    # 942 = é o espaço que restou entre a linha verde esquerda até o botão
                    global scaleResize
                    spaceGreenLineUntilButton = int((942 * scaleResize) / 100)
                    spaceBetweenButtonAndLine = int((20 * scaleResize) / 100)
                    
                    w = w+spaceBetweenButtonAndLine+spaceGreenLineUntilButton
                    x = x - spaceGreenLineUntilButton
                    # 632 é a altura fixa - o botão
                    fixedHeightMinusButton = int((620 * scaleResize) / 100)
                    h = int(h)+fixedHeightMinusButton
                    y = y-fixedHeightMinusButton
                    #print(x,y,w,h)
                    brX = x+w
                    brY = y+h
                    imgCropped = imgPrintScreen[y:brY, x:brX]
                    #cv2.namedWindow("crop")        # Create a named window
                    #cv2.moveWindow("crop", 300,300)
                    #cv2.imshow("crop",imgCropped)
                    #cv2.waitKey()
                    workFlow(x,y)
            print("Telas percorridas. Descansando.")
            sleep(300)
    
if __name__ == '__main__' :
    main()
    

    
        
        
