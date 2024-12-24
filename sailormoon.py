'''Discente: Kalyne Rodrigues de Melo  Matrícula: 20232014050032
    Discente: Thayna Bittencourt Baima  Matrícula: 20241014050030'''

import pygame  # Importa o Pygame para a criação do jogo
import os  # Módulo para manipulação de arquivos e pastas no sistema
import random  # Módulo para gerar números aleatórios (usado para a altura dos canos)

# Configurações da tela do jogo (largura e altura em pixels)
TELA_LARGURA = 500
TELA_ALTURA = 800

# Carregando e dimensionando as imagens usadas no jogo
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_SAILORMOON = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'sailormoon1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'sailormoon2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'sailormoon3.png'))),
]  # Três imagens para animar o personagem Sailor Moon

pygame.font.init()  # Inicializa o sistema de fontes do Pygame
# Definindo as fontes utilizadas no jogo
FONTE_GAME_OVER = pygame.font.Font(os.path.join('fonts', 'Sailor-Stitch.ttf'), 40)
FONTE_PONTOS = pygame.font.Font(os.path.join('fonts', 'Sailor-Stitch.ttf'), 30)
FONTE_PRESSIONAR_ESPACO_GO = pygame.font.Font(os.path.join('fonts', 'Sailor-Stitch.ttf'), 10)
FONTE_INICIO = pygame.font.Font(os.path.join('fonts', 'Sailor-Stitch.ttf'), 20)  # Fonte usada na tela inicial

# Classe que representa o personagem Sailor Moon
class Sailor:
    IMGS = IMAGENS_SAILORMOON  # Carrega a lista de imagens para animar o personagem
    ROTACAO_MAXIMA = 25  # Rotação máxima para a frente
    VELOCIDADE_ROTACAO = 20  # Velocidade com que a Sailor Moon rotaciona enquanto cai
    TEMPO_ANIMACAO = 5  # Tempo de animação para as asas se movimentarem

    def __init__(self, x, y):
        self.x = x  # Posição inicial no eixo X
        self.y = y  # Posição inicial no eixo Y
        self.angulo = 0  # Ângulo inicial do personagem
        self.velocidade = 0  # Velocidade vertical inicial
        self.altura = self.y  # Armazena a altura atual do personagem
        self.tempo = 0  # Controla o tempo de movimento
        self.contagem_imagem = 0  # Controla a troca das imagens para animação
        self.imagem = self.IMGS[0]  # Define a primeira imagem da animação

    # Função que faz o personagem "pular"
    def pular(self):
        self.velocidade = -10.5  # Define a velocidade para cima (negativo no eixo Y)
        self.tempo = 0  # Reseta o tempo
        self.altura = self.y  # Salva a altura atual

    # Função que move a Sailor Moon
    def mover(self):
        # Calcula o deslocamento baseado na física do jogo
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Limita o deslocamento para que não seja muito rápido
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2  # Aumenta a subida

        self.y += deslocamento  # Atualiza a posição Y

        # Ajusta o ângulo do personagem dependendo se está subindo ou caindo
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA  # Inclina para frente quando está subindo
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO  # Inclina para trás quando está caindo

    # Função que desenha a Sailor Moon na tela
    def desenhar(self, tela):
        self.contagem_imagem += 1 

        # Alterna as imagens para criar a animação
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]  # cima
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]  # meio
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]  # baixo
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]  # meio
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]  # Reseta a animação
            self.contagem_imagem = 0

        # Se a Sailor Moon estiver caindo, a imagem fica fixa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # Rotaciona a imagem conforme o ângulo e desenha na tela
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # Função para pegar a máscara do personagem, usada para detectar colisões
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Classe que representa os canos (obstáculos)
class Cano:
    DISTANCIA = 250  # Distância entre os canos superior e inferior
    VELOCIDADE = 5  # Velocidade com que os canos se movem

    def __init__(self, x):
        self.x = x  # Posição inicial do cano no eixo X
        self.altura = 0  # Altura inicial do cano
        self.pos_topo = 0  # Posição do topo do cano
        self.pos_base = 0  # Posição da base do cano
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)  # Inverte a imagem para criar o cano de cabeça para baixo
        self.CANO_BASE = IMAGEM_CANO  # Imagem do cano de baixo
        self.passou = False  # Indica se o personagem já passou pelo cano
        self.definir_altura()

    # Função que define uma altura aleatória para os canos
    def definir_altura(self):
        self.altura = random.randrange(50, 450)  # Define uma altura aleatória
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()  # Calcula a posição do cano superior
        self.pos_base = self.altura + self.DISTANCIA  # Calcula a posição do cano inferior

    # Função que move os canos para a esquerda
    def mover(self):
        self.x -= self.VELOCIDADE  # Move o cano para a esquerda

    # Função que desenha os canos na tela
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))  # Desenha o cano superior
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))  # Desenha o cano inferior

    # Função que verifica colisão entre Sailor Moon e os canos
    def colidir(self, sailor):
        sailor_mask = sailor.get_mask()  # Pega a máscara da Sailor Moon
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)  # Máscara do cano superior
        base_mask = pygame.mask.from_surface(self.CANO_BASE)  # Máscara do cano inferior

        # Calcula as distâncias para verificar sobreposição (colisão)
        distancia_topo = (self.x - sailor.x, self.pos_topo - round(sailor.y))
        distancia_base = (self.x - sailor.x, self.pos_base - round(sailor.y))

        topo_ponto = sailor_mask.overlap(topo_mask, distancia_topo)
        base_ponto = sailor_mask.overlap(base_mask, distancia_base)

        # Retorna True se houver colisão com qualquer um dos canos
        return base_ponto or topo_ponto

# Classe que representa o chão do jogo
class Chao:
    VELOCIDADE = 5  # Velocidade de movimentação do chão
    LARGURA = IMAGEM_CHAO.get_width()  # Largura da imagem do chão
    IMAGEM = IMAGEM_CHAO  # Imagem do chão

    def __init__(self, y):
        self.y = y  # Posição do chão no eixo Y
        self.x1 = 0  # Primeira parte do chão
        self.x2 = self.LARGURA  # Segunda parte do chão

    # Função que move o chão para a esquerda
    def mover(self):
        self.x1 -= self.VELOCIDADE  # Move a primeira parte do chão
        self.x2 -= self.VELOCIDADE  # Move a segunda parte do chão

        # Reposiciona o chão quando ele sai da tela
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    # Função que desenha o chão na tela
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))  # Desenha a primeira parte do chão
        tela.blit(self.IMAGEM, (self.x2, self.y))  # Desenha a segunda parte do chão

# Função que desenha todos os elementos na tela
def desenhar_tela(tela, sailor, canos, chao, pontos, game_started, game_over):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))  # Desenha o fundo do jogo

    if game_over:
        # Exibe a mensagem de Game Over e a pontuação final
        texto_game_over = FONTE_GAME_OVER.render("GAME OVER", 1, (255, 0, 0))
        tela.blit(texto_game_over, (TELA_LARGURA // 2 - texto_game_over.get_width() // 2, TELA_ALTURA // 2 - 100))
        texto_pontuacao_final = FONTE_PONTOS.render(f"Score: {pontos}", 1, (255, 255, 255))
        tela.blit(texto_pontuacao_final, (TELA_LARGURA // 2 - texto_pontuacao_final.get_width() // 2, TELA_ALTURA // 2 - 50))
        texto_reiniciar = FONTE_PRESSIONAR_ESPACO_GO.render("Pressione 'Espaço' para continuar.", 1, (255, 255, 255))
        tela.blit(texto_reiniciar, (TELA_LARGURA // 2 - texto_reiniciar.get_width() // 2, TELA_ALTURA // 2))
    else:
        # Desenha a Sailor Moon e os canos
        for moon in sailor:
            moon.desenhar(tela)
        for cano in canos:
            cano.desenhar(tela)

        # Exibe a pontuação atual
        texto = FONTE_PONTOS.render(f"Score: {pontos}", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

        # Exibe a mensagem de início se o jogo ainda não começou
        if not game_started:
            texto_inicio = FONTE_INICIO.render("Sailor Game", 1, (255, 255, 255))
            tela.blit(texto_inicio, (TELA_LARGURA // 2 - texto_inicio.get_width() // 2, TELA_ALTURA // 3))

    chao.desenhar(tela)  # Desenha o chão
    pygame.display.update()  # Atualiza a tela

# Função principal do jogo
def main():
    sailormoon = [Sailor(230, 350)]  # Inicializa a Sailor Moon
    chao = Chao(730)  # Inicializa o chão
    canos = [Cano(700)]  # Inicializa os canos
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))  # Define o tamanho da tela do jogo
    pontos = 0  # Inicializa a pontuação
    relogio = pygame.time.Clock()  # Controla a taxa de atualização do jogo (FPS)

    rodando = True  # Variável que indica se o jogo está rodando
    game_started = False  # Indica se o jogo já começou
    game_over = False  # Indica se o jogo acabou

    while rodando:
        relogio.tick(30)  # Define a taxa de atualização (FPS)

        # Interação com o usuário (teclas pressionadas)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se o jogador fechar o jogo
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Se a tecla espaço for pressionada
                    if game_over:
                        # Reinicia o jogo se estiver em estado de Game Over
                        sailormoon = [Sailor(230, 350)]
                        canos = [Cano(700)]
                        pontos = 0
                        game_over = False
                        game_started = False
                    elif not game_started:
                        game_started = True  # Começa o jogo
                    else:
                        for moon in sailormoon:
                            moon.pular()  # Faz a Sailor Moon pular

        if game_over:
            continue  # Se o jogo acabou, não atualiza os elementos

        if game_started:
            # Move a Sailor Moon, o chão e os canos
            for moon in sailormoon:
                moon.mover()
            chao.mover()

            remover_canos = []
            adicionar_cano = False

            for cano in canos:
                cano.mover()

                # Verifica se há colisão entre a Sailor Moon e os canos
                for i, moon in enumerate(sailormoon):
                    if cano.colidir(moon):
                        game_over = True  # Se houver colisão, termina o jogo

                    # Verifica se a Sailor Moon passou pelo cano e contabiliza pontos
                    if not cano.passou and cano.x < moon.x:
                        cano.passou = True
                        adicionar_cano = True

                # Remove os canos que saíram da tela
                if cano.x + cano.CANO_BASE.get_width() < 0:
                    remover_canos.append(cano)

            if adicionar_cano:
                pontos += 1  # Aumenta a pontuação
                canos.append(Cano(600))  # Adiciona um novo cano

            for cano in remover_canos:
                canos.remove(cano)  # Remove os canos fora da tela

            # Verifica se a Sailor Moon tocou o chão (Game Over)
            for i, moon in enumerate(sailormoon):
                if moon.y + moon.imagem.get_height() >= 730:
                    game_over = True

        desenhar_tela(tela, sailormoon, canos, chao, pontos, game_started, game_over)  # Atualiza a tela

pygame.mixer.init()

# Carregar a música
pygame.mixer.music.load(os.path.join('musica', 'musicatema.mp3'))  # Caminho para o arquivo de música

# Configurar a música para tocar em loop (-1 significa que vai tocar indefinidamente)
pygame.mixer.music.play(-1)

# Volume da música (de 0.0 a 1.0)
pygame.mixer.music.set_volume(0.5)

if __name__ == '__main__':
    main()  # Chama a função principal para iniciar o jogo