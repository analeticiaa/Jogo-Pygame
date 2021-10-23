import pygame
from pygame.locals import * 
from sys import exit 
import os 
import random

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

fundo1 = os.path.join(diretorio_imagens, 'imagem_fundo.png')
fundo2 = os.path.join(diretorio_imagens, 'imagem_game_over.png')
fundo3 = os.path.join(diretorio_imagens, 'imagem_fundo_erro.png')
img_fundo = pygame.image.load(fundo1)
img_fundo2 = pygame.image.load(fundo2)
img_fundo3 = pygame.image.load(fundo3)


largura = 640
altura = 480

tela = pygame.display.set_mode((largura, altura))
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'imagens.png')).convert_alpha()

pygame.display.set_caption('Joguinho do Summaê')

# som da colisão
som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
# aumenta o volume
som_colisao.set_volume(1)

# som da pontuação
som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
# aumenta o volume
som_pontuacao.set_volume(1)

colidiu = False

pontos = 0
velocidade = 10


def exibe_texto(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado


class Batman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        #aumentar o volume
        self.som_pulo.set_volume(1)

        self.imagens_batman = []

        for i in range(3):
            img = sprite_sheet.subsurface((i*32,0),(32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_batman.append(img)

        self.index_lista = 0
        self.image = self.imagens_batman[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100,altura-70)

        self.pulo = False
        self.posicao_inicial_y = altura-70-48

    def pular(self):
        self.pulo = True
        self.som_pulo.play()


    def update(self):
        if self.pulo == True: 
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20

        else:
            if self.rect.y < altura-70-48:
                self.rect.y += 20
            else: self.rect.y = altura-70-48           

        if self.index_lista > 2: self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_batman[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        #self.rect.center = (100,100)
        # sortear posições aleatórias para as nuvens
        self.rect.y = random.randrange(50, 200, 50)
        self.rect.x = largura - random.randrange(30,300,90)

    # para a nuvem se movimentar horizontalmente
    def update(self):
        # se ultrapassar a borda esquerda da tela a posição x será igual a largura da tela
        if self.rect.topright[0] < 0:  
            self.rect.x = largura
            self.rect.y = random.randrange(50,200,50)
            
        self.rect.x -= 10


class Chao(pygame.sprite.Sprite):
    def __init__(self, posicao_x): 
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*6,32*2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 56
        self.rect.x = posicao_x * 60

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -=10


class Abacaxi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((4*32,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*4,32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (largura, altura-70)
        self.rect.x = largura
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= velocidade


todas_as_sprites = pygame.sprite.Group()

batman = Batman()
todas_as_sprites.add(batman)

# criar várias nuvens 
for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

# repetir o bloco do chão várias vezes
for i in range(largura//32):
    chao = Chao(i)
    todas_as_sprites.add(chao)

abacaxi = Abacaxi()
todas_as_sprites.add(abacaxi)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(abacaxi)


relogio = pygame.time.Clock()

clicou_errado = False

while True: 
    relogio.tick(30)
    # coloca imagem no fundo
    tela.blit(img_fundo,(0,0))
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:

            if colidiu == False: 
                if event.key == K_SPACE:
                    
                    if batman.rect.y != batman.posicao_inicial_y: pass
                    else: batman.pular()

            else:
                if event.key == K_c:   
                    pontos = 0
                    colidiu = False
                    velocidade = 10
                    abacaxi = Abacaxi()
                    grupo_obstaculos.add(abacaxi)
                    todas_as_sprites.add(abacaxi)
                    todas_as_sprites.update()
                    abacaxi.rect.center = (largura, altura-70)

                else: clicou_errado = True 
                

    colisoes = pygame.sprite.spritecollide(batman, grupo_obstaculos, True, pygame.sprite.collide_mask)
    
    todas_as_sprites.draw(tela)

   
   # se não ocorrer colissões atualiza as sprites
    if colisoes and colidiu == False: 
        som_colisao.play()
        colidiu = True

    if colidiu == True: 
        # exibir mensagem de Game Over 
        if clicou_errado == False:

            tela.blit(img_fundo2,(0,0))
        
            integral = "Para continuar jogando, digite o resultado de ∫{}xcos(x²)dx, substituindo o valor de x por 0".format(pontos)
            
            game_over = exibe_texto(integral, 12, (0,0,0))
            tela.blit(game_over, (largura/10, altura/1.3))

            if pontos % 100 == 0: pontos += 1 
        
        else: 
            tela.blit(img_fundo3, (0,0))
            pygame.display.update()
            pygame.time.delay(150)
            clicou_errado = False

    else: 
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_texto(pontos, 40, (25,25,112))

    tela.blit(texto_pontos, (520,30))
    
    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade >= 23: velocidade += 1

    pygame.display.flip()
